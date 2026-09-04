"""Fronts: the two rates a non-stationary corpus needs.

CONNECTOME v5.5 sections 2.5 and 7.3.  The measurement that forced this module is in
section 0: the time-ordered field predicts better than a shuffled one at the head and
the tail of the estate and worse in the middle, because the middle is where the author
opened new subjects.  A corpus is a stream of fronts; the field must converge inside
one (habituation) and open structure between them (vigilance).

WHAT THE FIRST DETECTOR GOT WRONG, kept here because the correction is the finding.
A per-document CUSUM on the raw residual never fired on the estate: max 0.88 against a
5-sigma threshold.  Two reasons, both measurable rather than aesthetic.  (1) Document
residuals are tightly packed - quartiles 0.277 to 0.356 - so a single document, however
novel, is a fraction of a standard deviation and the statistic cannot accumulate before
the next ordinary document drains it.  (2) A front is not a property of one document; it
is a sustained shift in what the corpus is about.  The instrument therefore works on a
*window* of arrivals against the *trailing* field, which is the scale the phenomenon
actually lives at.

The rule below has no fitted constant: the shift is measured in units of the corpus's
own dispersion, and the window is the only knob, stated in documents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

from .loss import DocScore


@dataclass
class Front:
    opened_at: int                 # position in arrival order
    closed_at: int | None
    peak_z: float                  # how far the window ran above the trailing field
    peak_residual: float
    documents: list[int] = field(default_factory=list)

    @property
    def length(self) -> int:
        end = self.closed_at if self.closed_at is not None else self.opened_at
        return end - self.opened_at + 1


@dataclass
class FrontDetection:
    fronts: list[Front]
    z: np.ndarray                  # per position: window mean vs trailing, in sigmas
    window: int
    trailing: int
    open_z: float

    def summary(self) -> str:
        return (
            f"{len(self.fronts)} front(s); window {self.window} docs vs trailing "
            f"{self.trailing}; open at z>{self.open_z}"
        )


def detect(
    scores: Sequence[DocScore],
    *,
    window: int = 8,
    trailing: int = 40,
    open_z: float = 1.0,
    close_z: float = 0.0,
) -> FrontDetection:
    """Find sustained shifts in what the corpus is about.

    For each position, compare the mean residual of the next `window` documents with
    the trailing `trailing` documents, in units of the trailing standard deviation.  A
    front opens when that z rises above `open_z` and closes when it falls back to
    `close_z` - the corpus has stopped surprising the field relative to its own recent
    past, which is what saturation looks like from the outside.
    """
    n = len(scores)
    z = np.full(n, np.nan, dtype=np.float64)
    if n < trailing + window:
        return FrontDetection([], z, window, trailing, open_z)

    res = np.asarray([s.residual for s in scores], dtype=np.float64)
    for i in range(trailing, n - window + 1):
        past = res[i - trailing : i]
        ahead = res[i : i + window]
        sigma = float(past.std())
        z[i] = (float(ahead.mean()) - float(past.mean())) / sigma if sigma > 1e-9 else 0.0

    fronts: list[Front] = []
    current: Front | None = None
    for i in range(n):
        if np.isnan(z[i]):
            continue
        if current is None:
            if z[i] > open_z:
                current = Front(
                    opened_at=i, closed_at=None, peak_z=float(z[i]), peak_residual=float(res[i])
                )
                current.documents.append(scores[i].doc_id)
        else:
            current.documents.append(scores[i].doc_id)
            current.peak_z = max(current.peak_z, float(z[i]))
            current.peak_residual = max(current.peak_residual, float(res[i]))
            if z[i] <= close_z:
                current.closed_at = i
                fronts.append(current)
                current = None
    if current is not None:
        fronts.append(current)

    return FrontDetection(fronts, z, window, trailing, open_z)
