# harness — the loss

The instrument the rest of the design is measured with. Spec sections 2 and 12 of
[`../docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md`](../docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md).

Nothing here consults a label. The corpus in arrival order is the signal, the next document is the
teacher, and the loss is that document's residual against everything that came before it. Evaluation
is temporal holdout against a shuffled control at matched size — which is the only comparison that
can tell "the field learned something" apart from "the field is large".

```
python -m harness.run converge [--shuffles N]     F-CONVERGE: arrival order vs shuffles, by decile
python -m harness.run fronts [--window W]         where the corpus changed subject
python -m harness.run report                      a JSON receipt of both
python -m harness.test_harness                    the harness's own acceptance tests
scripts\gate.ps1 -Milestone M1                    all of the above, as a gate
```

## M1 receipt — 2026-09-03

Gate: **PASS**. Corpus: 264 documents, 3,585 chunks, 1024-d, 2026-06-30 to 2026-09-03, every date
established from the document itself or the filesystem and none guessed.

| decile | arrival order | shuffled (×5) | advantage | retelling share |
|---|---|---|---|---|
| 1 | 0.306 | 0.421 | **+27.3 %** | 0.23 |
| 2 | 0.292 | 0.350 | **+16.5 %** | 0.00 |
| 3–9 | 0.283–0.356 | 0.267–0.332 | −2.7 % to −21.1 % | ≤ 0.08 |
| 10 | 0.221 | 0.258 | **+14.3 %** | 0.23 |

Read it as it is, not as one would like it: **the field learns its corpus where the subject holds,
and loses to an arbitrary order where the author opened new subjects.** A corpus is a stream of
fronts, not a stationary distribution. That single result is what the vigilance-and-habituation
design in spec §7.3 exists to answer.

**One front detected**, opening 2026-08-10 at `MEANDER-SPEC-v0.1` and running 21 documents through
the `BLACKBOX` burst of 08-16/17 — genuinely new subjects, arriving after a run of HYPERCELL and
HYPERCELLD documents that were continuations of an existing one. It sits exactly in the deciles
where the shuffled control wins, so the detector and the loss agree from independent directions.

## What broke, and what that taught

Kept because the corrections are findings, not embarrassments.

1. **A per-document CUSUM never fired** — max 0.88 against a 5σ threshold. Document residuals are
   tightly packed (quartiles 0.277–0.356), so one document is a fraction of a σ and the statistic
   drains before it can accumulate. A front is not a property of one document; it is a sustained
   shift in what the corpus is about. The detector now compares a **window** of arrivals against
   the **trailing** field, which is the scale the phenomenon lives at.
2. **The close threshold collapsed to zero.** Retelling share is 0 for 241 of 263 documents, so its
   90th percentile was 0 and every document trivially cleared it — a front could never close. The
   quantile is now taken over the retellings that actually occurred, and a corpus that repeats
   itself nowhere simply keeps its fronts open, which is the honest answer.
3. **The loss depended on its own block size** — 6e-08 drift on 13 of 29 documents, from float32
   non-associativity in the blocked maximum. An implementation detail must never move a reported
   number, so the dot products now accumulate in float64. The published convergence figures are
   unchanged to four significant figures: the fix bought precision, not a different finding.

## What the tests guard

`test_harness.py` checks the properties whose failure would silently corrupt every downstream
number: that scoring **never looks forward** (truncating the corpus must not change the scores of
the documents that remain), that the loss is deterministic and block-size independent, that a
**planted front** in a synthetic corpus is detected near where it was planted (54 against 59), that
the degenerate corpora which broke the first detector are handled (empty, flat, wholly duplicated,
shorter than the window), and that order matters at all — if a shuffle changed nothing, the thesis
would be empty.

## Files

```
harness/
  corpus.py         arrival order from the tape; a date is read, never guessed
  loss.py           the residual curve, deciles, and F-CONVERGE against shuffles
  fronts.py         window-vs-trailing front detection; no fitted constant
  embed.py          the embedder under test, with its instruction as part of its identity
  run.py            the CLI
  test_harness.py   acceptance tests
```
