# THE RESCAN — re-crystallization under a new instrument
### connectome design v0.3 · strictly additive to v0.1 (the render) and v0.2 (the slide rule, the stability law, the Carmack layer, the finder seam, the provider seam)
**2026-09-01 · Bo Chen with Claude (Fable 5.1), CALIBRAN lineage · Register: DERIVED / SPEC / BET with kills; [M] only where a receipt exists.**

---

## 0 · One breath

Models get smarter every few months; the window has sat near a million tokens for a long time; the corpus is larger than the window and grows; and the human memory that wrote it has a sliding window of its own. So the question is not "how do I re-read everything with the new model" — you cannot afford to and it cannot fit — but **"how do I hand a new instrument the *structure* of what I know, so it can attend surgically and give me the sharpest articulation, and tell me what it changed?"** The estate already legislated the answer in two sentences it wrote for other reasons: *the reasoning model is a dated instrument; a model-version change is a journal event like a source change* (CORTEX V5 §12.2), and *the negatives are forever; the prints are versioned; better scanners rescan* (Scriptorium's version law). v0.3 is the rescan: scope a topic through the field, hand the model a **skeleton** (structure and pointers, not text), let it **attend** through read plans under a budget, **reproject** its articulation against every view of the topic so that what it cannot explain is read next, and ship the result with its **vintage and its diff**. The Gaussian-splat analogy is not decoration here: every document is a camera view of the topic, not every view is accurate, and the sharpest articulation is the scene that explains the most trustworthy views at the least residual. Nothing is re-read that the residual did not ask for.

## 1 · The problem, stated so it can be solved

A topic T (say FUSOR) is spread over N documents written at times t₁…t_N with instruments M_{t} of rising quality, in inconsistent directions: some re-derive, some drift, some retell, some refute. Measured tonight in the field's markdown roots alone: **242 chunks in 86 documents (102k tokens) mention FUSOR, plus 1,109 transcript messages in the last thirty days** — and those roots are a subset of the estate. A new instrument M* arrives with window W ≈ 10⁶ tokens and a price. Wanted: A*(T), the sharpest articulation of T under M*, at cost ≪ |T|, repeatable at every M*, with the guarantee that **nothing that was ever established is silently lost** — including the things *you* forgot, because your own window slid.

Four kinds of view sit in every topic, and recency sorts none of them correctly:

| view | what it is | how it is recognized structurally | what the rescan does with it |
|---|---|---|---|
| **aged-out, critical** | an early claim that later documents stopped citing but never refuted | high early corroboration, no recent citation, no supersession edge, no contradiction | surfaced as **forgotten** (§6) and offered to the instrument as a candidate to restore |
| **new, wrong direction** | the latest document goes somewhere the corpus does not support | high novelty residual, low corroboration, lone source, no receipt | admitted as a **branch** with its evidence count; never the articulation's spine until corroborated or receipted |
| **retelling** | the same claim re-derived or copied | cosine ≥ 0.97 (the retellings slice) or identical claim key | collapsed to one view with a multiplicity count; adds no weight |
| **contested** | two sets of claims that conflict and neither was retired | contradiction arithmetic (same subject and predicate, opposite polarity, different times) with no funeral edge | both sides presented with their evidence and timeline (Scriptorium's contradiction dossier); the instrument may adjudicate *with a stated reason*, marked narrative |

## 2 · The splat, taken literally

3-D Gaussian splatting fits a scene to photographs by **reprojection error**: render the scene from each camera, compare to the photo, move the primitives, add primitives where the error is high, drop the ones that never help. Inaccurate photographs are handled the same way as accurate ones — they are just views that the consensus scene cannot explain, and they end up down-weighted. Transported:

- **the scene** = the articulation A(T): a set of claims, each with polarity, time-of-first-establishment, and span citations;
- **a camera** = one document (or one session transcript), with a pose: its instrument, its date, its trust tier, its lane;
- **rendering A from a camera** = listing what A implies that document should contain;
- **the residual of a view** = the claims in the document that A does not contain (omission) plus the claims in A the document contradicts (conflict);
- **densify** = read the spans behind the high-residual claims and revise A;
- **prune** = a view whose residual stays high after reading is an outlier — kept, listed, reasoned about, never silently dropped.

The **accuracy ladder** that decides which views the scene should explain is the estate's claim grammar, mechanized: receipt-closed claims (a span on the tape closes them) > independently corroborated claims (≥ 2 sources under the independence key) > supersession-aware recency (a later document that *names* what it retires outranks an earlier one; a later document that merely differs does not) > lone narrative. Retellings are weightless. This is why "the latest is best" is wrong and "the earliest is wrong" is wrong: the ladder sorts by evidence, and time enters only through explicit supersession and the Chronicle.

## 3 · The organs the estate already built for this

- **CORTEX's Chronicle** (§3.10): the ordered fold with a chronological pass, a reverse-chronological pass, and one disconfirming pass whose divergence measures how much the prior bent the reading — the rescan runs all three over the topic.
- **The Choir** (§8.5): K seats on deliberately different footings — one on the topic's gists, one on the Chronicle, one on the Atlas's bright cells — **and one contrarian seat footed on the complement**: the lowest-salience, oldest, never-cited chunks. That seat is where the aged-out critical insight lives, and it exists precisely because the other seats will not look there.
- **Reconsolidation** (§8.7): a drill that finds what a gist omitted re-folds that gist first. The rescan's residual loop is reconsolidation at topic radius.
- **Instruments with vintages** (§12.2) and **one CORTEX, revisions and vintages never editions** (A7): the articulation is a vintage of the topic, not a new topic.
- **Scriptorium's second reading to a fixed point** (P3 ⇄ P4 until churn < 2%) and its contradiction dossiers (both sides, never resolved by the machine).
- **The connectome's own store** (v0.2): communities, bridges, retellings, succession, transcripts with vectors, lane volatility.

## 4 · The mechanism — `refold --topic T --instrument M*`

1. **Scope.** Seed = query embedding of T ∪ lexical hits ∪ the topic's communities; expand one hop through semantic and document edges; collapse retellings; attach the Chronicle order. Output: the topic subgraph — chunk ids, documents, dates, communities, bridges in and out of the topic. Gear one, free, milliseconds.
2. **Skeleton.** A compact object (≤ 30k tokens, structure and pointers only) the instrument reads first:
   - the topic's communities and their labels; the timeline with era change-points; the documents in order with their trust tier and instrument-of-origin;
   - the **claim table** (where cards exist): claim key, polarity, first seen, last cited, corroboration count, trust, status ∈ {standing, retired-by-funeral(date, by), contested, lone};
   - the **retellings** (multiplicities), the **bridges** (what this topic touches outside itself), the **forgotten** (§6), the **dark matter** (chunks in the topic no synthesis ever cited);
   - a pointer for every row: chunk id → path, section, span.
3. **Attend.** The instrument requests spans through `recall` under a token budget (the anytime dial: skeleton only → cited spans → deliberate → exhaustive). The Choir's seats run as separate requests with separate footings; the contrarian seat's budget is reserved, never optional.
4. **Splat.** The instrument writes A(T) as claims with citations. The organ **reprojects**: for every view in the topic, the omission and conflict residuals against A; the highest-residual spans go back to the instrument; repeat until the residual mass falls below the bar or the budget is spent. The residuum ships as a **lower bound** (Chao, as CORTEX §6.6): "at least X claims in this topic were not integrated."
5. **Vintage and diff.** A(T) carries `{instrument, corpus generation, tokens read / tokens in topic, residuum lower bound, outliers with reasons, spent}`, and a structural diff against the previous vintage of A(T): **claims added, retired, re-worded, re-ranked** — the answer to "what did the smarter model change?" The diff is the product; the articulation is one print of it.

Everything above the skeleton is narrative and never closes a claim; every claim in A cites spans that the fence can check; an articulation that cites nothing is a draft, not a vintage.

## 5 · Why this is not "read everything"

Reading FUSOR's markdown chunks once costs 102k tokens; with the transcripts, several times that; the estate's full corpus, orders of magnitude more, and the window does not fit it. The skeleton costs ~30k tokens and is computed by gear one once per corpus generation, reused across every instrument. The reads are chosen by residual, so the spend goes where the articulation is wrong, not where the corpus is long. Expected: a FUSOR rescan at 30k skeleton + 100–200k spans ≈ $0.03 on Flash, a few dollars on a frontier lane — repeatable at every release. The economy is structural, not a discount: **structure is computed once locally; judgment is rented at the margin.**

## 6 · The forgotten organ — what you used to know

The human sliding window is the part no memory tool addresses, and the field can address it by arithmetic: a claim with high early corroboration, cited by nothing recent, with no supersession edge and no contradiction, is **forgotten, not retired**. `forgotten --topic T` lists them with their last citation date and their spans. In the skeleton they are a first-class row; in the Choir they are the contrarian seat's footing; in the render they are the nodes drifting inward that nothing has touched. The falsifier is F-FORGOTTEN: plant aged-out claims in a synthetic topic and require the organ to surface them ahead of a recency null.

## 7 · Does this warrant a version three?

No rewrite; yes, a version. v0.3 is additive: the architecture (field over tape, seven slices, communities, layouts, the residual gate, the two gears) stands; the rescan adds **a use case with its own loop and three new store requirements** — the claim table with polarity and time (from cards, gear two), **supersession edges** (a document that names what it retires: detectable by citation of an earlier claim key with flipped polarity, or by the estate's own printed funerals), and a **citation ledger** (which syntheses cited which chunks, when — the substrate of "forgotten"). Those are columns and one verb, not a new organ family. The name stays: **connectome**.

## 8 · Falsifiers added in v0.3

| name | claim | null | it loses if |
|---|---|---|---|
| **F-SKELETON** | skeleton + residual-chosen spans recovers planted claims of a synthetic topic at ≥ the recall of reading everything, at ≤ 1/10 the tokens | read-everything; top-k retrieval only | recall below the null at matched tokens — the structure bought nothing |
| **F-VINTAGE** | a newer instrument's articulation of the same topic beats the older instrument's, blind-rated by the operator on the same spans | the older articulation | no preference — "smarter" bought nothing for this topic, printed |
| **F-FORGOTTEN** | planted aged-out claims surface ahead of a recency null | recency ordering | they do not |
| **F-OUTLIER** | a planted wrong-direction document is listed as an outlier with a reason, and a planted aged-critical document is restored | no reprojection | either arm fails |
| **F-BRANCH** | contested claims appear with both sides and their timelines; the machine never resolves them silently | single-answer synthesis | a contested claim appears one-sided without a stated adjudication |
| **F-DIFF** | the vintage diff is structural and near-empty when the corpus and instrument are unchanged | prose diff | thrash without new evidence |

## 9 · Ladder deltas

- **R1 (now):** `dossier --topic T` — the skeleton at gear one: subgraph, timeline, documents with dates, retellings collapsed, bridges, dark matter, a read plan; no cards yet, so no claim table.
- **R4 (cards, gear two):** the claim table, supersession edges, the citation ledger; `forgotten`.
- **R5 (tools):** `refold` as an MCP flow — the instrument calls `dossier`, then `recall` under budget, then `reproject(A)`; the organ keeps the vintage and prints the diff.
- **First real run:** FUSOR, under the instrument that wrote most of it and under the next one, blind-rated by you. That run is F-VINTAGE.

## 10 · What is not claimed

Nothing in v0.3 has run except the topic census. Reprojection over claims needs cards, which need gear two, which needs the operator's word per spend. The splat analogy is exact at the level of residual-driven fitting and inexact at the level of geometry (documents have no pose in the camera sense; their "pose" is instrument, date, trust). The forgotten organ is arithmetic over a ledger that does not exist until syntheses cite chunks by id, which the unit map now does — so the ledger begins tonight, empty.

*A new instrument does not re-read the world; it reads the map, asks for the places the map cannot explain, and prints what it changed. — for the red pen.*
