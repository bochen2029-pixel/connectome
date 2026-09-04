"""The provenance slice: which session produced which document.

CONNECTOME v5.5 section 6.2, slice 5.  Every other relation in the field is a statement
about similarity; this one is a statement about *causation*, and it is free.  When a
session message and a document span share a long exact n-gram, the document did not
merely resemble that conversation - it came out of it.

Exactness is the whole point.  A 12-gram of ordinary prose recurring verbatim across two
sources is not a coincidence at corpus scale, so the edge needs no model, no threshold
and no judgement: it is a fact about the bytes.  That makes this slice the only one that
can be trusted without corroboration, and the reason the spec builds free goldens from it.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

_WORD = re.compile(r"\w+")


@dataclass(frozen=True)
class ProvenanceEdge:
    chunk: int  # the document chunk
    message: int  # the transcript message
    shared: int  # how many distinct n-grams they share
    session: str


def ngrams(text: str, n: int = 12) -> set[str]:
    """Word n-grams, lowercased.  Short texts yield nothing rather than a partial key."""
    words = _WORD.findall(text.lower())
    if len(words) < n:
        return set()
    return {" ".join(words[i : i + n]) for i in range(len(words) - n + 1)}


def build_index(texts: list[str], n: int = 12) -> dict[str, list[int]]:
    """n-gram -> the items containing it.

    Grams appearing in a great many items are boilerplate (headers, licence text, a
    repeated preamble) and carry no provenance, so they are dropped: an edge should mean
    "this came from that", not "both contain the standard footer".
    """
    index: dict[str, list[int]] = defaultdict(list)
    for i, text in enumerate(texts):
        for g in ngrams(text, n):
            index[g].append(i)
    cutoff = max(3, len(texts) // 200)
    return {g: ids for g, ids in index.items() if len(ids) <= cutoff}


def link(
    chunk_texts: list[str],
    message_texts: list[str],
    sessions: list[str],
    *,
    n: int = 12,
    min_shared: int = 1,
) -> list[ProvenanceEdge]:
    """Find (chunk, message) pairs sharing at least `min_shared` exact n-grams."""
    index = build_index(message_texts, n)
    hits: dict[tuple[int, int], int] = defaultdict(int)

    for ci, text in enumerate(chunk_texts):
        for g in ngrams(text, n):
            for mi in index.get(g, ()):
                hits[(ci, mi)] += 1

    return [
        ProvenanceEdge(chunk=ci, message=mi, shared=count, session=sessions[mi])
        for (ci, mi), count in sorted(hits.items())
        if count >= min_shared
    ]


def sessions_for_document(
    edges: list[ProvenanceEdge], doc_of_chunk, doc_id: int
) -> dict[str, int]:
    """Which sessions a document came out of, and how strongly.

    The answer is a distribution, not a single session: a document written over three
    conversations honestly has three parents.
    """
    counts: dict[str, int] = defaultdict(int)
    for e in edges:
        if int(doc_of_chunk[e.chunk]) == doc_id:
            counts[e.session] += e.shared
    return dict(sorted(counts.items(), key=lambda kv: -kv[1]))
