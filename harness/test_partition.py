"""M2's acceptance tests.  Run: python -m harness.test_partition

The partition is the map's identity: if it moves under its own weight, nothing built on
it can be trusted to mean the same thing twice.  These check the properties that would
make the freeze a lie - that it is deterministic, that assignment truly never moves an
existing member, that overflow is real rather than a silent distortion, and that the
drift meter reports rather than hides.
"""

from __future__ import annotations

import sys

import numpy as np

from .corpus import Corpus, Document, load_store
from . import partition as P
from . import stability as S

_fail = 0


def expect(cond: bool, what: str) -> None:
    global _fail
    if cond:
        print(f"  ok    {what}")
    else:
        print(f"  FAIL  {what}")
        _fail += 1


def blobs(n_per: int = 40, k: int = 5, dim: int = 24, spread: float = 0.08, seed: int = 3):
    """k well-separated clusters: a corpus whose right answer is known by construction."""
    rng = np.random.default_rng(seed)
    centres = rng.normal(size=(k, dim))
    centres /= np.linalg.norm(centres, axis=1, keepdims=True)
    vecs = np.repeat(centres, n_per, axis=0) + spread * rng.normal(size=(k * n_per, dim))
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
    truth = np.repeat(np.arange(k), n_per)
    return vecs.astype(np.float32), truth


def test_recovers_structure() -> None:
    vecs, truth = blobs()
    part = P.build(vecs, n_seeds=6)
    expect(P.ari(truth.tolist(), part.community_of.tolist()) > 0.95, "planted clusters are recovered")
    expect(part.modularity > 0.5, f"modularity is substantial ({part.modularity:.3f})")
    expect(
        bool(np.all(part.sizes > 0)),
        "every community that survives the size floor has members",
    )


def test_deterministic() -> None:
    vecs, _ = blobs()
    a = P.build(vecs, n_seeds=6, seed=11).community_of
    b = P.build(vecs, n_seeds=6, seed=11).community_of
    expect(np.array_equal(a, b), "the same seed gives the identical partition")

    src1, dst1, _ = P.knn_graph(vecs)
    src2, dst2, _ = P.knn_graph(vecs, block=7)
    expect(
        np.array_equal(src1, src2) and np.array_equal(dst1, dst2),
        "the kNN graph does not depend on the block size",
    )


def test_consensus_beats_single_seed() -> None:
    """The reason for ten runs: agreement should be steadier than any one run."""
    vecs, _ = blobs(spread=0.30)  # ambiguous enough that seeds can disagree
    src, dst, wt = P.knn_graph(vecs)
    singles = [P._leiden_once(vecs.shape[0], src, dst, wt, 1.0, s) for s in (0, 1, 2, 3)]
    single_ari = float(np.mean([P.ari(singles[0].tolist(), m.tolist()) for m in singles[1:]]))

    cons = [
        P.consensus(vecs.shape[0], src, dst, wt, n_seeds=8, base_seed=b)[0] for b in (0, 100, 200)
    ]
    cons_ari = float(np.mean([P.ari(cons[0].tolist(), m.tolist()) for m in cons[1:]]))
    expect(
        cons_ari >= single_ari - 1e-9,
        f"consensus is at least as stable as single seeds ({cons_ari:.3f} vs {single_ari:.3f})",
    )


def test_assignment_never_moves_members() -> None:
    vecs, _ = blobs()
    part = P.build(vecs, n_seeds=6)
    before = part.community_of.copy()
    rng = np.random.default_rng(9)
    newcomers = vecs[:30] + 0.05 * rng.normal(size=(30, vecs.shape[1])).astype(np.float32)
    newcomers /= np.linalg.norm(newcomers, axis=1, keepdims=True)

    assigned = P.assign(part, newcomers.astype(np.float32))
    expect(np.array_equal(before, part.community_of), "assignment leaves existing members untouched")
    expect(assigned.shape[0] == 30, "every newcomer gets a verdict")
    placed = assigned >= 0
    expect(
        bool(np.all(assigned[placed] < part.centroids.shape[0])),
        "placed newcomers land in real communities",
    )


def test_overflow_is_real() -> None:
    """A full map must say so, not quietly stretch."""
    vecs, _ = blobs(n_per=20, k=3)
    part = P.build(vecs, n_seeds=6)
    rng = np.random.default_rng(5)
    flood = vecs[:1] + 0.01 * rng.normal(size=(600, vecs.shape[1])).astype(np.float32)
    flood /= np.linalg.norm(flood, axis=1, keepdims=True)

    assigned = P.assign(part, flood.astype(np.float32), size_cap=1.2)
    expect((assigned < 0).any(), "a flood of near-identical chunks overflows rather than fitting")
    sizes = np.bincount(assigned[assigned >= 0], minlength=part.centroids.shape[0])
    cap = int(1.2 * part.sizes.mean())
    expect(bool(np.all(sizes + part.sizes <= cap + 1)), "no community exceeds its size cap")


def test_drift_meter() -> None:
    vecs, _ = blobs()
    part = P.build(vecs, n_seeds=6)
    expect(P.drift(part, vecs) < 0.05, "a partition barely drifts against its own corpus")

    # Rotate the corpus away from its centroids: drift must notice.
    rng = np.random.default_rng(2)
    moved = vecs + 0.9 * rng.normal(size=vecs.shape).astype(np.float32)
    moved /= np.linalg.norm(moved, axis=1, keepdims=True)
    expect(P.drift(part, moved.astype(np.float32)) > 0.2, "drift rises when the corpus moves away")


def test_growth_on_the_estate() -> None:
    """The claim M2 exists to test, on the real corpus if it is present."""
    try:
        c = load_store()
    except (FileNotFoundError, OSError):
        print("  skip  no store/ in this directory")
        return
    r = S.grow(c, base_fraction=0.8, n_seeds=6)
    expect(r.frozen_ari > r.refit_ari, f"freezing beats re-clustering ({r.frozen_ari:.3f} vs {r.refit_ari:.3f})")
    expect(r.frozen_moved == 0.0, "no existing member moved under growth")
    expect(r.refit_moved > 0.05, f"re-clustering does move members ({r.refit_moved:.1%})")
    expect(0.0 <= r.frozen_drift <= 1.0, f"drift is reported, not hidden ({r.frozen_drift:.3f})")


if __name__ == "__main__":
    for fn in (
        test_recovers_structure,
        test_deterministic,
        test_consensus_beats_single_seed,
        test_assignment_never_moves_members,
        test_overflow_is_real,
        test_drift_meter,
        test_growth_on_the_estate,
    ):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\n{_fail} failure(s)")
    sys.exit(1 if _fail else 0)
