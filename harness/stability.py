"""F-LAYOUT-STABLE: does freezing the partition actually buy stability?

CONNECTOME v5.5 sections 6.3 and 12.  The claim under test is the one the map's identity
rests on: that growing a frozen partition by assignment keeps memberships still, where
re-clustering the whole corpus does not.  Both arms are measured on the same corpus, in
the same arrival order, against the same held-out growth - the only difference is what
happens when new documents land.

The comparison is deliberately unkind to the freeze.  ARI is computed on the chunks the
two arms share, so the freeze gets no credit for the trivial stability of refusing to
place anything, and the re-clustering arm is given the same consensus treatment rather
than a single seed, so it is not a strawman built from a worse algorithm.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .corpus import Corpus
from . import partition as P


@dataclass
class StabilityResult:
    """One growth experiment: a base corpus, then a fraction of it arriving."""

    grown_fraction: float
    frozen_ari: float  # base memberships vs after growth, frozen + assignment
    refit_ari: float  # base memberships vs after growth, re-clustered
    frozen_moved: float  # share of base chunks that changed community
    refit_moved: float
    frozen_drift: float  # nearest-centroid disagreement after growth
    n_base: int
    n_new: int
    overflow: int  # new chunks no community had room for

    @property
    def advantage(self) -> float:
        return self.frozen_ari - self.refit_ari


def grow(
    corpus: Corpus,
    *,
    base_fraction: float = 0.8,
    n_seeds: int = 10,
    seed: int = 0,
    resolution: float = 1.0,
) -> StabilityResult:
    """Partition the first `base_fraction` of arrivals, then let the rest arrive.

    The split is by arrival time, never at random: a partition is asked to survive the
    future, and a random split would leak it.
    """
    order = corpus.order
    cut = int(len(order) * base_fraction)
    base_docs, new_docs = order[:cut], order[cut:]

    base_ids = np.concatenate(
        [np.asarray(corpus.documents_by_id[d].chunk_ids, dtype=np.int64) for d in base_docs]
    )
    new_ids = np.concatenate(
        [np.asarray(corpus.documents_by_id[d].chunk_ids, dtype=np.int64) for d in new_docs]
    )
    base_vec = corpus.vectors[base_ids]
    all_ids = np.concatenate([base_ids, new_ids])
    all_vec = corpus.vectors[all_ids]

    # --- the frozen arm: partition the base once, then assign what arrives ----------
    frozen = P.build(base_vec, n_seeds=n_seeds, seed=seed, resolution=resolution)
    assigned = P.assign(frozen, corpus.vectors[new_ids])
    frozen_after = np.concatenate([frozen.community_of, assigned])
    frozen_moved = 0.0  # by construction: assignment never moves an existing member

    # --- the re-fit arm: cluster the whole grown corpus from scratch -----------------
    refit = P.build(all_vec, n_seeds=n_seeds, seed=seed, resolution=resolution)
    refit_base = refit.community_of[: base_ids.size]

    # ARI on the shared chunks - the base - in both arms.
    frozen_ari = P.ari(frozen.community_of.tolist(), frozen_after[: base_ids.size].tolist())
    refit_ari = P.ari(frozen.community_of.tolist(), refit_base.tolist())

    # "Moved" needs a label correspondence, since community ids are arbitrary between
    # runs.  Map each new community to the old one it overlaps most, then count the
    # members that ended up somewhere else.
    def moved_share(before: np.ndarray, after: np.ndarray) -> float:
        mapping: dict[int, int] = {}
        for c in np.unique(after):
            members = after == c
            if not members.any():
                continue
            counts = np.bincount(before[members], minlength=int(before.max()) + 1)
            mapping[int(c)] = int(np.argmax(counts))
        remapped = np.asarray([mapping.get(int(c), -1) for c in after], dtype=np.int32)
        return float(np.mean(remapped != before))

    refit_moved = moved_share(frozen.community_of, refit_base)

    # Drift after growth: the number a version event would actually fire on.
    grown = P.Partition(
        version=frozen.version,
        community_of=frozen_after,
        centroids=frozen.centroids,
        sizes=np.bincount(
            frozen_after[frozen_after >= 0], minlength=frozen.centroids.shape[0]
        ).astype(np.int32),
        seed=frozen.seed,
        resolution=frozen.resolution,
        n_seeds=frozen.n_seeds,
        modularity=frozen.modularity,
        co_classification=frozen.co_classification,
    )
    frozen_drift = P.drift(grown, all_vec)

    return StabilityResult(
        grown_fraction=1.0 - base_fraction,
        frozen_ari=frozen_ari,
        refit_ari=refit_ari,
        frozen_moved=frozen_moved,
        refit_moved=refit_moved,
        frozen_drift=frozen_drift,
        n_base=int(base_ids.size),
        n_new=int(new_ids.size),
        overflow=int((assigned < 0).sum()),
    )


def seed_stability(
    vectors: np.ndarray, *, seeds: int = 5, n_seeds: int = 10, resolution: float = 1.0
) -> tuple[float, float]:
    """How much a fresh partition disagrees with itself across base seeds.

    This is the baseline the freeze is measured against: on the estate, plain Leiden
    scored ARI 0.73-0.86 between seeds.  Consensus should do better, and how much
    better is worth knowing before trusting either.
    """
    parts = [
        P.build(vectors, n_seeds=n_seeds, seed=s * 1000, resolution=resolution).community_of
        for s in range(seeds)
    ]
    scores = [P.ari(parts[0].tolist(), p.tolist()) for p in parts[1:]]
    return (float(np.mean(scores)), float(np.min(scores))) if scores else (1.0, 1.0)
