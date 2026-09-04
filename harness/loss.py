"""The loss: how badly the field, as it stood, predicted what arrived next.

CONNECTOME v5.5 section 2.1.  The signal is the tape in arrival order; the teacher is
the next document; the loss is its residual against everything before it.  Nothing here
consults a label, and nothing here may look forward - `residual_curve` walks the corpus
strictly in order and a document is scored before its own chunks enter the field.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .corpus import Corpus

# Above this cosine a passage is a retelling of one already held, not a prediction
# failure.  The value is the trough of the corpus's own bimodal top-1 distribution
# (measured 0.97 on the estate) and is re-estimated per corpus, never assumed.
RETELLING_COSINE = 0.97


@dataclass
class DocScore:
    doc_id: int
    position: int            # index into the order actually walked
    residual: float          # mean over chunks of (1 - max cosine to anything earlier)
    retelling_share: float   # share of chunks that are retellings of something earlier
    n_chunks: int


def residual_curve(
    corpus: Corpus,
    order: Sequence[int] | None = None,
    *,
    retelling_cosine: float = RETELLING_COSINE,
    block: int = 4096,
) -> list[DocScore]:
    """Walk the corpus in `order`, scoring each document against only its past.

    The first document has no past and is skipped rather than scored against nothing.
    """
    order = list(order if order is not None else corpus.order)
    X = corpus.vectors
    seen = np.zeros(corpus.n_chunks, dtype=bool)
    out: list[DocScore] = []

    for position, doc_id in enumerate(order):
        ids = np.asarray(corpus.documents_by_id[doc_id].chunk_ids, dtype=np.int64)
        if seen.any() and ids.size:
            past = np.flatnonzero(seen)
            Q = X[ids].astype(np.float64)
            best = np.full(ids.size, -1.0, dtype=np.float64)
            # Blocked so a large past never materialises a full similarity matrix.
            # The dot products accumulate in float64: in float32 the sum order inside
            # a block changes the last bits, so the residual would depend on the block
            # size - an implementation detail silently moving a reported number, which
            # is exactly what the determinism rule exists to prevent.  Measured drift
            # before this fix: 6e-08 on 13 of 29 documents.
            for start in range(0, past.size, block):
                sims = Q @ X[past[start : start + block]].T.astype(np.float64)
                np.maximum(best, sims.max(axis=1), out=best)
            out.append(
                DocScore(
                    doc_id=doc_id,
                    position=position,
                    residual=float(np.mean(1.0 - best)),
                    retelling_share=float(np.mean(best >= retelling_cosine)),
                    n_chunks=int(ids.size),
                )
            )
        seen[ids] = True
    return out


def deciles(scores: Sequence[DocScore], k: int = 10) -> list[tuple[float, float]]:
    """Mean (residual, retelling share) per k-quantile of arrival position."""
    n = len(scores)
    if n == 0:
        return []
    res = np.asarray([s.residual for s in scores], dtype=np.float64)
    ret = np.asarray([s.retelling_share for s in scores], dtype=np.float64)
    out = []
    for q in range(k):
        lo, hi = int(q * n / k), int((q + 1) * n / k)
        if hi <= lo:
            out.append((float("nan"), float("nan")))
            continue
        out.append((float(res[lo:hi].mean()), float(ret[lo:hi].mean())))
    return out


@dataclass
class ConvergenceResult:
    """F-CONVERGE: does arrival order predict better than an arbitrary order?"""

    time_deciles: list[tuple[float, float]]
    shuffled_deciles: list[tuple[float, float]]
    time_scores: list[DocScore]
    n_shuffles: int

    def ratio(self, deciles_: list[tuple[float, float]], head: int = 2, tail: int = 2) -> float:
        h = float(np.mean([d[0] for d in deciles_[:head]]))
        t = float(np.mean([d[0] for d in deciles_[-tail:]]))
        return t / h if h else float("nan")

    def advantage(self) -> list[float]:
        """Per decile: how much lower the time-ordered residual is, as a fraction."""
        return [
            (s[0] - t[0]) / s[0] if s[0] else float("nan")
            for t, s in zip(self.time_deciles, self.shuffled_deciles)
        ]


def converge(corpus: Corpus, *, shuffles: int = 5, seed: int = 0) -> ConvergenceResult:
    """The master falsifier, run without a single label."""
    time_scores = residual_curve(corpus, corpus.order)
    time_dec = deciles(time_scores)

    rng = random.Random(seed)
    shuffled = np.zeros((shuffles, len(time_dec), 2), dtype=np.float64)
    for s in range(shuffles):
        order = list(corpus.order)
        rng.shuffle(order)
        shuffled[s] = np.asarray(deciles(residual_curve(corpus, order)), dtype=np.float64)

    mean = shuffled.mean(axis=0)
    return ConvergenceResult(
        time_deciles=time_dec,
        shuffled_deciles=[(float(a), float(b)) for a, b in mean],
        time_scores=time_scores,
        n_shuffles=shuffles,
    )
