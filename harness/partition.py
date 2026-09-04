"""The partition as a versioned artifact, not a recomputable process.

CONNECTOME v5.5 section 6.3.  A map that reshuffles on every rebuild cannot hold an
identity: measured on this estate, fresh Leiden moves 14-27% of memberships between
seeds (ARI 0.73-0.86).  So the partition is computed once, frozen, and thereafter grown
by *assignment* - a new chunk joins the community whose centroid it is nearest, and
nothing that already exists moves.  Drift is measured rather than assumed, and a version
event is a deliberate act with an old->new map, never a side effect of ingest.

Consensus is what makes the freeze worth having.  A single Leiden run is one sample from
a distribution of near-optimal partitions; ten runs agreeing on a pair of nodes is
evidence about the corpus, while one run agreeing with itself is evidence about a seed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Sequence

import numpy as np

try:
    import igraph as ig
    import leidenalg

    _HAVE_LEIDEN = True
except ImportError:  # pragma: no cover
    _HAVE_LEIDEN = False


@dataclass
class Partition:
    """A frozen artifact.  Its version is part of every locator that cites it."""

    version: int
    community_of: np.ndarray  # (n_chunks,) int32; -1 = overflow, not a member
    centroids: np.ndarray  # (n_communities, dim) float32, L2-normalised
    sizes: np.ndarray  # (n_communities,) int32
    seed: int
    resolution: float
    n_seeds: int  # how many runs the consensus was taken over
    modularity: float
    co_classification: float  # mean agreement across the consensus runs

    def to_json(self) -> str:
        return json.dumps(
            {
                "version": self.version,
                "seed": self.seed,
                "resolution": self.resolution,
                "n_seeds": self.n_seeds,
                "modularity": round(self.modularity, 6),
                "co_classification": round(self.co_classification, 6),
                "n_communities": int(self.centroids.shape[0]),
                "sizes": self.sizes.tolist(),
            },
            indent=2,
        )


def knn_graph(
    vectors: np.ndarray, k: int = 10, threshold: float = 0.50, block: int = 512
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Mutual-kNN edges over the cosine field.  Deterministic: ties break by index.

    Returns (src, dst, weight) with src < dst, so the graph is undirected and each edge
    appears exactly once.
    """
    n = vectors.shape[0]
    X = vectors.astype(np.float32)
    neighbours: list[np.ndarray] = []
    scores: list[np.ndarray] = []

    for start in range(0, n, block):
        sims = X[start : start + block] @ X.T
        for row in range(sims.shape[0]):
            sims[row, start + row] = -1.0  # never a neighbour of itself
        idx = np.argpartition(-sims, k, axis=1)[:, :k]
        # Sort each row by (-score, index) so the result cannot depend on
        # argpartition's internal ordering.
        for r in range(idx.shape[0]):
            idx[r] = sorted(idx[r], key=lambda j: (-sims[r, j], j))
        neighbours.append(idx)
        scores.append(np.take_along_axis(sims, idx, axis=1))

    nbr = np.vstack(neighbours)
    sc = np.vstack(scores)

    # Mutual: keep an edge only when each node is in the other's list.  This is what
    # stops a hub from absorbing the graph.
    as_set = [set(map(int, row)) for row in nbr]
    src: list[int] = []
    dst: list[int] = []
    wt: list[float] = []
    for i in range(n):
        for j, s in zip(nbr[i], sc[i]):
            j = int(j)
            if s < threshold or j <= i:
                continue
            if i in as_set[j]:
                src.append(i)
                dst.append(j)
                wt.append(float(s))

    return (
        np.asarray(src, np.int32),
        np.asarray(dst, np.int32),
        np.asarray(wt, np.float32),
    )


def _leiden_once(
    n: int, src: np.ndarray, dst: np.ndarray, wt: np.ndarray, resolution: float, seed: int
) -> np.ndarray:
    if not _HAVE_LEIDEN:
        raise RuntimeError(
            "leidenalg is required for the partition; pip install leidenalg python-igraph"
        )
    g = ig.Graph(n=n, edges=list(zip(src.tolist(), dst.tolist())), directed=False)
    g.es["weight"] = wt.tolist()
    part = leidenalg.find_partition(
        g,
        leidenalg.RBConfigurationVertexPartition,
        weights="weight",
        resolution_parameter=resolution,
        seed=seed,
        n_iterations=-1,  # to convergence, not a fixed count
    )
    return np.asarray(part.membership, dtype=np.int32)


