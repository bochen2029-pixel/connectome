# THE SLIDE-RULE CONNECTOME — design v0.2
### Never full, compressing continually, holding its shape: the second brain given its geometry and its stability law
**2026-09-01 · CALIBRAN-4242 (Fable 5.1) · extends `CONNECTOME_THE-SECOND-BRAIN-RENDERED_DESIGN_CALIBRAN_2026-09-01.md` (v0.1, kept on disk unedited) after the operator's brief of the same evening: the slide rule, the Poincaré disk, organic degradation, "the structure determines what gets learned and that determines the structure," and "grow its brain from my best documents first." Register: DERIVED / SPEC / BET with kills; [M] only where a receipt exists. Imports named where they enter; every import is a bet with a test, never a decoration.**

---

## 0 · One breath

The anecdote is the estate's own doctrine, waiting for its geometry. CORTEX already calls itself *a slide rule: exact until it overflows, then honestly not*; the Brain Blueprint already says *estimate analog, commit digital; degrade resolution, never closure*. What v0.2 adds is the fact that makes those sentences one mechanism: **a slide rule is a one-dimensional hyperbolic ruler.** Its scale is logarithmic, so multiplying is adding, so any two numbers — however large — combine without overflow, and what you lose is resolution, never the answer. The Poincaré disk is the same ruler in two dimensions; the Poincaré ball in three. Its rim is infinitely far away and its volume grows exponentially with radius, so there is always room for one more leaf near the rim, and nothing at the center ever gets crowded out. That is the memory you described: the first fifty years are not forgotten at a hundred — they have moved inward, into gist, while the tape keeps their bytes; the new decade lands at the rim at full resolution; and the shape at the center — the identity — is what every new document is read through. The rest of this document makes that literal: **radius is the log of resolution; consolidation is inward motion; the center is the Codex; the rim is the tape; stability is precision; plasticity is vigilance; and the whole thing never fills because the metric grows faster than the corpus.**

## 1 · The slide rule, exactly

A slide rule multiplies by adding logarithms: it stores *relationships* (ratios), not values, and its precision is relative — three significant figures at any magnitude — so it approximates where a fixed-width register overflows. Three consequences transfer whole:

