"""Loading a corpus in arrival order.

The tape is truth; this module only reads it.  A document's date comes from its own
name where the corpus states one (the estate's convention is a trailing YYYY-MM-DD),
and from the filesystem otherwise - never from a model, and never from the order the
files happen to sit in on disk.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
from dataclasses import dataclass, field
from typing import Iterable, Sequence

import numpy as np

_DATE_IN_NAME = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")


@dataclass(frozen=True)
class Document:
    doc_id: int
    name: str
    path: str
    when: float                 # POSIX seconds; the arrival axis
    date_source: str            # "name" | "mtime" | "absent"
    chunk_ids: tuple[int, ...]


@dataclass
class Corpus:
    """Chunk vectors plus the documents that own them, ordered by arrival."""

    vectors: np.ndarray                 # (n_chunks, dim), L2-normalised float32
    doc_of_chunk: np.ndarray            # (n_chunks,) int32
    documents: list[Document]
    order: list[int] = field(default_factory=list)   # document ids, arrival order

    @property
    def n_chunks(self) -> int:
        return int(self.vectors.shape[0])

    @property
    def dim(self) -> int:
        return int(self.vectors.shape[1])

    def chunks_of(self, doc_id: int) -> np.ndarray:
        return np.asarray(self.documents_by_id[doc_id].chunk_ids, dtype=np.int64)

    def __post_init__(self) -> None:
        self.documents_by_id = {d.doc_id: d for d in self.documents}
        if not self.order:
            self.order = [d.doc_id for d in sorted(self.documents, key=lambda x: (x.when, x.doc_id))]

    def span(self) -> tuple[_dt.date, _dt.date]:
        whens = [d.when for d in self.documents]
        return (
            _dt.datetime.fromtimestamp(min(whens)).date(),
            _dt.datetime.fromtimestamp(max(whens)).date(),
        )


def _date_of(doc: dict) -> tuple[float | None, str]:
    """A document's arrival time, and where the number came from."""
    haystack = " ".join(str(doc.get(k, "")) for k in ("n", "p", "f", "t"))
    m = _DATE_IN_NAME.search(haystack)
    if m:
        try:
            return _dt.datetime(int(m[1]), int(m[2]), int(m[3])).timestamp(), "name"
        except ValueError:
            pass
    for key in ("f", "p"):
        path = doc.get(key)
        if path and os.path.exists(path):
            return os.path.getmtime(path), "mtime"
    return None, "absent"


def load_store(store_dir: str = "store") -> Corpus:
    """Read the v0.1 organ's store: field.npz for vectors, index.json for structure."""
    with np.load(os.path.join(store_dir, "field.npz")) as z:
        vectors = z["X"].astype(np.float32)
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-9

    with open(os.path.join(store_dir, "index.json"), encoding="utf-8") as fh:
        index = json.load(fh)

    chunks = index["chunks"]
    if len(chunks) != vectors.shape[0]:
        raise ValueError(
            f"store is inconsistent: {len(chunks)} chunks but {vectors.shape[0]} vectors"
        )

    doc_of_chunk = np.asarray([c["d"] for c in chunks], dtype=np.int32)
    by_doc: dict[int, list[int]] = {}
    for i, c in enumerate(chunks):
        by_doc.setdefault(int(c["d"]), []).append(i)

    documents: list[Document] = []
    undated = 0
    for doc in index["docs"]:
        doc_id = int(doc["i"])
        ids = by_doc.get(doc_id)
        if not ids:
            continue                     # a document with no chunks is not in the field
        when, source = _date_of(doc)
        if when is None:
            undated += 1
            continue                     # never guess an arrival time
        documents.append(
            Document(
                doc_id=doc_id,
                name=str(doc.get("n", f"doc-{doc_id}")),
                path=str(doc.get("f", "")),
                when=when,
                date_source=source,
                chunk_ids=tuple(ids),
            )
        )

    corpus = Corpus(vectors=vectors, doc_of_chunk=doc_of_chunk, documents=documents)
    corpus.undated = undated
    return corpus