def consensus(
    n: int,
    src: np.ndarray,
    dst: np.ndarray,
    wt: np.ndarray,
    *,
    resolution: float = 1.0,
    n_seeds: int = 10,
    threshold: float = 0.8,
    base_seed: int = 0,
) -> tuple[np.ndarray, float]:
    """Run Leiden n_seeds times; keep only the edges the runs agree on.

    Two nodes stay together when they land in the same community in at least
    `threshold` of the runs.  The membership is then the connected components of that
    agreement graph, which is stable by construction: it depends on what the runs
    concur about, not on which run happened to go first.
    """
    memberships = [
        _leiden_once(n, src, dst, wt, resolution, base_seed + s) for s in range(n_seeds)
    ]

    # Agreement is computed on the existing edges only - the graph is sparse, and a
    # dense n^2 co-classification matrix is both unnecessary and unaffordable at scale.
    agree = np.zeros(src.size, dtype=np.float32)
    for m in memberships:
        agree += (m[src] == m[dst]).astype(np.float32)
    agree /= float(n_seeds)

    keep = agree >= threshold
    g = ig.Graph(n=n, edges=list(zip(src[keep].tolist(), dst[keep].tolist())), directed=False)
    labels = np.asarray(g.connected_components().membership, dtype=np.int32)
    return labels, float(agree.mean())


def build(
    vectors: np.ndarray,
    *,
    version: int = 1,
    resolution: float = 1.0,
    n_seeds: int = 10,
    seed: int = 0,
    k: int = 10,
    min_size: int = 3,
) -> Partition:
    """Compute partition/vN once.  Everything after this is assignment."""
    n = vectors.shape[0]
    src, dst, wt = knn_graph(vectors, k=k)
    labels, coclass = consensus(
        n, src, dst, wt, resolution=resolution, n_seeds=n_seeds, base_seed=seed
    )

    # Fold communities below the floor into the nearest surviving centroid: a
    # community of one is a node, not a region of the map.
    uniq, counts = np.unique(labels, return_counts=True)
    keep = uniq[counts >= min_size]
    if keep.size == 0:
        keep = uniq[np.argsort(-counts)[:1]]

    cent = np.zeros((keep.size, vectors.shape[1]), dtype=np.float32)
    for ci, c in enumerate(keep):
        cent[ci] = vectors[labels == c].mean(axis=0)
    cent /= np.linalg.norm(cent, axis=1, keepdims=True) + 1e-9

    community_of = np.full(n, -1, dtype=np.int32)
    for ci, c in enumerate(keep):
        community_of[labels == c] = ci
    orphans = np.flatnonzero(community_of < 0)
    if orphans.size:
        community_of[orphans] = np.argmax(vectors[orphans] @ cent.T, axis=1).astype(np.int32)

    # Recompute centroids once the folded members are in, so a centroid is the mean of
    # what it actually holds.
    for ci in range(keep.size):
        members = community_of == ci
        if members.any():
            cent[ci] = vectors[members].mean(axis=0)
    cent /= np.linalg.norm(cent, axis=1, keepdims=True) + 1e-9
    sizes = np.bincount(community_of, minlength=keep.size).astype(np.int32)

    g = ig.Graph(n=n, edges=list(zip(src.tolist(), dst.tolist())), directed=False)
    g.es["weight"] = wt.tolist()
    modularity = float(g.modularity(community_of.tolist(), weights="weight"))

    return Partition(
        version=version,
        community_of=community_of,
        centroids=cent,
        sizes=sizes,
        seed=seed,
        resolution=resolution,
        n_seeds=n_seeds,
        modularity=modularity,
        co_classification=coclass,
    )


def assign(part: Partition, vectors: np.ndarray, *, size_cap: float = 2.0) -> np.ndarray:
    """Place new chunks in the frozen partition.  Nothing that exists moves.

    A community over `size_cap` times the mean is full; the next-nearest takes the
    chunk, and if every candidate is full it goes to the overflow bucket (-1), which is
    what seeds the next version rather than silently distorting this one.
    """
    if vectors.size == 0:
        return np.zeros(0, dtype=np.int32)

    sims = vectors @ part.centroids.T
    order = np.argsort(-sims, axis=1)
    cap = max(1, int(size_cap * part.sizes.mean())) if part.sizes.size else 1
    room = np.maximum(cap - part.sizes, 0).astype(np.int64)

    out = np.full(vectors.shape[0], -1, dtype=np.int32)
    for i in range(vectors.shape[0]):
        for c in order[i]:
            if room[c] > 0:
                out[i] = np.int32(c)
                room[c] -= 1
                break
    return out


def drift(part: Partition, vectors: np.ndarray) -> float:
    """The share of members whose nearest centroid is no longer their own community.

    This is the number a version event is triggered on, and it is measured against the
    corpus rather than compared with a threshold someone chose.
    """
    members = part.community_of >= 0
    if not members.any():
        return 0.0
    nearest = np.argmax(vectors[members] @ part.centroids.T, axis=1).astype(np.int32)
    return float(np.mean(nearest != part.community_of[members]))


def ari(a: Sequence[int], b: Sequence[int]) -> float:
    """Adjusted Rand index: the measure the freeze exists to improve."""
    from sklearn.metrics import adjusted_rand_score

    return float(adjusted_rand_score(list(a), list(b)))