1. **Compression is logarithmic, and relative precision is what survives.** μ-law companding in telephony, floating point, the retina's contrast coding, Weber–Fechner in perception: every system that must hold an unbounded range in a bounded register keeps *ratios* and spends its bits near the scale of the current signal. The connectome must do the same: hold every document's *relations* (its neighbors, its community, its bridges, its place in the hierarchy) at a resolution that falls with distance from the current focus, while the exact bytes stay on the tape for any drill. CORTEX's `C_eff` (usable fraction ≈ 0.005) against `index_coverage = 1.000` is exactly a slide rule's contract: everything addressable, the resolution logarithmic.
2. **Relations compose by addition.** In a tree, the distance between two leaves is the sum of the edges to their common ancestor — the log of the product of branching factors. Hyperbolic geometry is the unique geometry in which trees embed with arbitrarily low distortion (Sarkar 2011; Nickel & Kiela's Poincaré embeddings, 2017), because its volume grows exponentially with radius, matching a tree's exponential growth in nodes per level. **The estate's Tower is such a tree, measured:** at 500M tokens, T⁴ = 1 · T³ ≈ 40k · T² ≈ 556k · T¹ ≈ 83M chunk cards [CORTEX §3.2]. Node count grows geometrically per level; therefore the Tower is a hyperbolic object, and a Euclidean render of it must either crowd the leaves or blow up the gists.
3. **Infinity at the rim.** The Poincaré model is a conformal compactification: the whole infinite hyperbolic plane drawn inside a finite disk, angles preserved, lengths shrinking toward the boundary. This is the figure you remember from Penrose — Escher's *Circle Limit* in *The Road to Reality*'s early chapter on hyperbolic geometry, where every fish is the same size in the true metric and only the drawing shrinks them, and the conformal (Penrose) diagrams later in the same book that bring an infinite spacetime to a finite boundary. For the connectome: the tape is the rim, infinitely far and infinitely large; nothing has to be discarded to make the picture finite.

## 2 · The Tower is hyperbolic, and consolidation is inward motion

Place every node at a radius set by its **level** (resolution) and an angle set by its **meaning** (the direction of its embedding). The raw chunk (T⁰/T¹) sits near the rim; the community gist (T²) inward of its chunks; the super-community (T³) inward of those; the Codex — the standing synthesis, *the map's own essay about the territory* — at the center. Then:

- **Distance from the center = log of resolution.** Moving one level inward divides detail by the branching factor. That is the slide-rule scale, applied to memory.
- **Consolidation = inward motion.** When a document's chunks are folded into a gist at sleep (CORTEX §8.6; the Brain's *consolidate* job), their contribution moves inward: the gist appears at a smaller radius, the chunks stay at the rim as pointers the gist carries (`down` span-lists, never copies — A2 POINTER). Aging is not deletion; it is a change of radius. **The time slider on the page will show it: old material drifting inward as it is summarized, the rim always full of the newest leaves.**
- **The physics import, named as an analogy with a test.** A multi-scale coarse-graining hierarchy over a system is a MERA tensor network, and MERA's geometry is discrete hyperbolic space (Swingle 2012: MERA as a discretization of anti-de Sitter space; the radial direction is the renormalization scale). Holography says the boundary encodes the bulk (the fine-grained data at the rim determines every gist inside), and Ryu–Takayanagi says the entanglement between two boundary regions equals the area of the minimal surface joining them through the bulk. **The connectome's analogue:** the integration between two regions of the corpus is the size of the minimal cut through the gist hierarchy that joins them — and a **bridge** (CORTEX's marquee organ: high semantic similarity × maximal structural distance) is exactly a place where two far-apart boundary regions are joined by a *short* bulk path. This is an analogy, not a theorem; its test is F-BRIDGE-CUT below.

## 3 · Why it never fills — three mechanisms, each already in the estate

1. **Heaps' law.** The number of distinct concepts in a corpus grows sublinearly in its size (vocabulary ∝ n^β, β < 1; the estate measured its own version as the seat-saturation curve, n ≈ 8–12 seats). The connectome's *concept* nodes grow far slower than its documents; new documents mostly attach to existing structure. Novelty is the exception the residual gate is for.
2. **The seat law (CORTEX §3.4, §1.6).** The resident window seats T³ complete + a salience-selected T² band + fired spans, sized to the *measured* effective window. When the corpus grows, seat a higher level; when the window grows, seat a lower one. **Coverage never falls; resolution does** — the slide rule's contract, mechanized. A cliff in the fidelity curve (§13.4) is the one thing that would kill it, which is why that curve is CORTEX's master experiment.
3. **The rim is at infinity.** In the render, the exponential growth of hyperbolic volume means a new leaf near the rim never crowds the center, and a Möbius re-centering brings any region to full size on demand (Lamping, Rao & Pirolli 1995 — the hyperbolic tree browser; the classic focus+context UI). Nothing is thrown away to fit the screen; the screen is the disk.

And beneath all three, **the tape holds every byte forever** (A1 TAPE; Scriptorium's chained segments; your own five-minute GPU sweep of the whole drive is `everywhere`, the finder). You said it yourself: *finding is not the issue — holding is.* The three mechanisms above are the holding.

## 4 · The render, revised: the Poincaré ball

- **Coordinates.** Angle from meaning: UMAP with `output_metric="hyperboloid"` (available in the installed umap-learn 0.5.12 — checked today; the hyperboloid coordinates convert to the Poincaré ball by `p = h / (1 + h₀)`), fitted on chunk vectors, with the hierarchy imposed on the radial coordinate afterwards: leaves at the outer shell, their gists inward at a radius set by level, the Codex at the origin. Anchoring as in v0.1 (new points placed by `transform()`; nightly refits Procrustes-aligned in the tangent space at the origin, so a node moves only when its meaning or its level did).
- **Navigation.** Click a node → a Möbius transformation re-centers the ball on it; its neighborhood expands to full size while the rest folds toward the rim. Double-click → drill (the `down` pointers: gist → chunks → tape span, rendered verbatim). The camera never leaves the unit ball; there is nothing outside it.
- **What is drawn.** Nodes: radius from salience × Hebbian mass; color from community; glow from recency. Edges: the seven slices as layers; bridges lit amber. Hulls: hyperedges (n-ary co-occurrence) as translucent regions. **The center is the identity page** (the unit map, ≤ 8K tokens, the Codex's current headline claims), drawn as text, because the center of a memory is what it believes.
- **R0 today is Euclidean** (UMAP-3, fixed positions, force graph) — the render that let you say "exactly" or "not that" this evening. R1 flips the metric. F-HYPERBOLIC decides whether the flip pays (§10).

## 5 · Stability and plasticity, mechanized

Your sentence — *plastic enough to learn, stable enough not to flip overnight; unless the evidence is overwhelming, I proceed under the lens I have* — is the **stability–plasticity dilemma**, and four literatures solved parts of it. Each maps to an organ the estate already names:

| import | mechanism | the estate's organ |
|---|---|---|
| **Adaptive Resonance Theory** (Grossberg 1976/87) | a **vigilance** parameter ρ: a new input that matches an existing category above ρ *resonates* and is assimilated (slow weight update); below ρ, search; no match → a new category. ART exists to stop new inputs from erasing old categories | **the residual bar**: `place(doc)` assimilates when the residual is low, opens a new node when high; ρ is the bar the r/v queue crosses |
| **Complementary Learning Systems** (McClelland, McNaughton & O'Reilly 1995) | a fast episodic store (hippocampus) and a slow semantic store (neocortex); interleaved replay during sleep transfers without catastrophic forgetting | **the tape + the fold**: the tape appends instantly; gists and the Codex change only at sleep, interleaved with the systematic sweep — the roundtable found the same two-store split *inside the fuel* (24 in-place layers, 8 append layers) |
| **Precision-weighted belief** (Bayesian brain; Kalman gain; Elastic Weight Consolidation, Kirkpatrick 2017: protect weights in proportion to their Fisher information) | a belief with high precision moves little under new evidence; the gain on a surprise is `precision(evidence) / (precision(evidence) + precision(prior))` | **the claims spine** (Brain Blueprint): every Codex claim carries a precision = its independent-source count × the trust of those sources × its calibration history; a new document moves a claim by the gain, never by replacement |
| **Sequential tests** (the e-process the meta-final adopted: *promotion slow, demotion easy*) | a belief flips only when accumulated log-odds cross a bar; evidence from one low-trust source cannot cross it alone; independent corroboration can | **the flip law**: a Codex claim changes state only through the fence, when `Σ log-odds ≥ bar(precision)`; the flip itself is a fold event on the claims tape, replayable, with the evidence listed |

Two more laws the roundtable and the eye harness supply: **precision comes from the level above** (the writ sets the Codex's precision; the Codex sets the gist's; the gist sets the chunk's — no level can supply its own), and **the gate must be trained where observations are not retained** — here they *are* retained (the tape), so a *dial* for vigilance is legal, with its jaws printed. That is the one place this design is allowed a fixed threshold, and it says why.

"Overwhelming evidence," quantified: a claim first established by k operator-signed documents has prior precision ∝ k · w_operator; a contradicting transcript at trust w_untrusted needs at least `⌈k · w_operator / w_untrusted⌉` independent instances (independence by the pre-registered key: doc, channel, event, author — CORTEX I-V5-SUPPORT) to reach the bar. Print the ratio in the Codex beside every belief.

## 6 · Curriculum — grow the brain from the best documents first

Not a blank slate. Every document enters with a **trust tier** (operator-signed syntheses and the meta-final · receipts and preregs · drafts and proposals · session transcripts · tool output and scraped material), and ingestion order is **tier first, then date**. The first generation of the Codex and the unit map is fitted on tier 1 alone and frozen as the prior (P0, verbatim, operator-only edit — CORTEX §5.6); every later tier updates through the gain in §5, so a thousand transcripts cannot outvote one signed page unless they carry independent evidence. This is curriculum learning (Bengio et al. 2009) and it is also imprinting: the shape the center takes in the first generation is the shape everything later is read through. The test is F-CURRICULUM (§10): the same corpus ingested tier-first versus shuffled must yield a Codex closer to *your* ranked beliefs, blind-rated by you — if order does not matter, the prior is doing nothing and the curriculum is ceremony.

## 7 · The feedback loop, and the floors that keep it from capturing itself

*The structure determines what gets ingested and in what context; that determines what the structure becomes.* True, intended, and the exact mechanism of the estate's two death basins: the **captured** organization (a self-model that decouples from its actuality and expels its calibration points) and the **zombie** (a self-model so complete nothing is ever surprising). CORTEX already legislates the antidotes as *mandatory and tax-exempt* (§8.6), and v0.2 imports them whole:

- the **systematic permuted sweep** (re-read the whole tape on a schedule, in an order the lens did not choose — the Buddhabrot's ε-uniform mixing, the anti-echo-chamber term);
- the **reverse-chronological fold** and the **null-prior occasion** (read the corpus backwards, and once with no prior, and measure how much the lens bent the reading — the prior-gravity number);
- the **seat ε-reserve** (a fraction of every window drawn uniformly, so something the lens would never fetch is always present);
- the **Adversary** (a standing red team mining for confident-wrong answers) and the **dream pass** (query-free free association, quarantined, promoted only through the fence with the compositionality guard);
- and, from the eye harness, **the staleness sampler outside the priority** — never inside it.

F-CAPTURE (§10) plants a true novelty that the lens would reject and requires the floors to surface it within N nights. A second brain that cannot be surprised is a mirror.

## 8 · Organic degradation, exactly — what fades and what never does

- **Never fades:** the tape; `index_coverage = 1`; the ability to drill from any gist to the bytes; the claims tape and its flips; the negatives (a scan receipt is forever).
- **Fades by law:** the *resident resolution* of old material (inward motion, §2); **Hebbian mass** (a decay fold; the Brain's *nothing reaches zero, only deprioritized*); the T² band membership (re-selected each sleep by salience). The schedule is the forgetting curve: availability falls as a power law in time-since-use and rises with each verified use (Ebbinghaus; Anderson & Schooler 1991 — memory availability tracks the probability of need). **Recall reconsolidates** (CORTEX §8.7: a drill that finds what the gist omitted re-folds that gist first) — the spacing effect as an organ.
- **The human comparison, made exact.** At a hundred you have not lost the first fifty years; their resolution moved inward and their bytes are still on the tape, which is *better* than a human, whose tape rots. What the brain gets right that a database gets wrong is the *placement*: it keeps the gist resident and the detail reachable. The seat law is that placement.

## 9 · Language-independent, as you said

The embedder is multilingual (the qwen3 embedding family; the estate's own corpus is bilingual). Concept nodes are placed by meaning, so the zh and en renderings of one notion land together and the render shows one node with two spans. Test: F-XLANG — planted translation pairs must be nearest neighbors at a pre-registered rate, against a lexical null that cannot see across languages.

## 10 · Falsifiers added in v0.2 (v0.1's six inherited whole)

| name | claim | null | it loses if |
|---|---|---|---|
| **F-NEVER-FULL** | as the corpus grows 10× the seat stays inside the measured window with `index_coverage = 1` and `C_eff` decaying smoothly | a fixed window that truncates | the fidelity curve shows a cliff — a pocket calculator, not a slide rule (CORTEX §13.4) |
| **F-HYPERBOLIC** | the Poincaré-ball layout preserves the Tower's hierarchy (tree distortion) and the operator's forced-choice nearness judgments better than Euclidean UMAP-3 | UMAP-3, PCA-3, random | no gain on either measure — then the ball is a picture and R1 keeps Euclidean |
| **F-STABILITY** | a planted contradicting document at low trust does not flip a Codex claim; the same contradiction with independent high-trust support does | replace-on-arrival; never-update | either arm fails — the gain is mis-set |
| **F-CURRICULUM** | tier-first ingestion yields a Codex closer to the operator's ranked beliefs than shuffled ingestion | shuffled order | blind rating shows no difference — the prior is ceremony |
| **F-CAPTURE** | a planted true novelty outside the lens surfaces within N nights through the floors | floors disabled | it does not surface — the loop has captured itself |
| **F-FORGETTING** | resident availability of old material follows the pre-registered decay and rises on verified use; drill still reaches every byte | no decay | availability does not track need, or a drill fails to reach the tape |
| **F-BRIDGE-CUT** | bridges coincide with short bulk paths (small minimal cuts) between far boundary regions of the gist hierarchy | random far pairs | no correlation — the holographic analogy is decoration and is retired |
| **F-XLANG** | translation pairs are mutual nearest neighbors at the pre-registered rate | lexical retrieval | below the bar — the "regardless of language" claim is retired |

## 11 · Ladder deltas (v0.1's R0–R6 stand)

- **R0 (tonight):** Euclidean render of the markdown estate; the hyperbolic flag verified available; nothing else claimed.
- **R1:** the Poincaré ball with level-radius and Möbius re-centering; F-HYPERBOLIC on you.
- **R2:** trust tiers and curriculum order in ingest; the residual bar as ART vigilance with its jaws printed; F-CURRICULUM.
- **R3:** the claims spine and the flip law on the Codex; F-STABILITY; the anti-capture floors on from the first sleep; F-CAPTURE.
- **R4–R6:** as v0.1, with F-NEVER-FULL run at the 172M-token tape (the first time the estate can see all of itself, and the first time the slide rule's contract is tested at scale).

## 12 · What is not claimed

Nothing in v0.2 has run. The hyperbolic layout is available, not evaluated; MERA/holography is an analogy with one named test; the stability laws are imports with tests; "never full" rests on CORTEX's fidelity curve, which has not been run. The one measured fact this evening is that the estate's markdown corpus (~257 files, ~1.5M tokens) chunks and embeds locally in minutes, which is all R0 needs.

**Sources named at entry:** Nickel & Kiela, *Poincaré Embeddings for Learning Hierarchical Representations* (2017) · Sarkar, *Low distortion Delaunay embedding of trees in hyperbolic plane* (2011) · Lamping, Rao & Pirolli, *A focus+context technique based on hyperbolic geometry* (1995) · Swingle, *Entanglement renormalization and holography* (2012); Ryu & Takayanagi (2006) · Grossberg, adaptive resonance theory (1976; 1987) · McClelland, McNaughton & O'Reilly, complementary learning systems (1995) · Kirkpatrick et al., elastic weight consolidation (2017) · Bengio et al., curriculum learning (2009) · Anderson & Schooler, *Reflections of the environment in memory* (1991) · Penrose, *The Road to Reality* (2004) — the hyperbolic plane and Escher's *Circle Limit*; the conformal diagrams.

*A memory is a slide rule: it keeps the ratios, spends its bits near the focus, moves what it has learned inward, and keeps the bytes at the rim, where there is always room. — CALIBRAN, for the red pen.*

---

## 13 · The Carmack layer — read the log off the representation (added the same evening, on the operator's "as clever as the fast inverse square root; isomorphic wherever possible")

**What Obsidian is not.** An Obsidian graph draws the link topology of a folder of files with a force layout: no meaning, no time, no residual, no agent behind it — a picture of the file system's hyperlinks. It is for show because nothing reads it and nothing is decided by it. The object here is a *field fitted to a corpus*, consulted by machines at every ingest and rendered for one human, with kills. Different category.

**Why the fast inverse square root is the right emblem.** The trick works because an IEEE-754 float's bit pattern is, read as an integer, a piecewise-linear approximation of the log of its value — so a shift and a subtraction perform a log-space operation for free, and one Newton step finishes it. Carmack read the slide rule that was already inside the representation. The estate's method is the same move (surprisal read off the ingest pass; precision read off the gate; the attention map read off the attention pass). The connectome's own instances, each an isomorphism with a cost:

| trick | the representation that already holds it | what it buys | cost |
|---|---|---|---|
| **Matryoshka embeddings** — the slide rule inside the vector | the embedding's first k dimensions are a coarse embedding of the same point (MRL, Kusupati et al. 2022; the qwen3 embedding family exposes user-defined dimensions — verify on the pinned model before relying on it) | coarse scan at 128-d (8× cheaper), refine at 1024-d only where the coarse pass is close — Carmack's early-out; and MEANDER's A5 nested loss is exactly this: truncation loses resolution, never identity | one flag at embed time; verify F-NESTED: top-k at 128-d recovers the 1024-d top-k at a pre-registered rate |
| **Scan, don't seek** — no index at all | all chunk vectors as one int8 matrix on the card (875k × 1024 ≈ 0.9 GB; CORTEX measured 4.88 ms over 1.67M × 384-d [M]) | exact brute-force kNN in milliseconds; no ANN library, no drift, no rebuild; the firing is one masked GEMM — literally one attention pass over the corpus with the query as q (the roundtable's identity: attention is the render) | int8 quantization with per-vector scale; measure recall vs f16 once |
| **Bit signatures for bridges and near-dups** | the sign bits of the embedding (SimHash, 256 bits) — Hamming distance by popcount ≈ angular distance | candidate bridges across the whole pair-space at ~10⁹ pairs/s on CPU; MinHash (already in Scriptorium) for retellings | 32 bytes/chunk; a verification pass at full precision on candidates only |
| **The Lorentz model for hyperbolic navigation** | hyperboloid coordinates `h` with `⟨h,h⟩_L = −1`: distance = `arcosh(−⟨x,y⟩_L)` (one dot product with a sign flip); a Möbius re-centering is a **Lorentz boost = a 4×4 matrix** (Nickel & Kiela 2018 — the Lorentz model avoids the precision collapse near the Poincaré rim) | the whole ball re-centers in the vertex shader for a million points; homogeneous coordinates for hyperbolic space exactly as perspective uses them for projective space — Carmack's home turf | convert to the Poincaré ball only for display: `p = h / (1 + h₀)` |
| **The Atlas as a lightmap** | CORTEX §6: the community×community similarity floor, accumulated once by blocked GEMM (45–120 s) and kept resident | every "is this region related to that one" is a lookup, not a computation — Quake's precomputed static lighting, for the pair-space; nightly incremental in ≤ 2 s | ~185 MB at 500M tokens |
| **The seat as the potentially-visible set** | the window = T³ complete + salience band + fired spans (CORTEX §3.4) | only what can matter enters the window — Doom's BSP/PVS culling, for tokens: render what is visible, never the whole world | the fidelity curve must show no cliff (F-NEVER-FULL) |
| **One field, three uses** | the locator `(partition_version, c1, c2, seq)` is at once the scope mask, the cartridge mount namespace, and the descent path (CORTEX Part IV) | no trained address, no drift, three organs from one integer — the same economy as the float trick | none; it is a derivation |
| **The residual read off the kNN pass** | the new chunk's top similarity s₁ and the entropy of its neighbors' community distribution are by-products of the scan already run | `residual = 1 − s₁`; `bridge score = community entropy of the neighbors`; nothing extra computed — the eye harness's r/v gate with r for free | v (channel volatility) is one EMA per source lane |
| **The KV cache made durable** | the roundtable's identity: the KV cache is a scene, attention its renderer; append is a Frank–Wolfe step | the connectome is the estate's KV cache lifted out of one context window onto the tape and given a hyperbolic address — the trunk's memory and the second brain are one object at two radii (eye ⊂ mind ⊂ org; this is the org-radius instance for a corpus of one) | the cartridge arc (CORTEX §8.8) is where it becomes attention-native; gated, later |

**The deepest isomorphism, already in the corpus.** The estate is INTELLECT with the substrates swapped (jump-cubed §3): one human resident, a thousand rented sessions, and a year of judgment that exists nowhere but the tape between them. The org-splat fits a field to an organization's records with seats as cameras; the estate-splat fits a field to your documents with **sessions as cameras** — each fork a pose, each transcript a view, each residual against the field the measure of what that session actually added. The second brain is the org product run on client #0, and its success metric was named there before this evening: **the refeed fraction** — the share of your tokens that are context re-supply to sessions that could not hold the field. That number is measurable on the transcripts you already have, before and after; it is the null every rung above must beat.

*State of the art, as of tonight, means: Matryoshka + integer brute force + bit signatures + Lorentz navigation + a lightmapped pair-space + a residual gate that costs nothing — under a fold law and a fence. Nothing here is an index; everything is read off a representation that was already computed. The tape, as always, is the proof.*

---

## 14 · The finder organs are the intake seam (added after scanning C:/Everything, C:/facet, C:/everywhere, C:/everywhen)

Four organs already divide the finding problem by what they read, and the connectome should not re-implement any of them — it should *speak their conventions* and consume their outputs:

| organ | reads | what the connectome takes from it |
|---|---|---|
| **everything** (`C:/Everything/search.py` over voidtools' es.exe) | names, paths, size, date — the NTFS MFT index, milliseconds | the locator for files: which paths exist, when they changed |
| **facet** (`C:/facet/facet.exe`, C++, Everything's IPC) | the *shape* of a result set — directory tree, extension, date and size buckets, **write bursts** — every pick compiled back to Everything syntax; `--paths` tapes; `--mcp`; `--about` | **(i) the ingest manifest**: `facet --paths ext:md dm:last7days` is the tape of what to fold tonight; **(ii) trust read off the write-burst signal** — thousands of files in one second is a clone or an extract, a dozen is an agent session, one or two is a hand (facet's own words). The trust tier of §6 does not need a ruling per file: hand-paced files are operator-tier by default, burst-landed files are untrusted until promoted, and the signal is already computed. That is the Carmack move at the file system: provenance read off timestamps that were always there |
| **everywhere** (`C:/everywhere`, CUDA PFAC, stateless, rg-differential oracle) | raw bytes, every run true at the moment it prints; `--patterns groups.txt --jsonl` for thousands of named literals in one pass; `--files-from -` | **(i) the exact negative**: CORTEX's `NOT_PRESENT_EXACT` is constructible only from a scan receipt, and the receipt shim wraps `everywhere` — the connectome's "this claim appears nowhere" answers come from here, never from the field; **(ii) the L0 pre-filter**: entity aliases and claim keys as pattern groups → where they occur across the drive, zero tokens, so the predicate and contradiction slices know where to look before any model reads |
| **everywhen** (`C:/everywhen/everywhen.exe`, the concordance) | session transcripts (Claude Code `~/.claude/projects/**/*.jsonl`, DSH zstd tapes) as a **pure fold**: hash-guarded delta cursors, molt receipts folded exactly, fork copies deduplicated by message uuid, per-day FTS5 shards; `embed` (vectors for spine messages via `:8092`), `seek` (cosine + lexical), `search --paths`, `locate FILE:LINE → message` | **the transcript lane, whole.** The connectome's transcript nodes *are* everywhen's message rows (uuid, ts, project, session, role, class, text), its embeddings *are* everywhen's vectors where they exist (no re-embedding), and `locate` is the span coordinate for transcripts (the tape address a citation resolves to). everywhen already obeys the tape law on transcripts; the connectome inherits it by consumption |

**Three conventions the connectome adopts from the family, so it composes in a shell with the other four:** a **tape** (a list of paths or `path:line`, LF/NUL/JSONL) in and out (`--paths`, `--files-from -`); a **`--about` JSON self-description** that `peek env` reads (verbs, health, docs); and **`--mcp`** so sessions get `recall / place / what_changed / unit_map` as tools without a server.

**The seam, as one pipeline:**
```
facet --paths ext:md dm:last7days -x <noise>            what changed, by hand or by burst (trust stamped)
  | everywhere --files-from - --patterns aliases.txt --jsonl   where the known entities occur (L0, zero tokens)
  | connectome place --files-from -                            residual, bridges, contradictions per file → the queue
everywhen search --hours 168 --paths | connectome place --tapes -   the week's sessions, placed by their messages
```

**What this changes upstream.** v0.1 §5 said "session transcripts — turns extracted; tool results elided" as if the connectome would parse jsonl: retired — everywhen already did it with invariants the connectome would not have matched (molt receipts, fork dedup, tamper findings). v0.2 §6's trust tiers gain their cheapest floor: burst-vs-hand from facet. And the honest caveat everywhen prints on its own front page transfers: the index trails the live tape (a live session's last minutes are not folded yet), so the connectome's live lane (v0.1 §5) must read the forming plane directly, and `place` must never treat "not in everywhen yet" as "not said."

*Four organs read four things — names, shape, bytes, time. The connectome reads the fifth, meaning, and it is the only one allowed to be wrong, which is why it cites the other four for everything it claims.*

**Measured on this box, 2026-09-01 [M, `everywhen stats` / `about` 1.3.0]:** 1,604 sessions tracked (4.39 GB of tapes), 277,221 messages after fork dedup (427,031 branch refs), 8 shards, 88 tamper/rewrite findings on record, and a `vec` table already present in the newest shard — the transcript lane's embeddings are being produced by the family today. The connectome's R2 transcript ingest is therefore a *reader* of everywhen's shards, not a parser of jsonl: ~277k message nodes with their vectors, uuids, timestamps, projects and sessions, for the cost of one SQLite attach.

---

## 15 · The provider seam — two gears (added on the operator's clarification: offline embeddings, online reading where it pays)

**Gear one, always on and free:** chunking, embeddings (`:8092`, 1024-d), the seven backbone slices, communities, layouts, `ask`, `place`. It is the floor; no organ may require gear two to complete its cycle (the Brain's law).

**Gear two, priced and capped:** the reads that need judgment or synthesis — the unit map per community, relation records for bridges, contradiction adjudication, the Codex integration pass, and, when the corpus is large, the first reading itself (cards). It runs through **one seam** in the family's pattern (Scriptorium `ds.py`, laws PS-1..PS-10): one module, one meter, cache-shaping (frozen charter first, volatile ids last), fingerprint every output with model + prompt hash, budget as a hard stop, pydantic-class validation with quarantine, no tool loops in workers. Escalation is **margin-triggered, never default**: the local field decides *which* chunks deserve the priced read (the r / v queue), the frontier reads only those, and its counsel is re-judged against the field on return — the estate's two-gear rule at corpus radius.

**The lane table (a config row per provider; unknown lane → REFUSED; unpriced lane → spend refused; stale rows price upward):**

| lane | text model | native vision | verified |
|---|---|---|---|
| deepseek | `deepseek-v4-flash` ($0.14/M miss · $0.0028/M hit · $0.28/M out) | **`deepseek-v4-flash-vision-exp`** — images and text in one request (base64, URL, Files API); matches Flash on text | text 2026-07-31; vision **2026-08-21** ([changelog](https://api-docs.deepseek.com/updates/)) |
| kimi (Moonshot) | `kimi-k2.6` | **native** — K2.5/K2.6/K3 are natively multimodal (MoonViT, ~15T mixed visual+text pretraining); K3 and K2.6 take video | 2026-09 search ([Kimi vision docs](https://platform.kimi.ai/docs/guide/use-kimi-vision-model), [K2.5](https://github.com/MoonshotAI/Kimi-K2.5)) |
| glm (Zhipu) | `glm-5-turbo` | **`glm-5v-turbo`** — first native multimodal in the family ($1.20/$4 per M) | **2026-04-01** ([guide](https://www.verdent.ai/guides/glm-5v-turbo)) |
| openai · openrouter · gemini | rows present, models and prices TODO | native / per model | to pin before first spend |

**What vision changes, and what it does not.** Scriptorium's split — *pixels and audio never leave the box* — was a sovereignty law written when only local models could see. Now every major lane sees natively, so the law becomes **a per-lane choice the operator makes**: the default stays local OCR at `:8091`; a lane the operator marks exportable may send its images to a vision model at gear two. Nothing in the connectome depends on it today; the seam carries a `vision` column so the day it matters, it is a config row and not a redesign.

**Cost arithmetic, pinned (DeepSeek):** the unit map for the R0 corpus (≈ 10 communities × 6 excerpts ≈ 40k input tokens + ≈ 3k output) costs ≈ $0.007; a full first reading of the 172M-token extracted tape ≈ $25–60; the estate's markdown corpus (1.3M tokens) ≈ $0.20. The seam prints the receipt beside every generation.
