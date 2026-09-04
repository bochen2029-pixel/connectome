"""M1's acceptance tests.  Run: python -m harness.test_harness

The harness is the instrument every later claim is measured with, so its own failure
modes matter more than its features.  These check the properties that would silently
corrupt every downstream number: that scoring never looks forward, that the loss is
deterministic, that a shuffle actually changes the answer, and that the front detector
survives the degenerate corpora that broke its first version.
"""

from __future__ import annotations

import sys

import numpy as np

from .corpus import Corpus, Document, load_store
from .fronts import detect
from .loss import DocScore, deciles, residual_curve

_fail = 0


def expect(cond: bool, what: str) -> None:
    global _fail
    if cond:
        print(f"  ok    {what}")
    else:
        print(f"  FAIL  {what}")
        _fail += 1


def synthetic(n_docs: int = 30, per_doc: int = 4, dim: int = 32, seed: int = 7) -> Corpus:
    """A corpus with a planted front: the second half occupies a different subspace."""
    rng = np.random.default_rng(seed)
    vecs = rng.normal(size=(n_docs * per_doc, dim)).astype(np.float32)
    half = n_docs // 2
    vecs[: half * per_doc, dim // 2 :] *= 0.01     # early documents live in one half
    vecs[half * per_doc :, : dim // 2] *= 0.01     # later ones in the other
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9

    docs, doc_of = [], np.zeros(n_docs * per_doc, dtype=np.int32)
    for d in range(n_docs):
        ids = tuple(range(d * per_doc, (d + 1) * per_doc))
        for i in ids:
            doc_of[i] = d
        docs.append(Document(d, f"doc{d}", "", float(1_700_000_000 + d * 86400), "name", ids))
    return Corpus(vectors=vecs, doc_of_chunk=doc_of, documents=docs)


def test_no_lookahead() -> None:
    """A document must be scored against its past only - never against itself."""
    c = synthetic()
    scores = residual_curve(c)
    expect(len(scores) == len(c.order) - 1, "the first document is not scored against nothing")
    expect(all(s.residual > 1e-6 for s in scores), "no document scores zero residual against itself")

    # Truncating the corpus must not change the scores of the documents that remain:
    # if it did, scoring would be peeking at the future.
    head_ids = c.order[:15]
    head = Corpus(
        vectors=c.vectors,
        doc_of_chunk=c.doc_of_chunk,
        documents=[c.documents_by_id[i] for i in head_ids],
    )
    full = {s.doc_id: round(s.residual, 9) for s in scores if s.doc_id in set(head_ids)}
    trunc = {s.doc_id: round(s.residual, 9) for s in residual_curve(head)}
    expect(all(full[k] == trunc[k] for k in trunc), "scores are unchanged by removing the future")


def test_determinism() -> None:
    c = synthetic()
    a = [round(s.residual, 12) for s in residual_curve(c)]
    b = [round(s.residual, 12) for s in residual_curve(c)]
    expect(a == b, "the loss repeats exactly")

    small = [round(s.residual, 12) for s in residual_curve(c, block=3)]
    expect(a == small, "block size does not change the result (float64 accumulation)")


def test_planted_front() -> None:
    """The planted subspace change must show up as a front, and not before it happens."""
    c = synthetic(n_docs=120, per_doc=4)
    s = residual_curve(c)
    d = detect(s, window=6, trailing=30)
    expect(len(d.fronts) >= 1, "the planted front is detected")
    if d.fronts:
        first = d.fronts[0]
        planted_at = 60 - 1                        # first scored position of the second half
        expect(
            abs(first.opened_at - planted_at) <= 10,
            f"it opens near the plant (at {first.opened_at}, planted {planted_at})",
        )


def test_degenerate_corpora() -> None:
    """The failures that broke the first detector must not raise or hang."""
    expect(detect([], window=8, trailing=40).fronts == [], "an empty series yields no fronts")

    flat = [DocScore(i, i, 0.3, 0.0, 4) for i in range(200)]
    expect(detect(flat).fronts == [], "a flat corpus with no repetition yields no fronts")

    identical = [DocScore(i, i, 0.0, 1.0, 4) for i in range(200)]
    expect(detect(identical).fronts == [], "a wholly duplicated corpus yields no fronts")

    short = [DocScore(i, i, 0.3, 0.0, 4) for i in range(5)]
    expect(detect(short).fronts == [], "a corpus shorter than the window is handled")


def test_shuffle_matters() -> None:
    """If order did not matter, the whole thesis would be empty."""
    c = synthetic(n_docs=60)
    import random

    order = list(c.order)
    random.Random(3).shuffle(order)
    t = deciles(residual_curve(c, c.order))
    s = deciles(residual_curve(c, order))
    expect(
        abs(t[0][0] - s[0][0]) > 1e-3,
        "arrival order and a shuffle give different first-decile residuals",
    )


def test_live_store() -> None:
    """The real corpus, if the store is present."""
    try:
        c = load_store()
    except (FileNotFoundError, OSError):
        print("  skip  no store/ in this directory")
        return
    expect(c.n_chunks == c.vectors.shape[0], "every chunk has a vector")
    expect(all(d.date_source in ("name", "mtime") for d in c.documents), "no date was guessed")
    norms = np.linalg.norm(c.vectors[:256], axis=1)
    expect(bool(np.all(np.abs(norms - 1.0) < 1e-3)), "vectors are L2-normalised")


if __name__ == "__main__":
    for fn in (
        test_no_lookahead,
        test_determinism,
        test_planted_front,
        test_degenerate_corpora,
        test_shuffle_matters,
        test_live_store,
    ):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\n{_fail} failure(s)")
    sys.exit(1 if _fail else 0)
