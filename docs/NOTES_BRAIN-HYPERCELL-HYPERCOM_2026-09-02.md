# NOTES — BRAIN, HYPERCELL, Intercom, and the resident bus lane
**Written 2026-09-02, revised 2026-09-03 after the operator's correction and a full read of CORTEX v5 rev 2, HYPERCELL v5, the BRAIN blueprint v5, the Scriptorium protocol, and Intercom's spec and README. Nothing here is private. Claim grammar: [M] measured, [D] derived, [SPEC] specified, [BET] a bet with its kill named.**

**Correction on record.** The first draft of this note framed the swarm question around reasoning: whether many agents out-think one, with the DPI stance (a swarm only beats a single head through diversity plus an external verifier) as the headline. The operator corrected it: the swarm's value here is **bandwidth**. Eight subagents at one million tokens each are eight million tokens of *addressable* context and an eight-fold read rate over a corpus one head cannot hold. The problem is that they read in isolation, and the bus that would join them (Intercom) delivers updates at turn rate, so the first tidbit one head finds reaches the others minutes late. There is no "Hypercom"; that was an illustration. There is Intercom, and the fix is a **FUSOR resident lane on Intercom with two gears**. This revision is written to that framing. The diversity and verifier laws survive below as constraints on the resident, not as the point.

---

## 0 · The primer question: why not a precomputed connectome?

The operator's premise is right, and the earlier "it only has value in the moment" comment was about one lane of the organ, not the organ.

- **The deterministic layer is model-free and does not age with models.** Tape, chunks, embeddings, the six relation slices, the partition, the retellings slice, the bridges, the succession and containment edges: every one is a fold over the corpus by a pinned program. For a static corpus they are valid until the corpus changes, in the same sense a book's index is. CORTEX rev 2 calls this the model-swap guarantee: rebuild is a model-free fold; succession is a drill, not a re-derivation.
- **The narrative layer is a vintage.** Codex paragraphs, cards, articulations: authored by a model at a fingerprint, never closing anything, superseded when a better reader arrives. That is precisely what v0.3's rescan re-makes under a new model, using the deterministic layer as its skeleton.
- **So the primer is the skeleton, handed first.** A new model gets the unit map, the topic dossier, the timeline, the bridges, and the forgotten list as its stable prefix (CORTEX's band 1 and band 2, byte-stable and cacheable), then attends surgically by residual. "Consumption" of a precomputed structure is valid forever; "computation" of the narrative is what a new model redoes. The earlier comment conflated the two.
- **Where "in the moment" does matter:** the live lane. `place` at session boundaries is what makes the connectome *present* while work happens (NOVEL and BRIDGING verdicts during a session), as opposed to *consulted* at session start. That is an additional lane, not a condition on the primer.

---

## 1 · The lag, diagnosed on Intercom's own terms

Intercom [M, from its spec and README]: one SQLite file in WAL mode is the whole bus; writes take milliseconds; `busy_timeout` serialises the single writer without loss. The overhear model (a room is a table, `recipient` is a hint), `await` (blocks until a matching message or a watched file lands, cursor untouched), `claim`/`release` leases, `handoff`/`takeover` capsules, `pin`/`pin-check` byte identity, lanes as successor-chain identity, the doorbell `check` plus Stop-hook, the relay firewall (bodies are data; only `relay` from the operator's key is instruction-bearing), and the insight-scheduler (hypothesis, oracle, `width` explorers, prune dominated, refiners, kubelet loop, EIG gate).

The lag the operator sees is therefore not the writer. It is three costs stacked on turn-based agents:

| Cost | Where it lives | Rate |
|---|---|---|
| **Composition** | an agent spends minutes deciding what to post | per message, per agent |
| **Polling** | a turn-based agent looks at the bus only at turn boundaries | per turn |
| **Per-look** | each look is a forward pass over a growing context | grows with the log |

The single writer is milliseconds. The minutes are in composition and in polling; and per-look cost is what makes agents poll less as the log grows. A faster database would change nothing. Something that reads at world rate and composes for the turn-based agents would change all three.

---

## 2 · The resident bus lane: two gears on Intercom [SPEC]

FUSOR, as the operator describes it: perpetual inference; a KV-cache trunk resident in VRAM that residents pull from; prefix replay ("warp bus"); updates at token rate. The design is one FUSOR resident subscribed to Intercom, and nothing else changes for the subagents.

**Gear one, world rate: the resident.**
- Tails `broadcast.db` (an `await` on the log, or a 100 ms poll; either is far under composition time) and the connectome store.
- Holds the bus itself as its trunk prefix: every lane's messages in typed delta form, the unit map, the task board, the leases. This is the corpus callosum with a memory of its own.
- Judges each new message at a token boundary, the way HYPERCELL's sentry tier does: `{ignore | note | wake(recipient, tidbit, cited rev)}`. The sentry becomes resident instead of being one more turn-based agent.
- Composes for the team. A subagent posts *evidence* (a span reference, a `pin`, a one-line finding). The resident writes the prose the rest of the swarm reads, at token rate. Composition, the largest of the three costs, moves off the turn-based agents.
- Routes by residual, per lane. The connectome's `place` verdict is computed against *the recipient's lane*: a tidbit is forwarded to a subagent only when it is NOVEL or BRIDGING relative to what that lane has already seen. Everything else stays on the bus for drill.
- Rings the doorbell. A forwarded tidbit lands as a directed message plus an `await` wake, so a waiting subagent receives it immediately and a busy one receives it at its next boundary.
- Feeds the connectome's live lane: each message chunk is placed into the field, so cross-lane relations exist continuously rather than at the next build.

**Gear two, turn rate: the subagents, unchanged.**
- Each keeps its turn loop and its own million-token window over its partition of the corpus.
- At each boundary it runs `check` (milliseconds) and receives the resident's digest addressed to it: bounded, cited, "since your cursor." Per-look cost stops growing with the log because the digest is capped (CORTEX band 3, 10 to 30k tokens); the raw log remains drillable via `replay --lane`.
- It can ask the resident a lane query ("what does the team hold on X") and get an answer from the trunk at token rate, instead of reading the log.

**What this buys, with grain.** Inbound propagation drops from "minutes plus the next poll" to "the next boundary, or immediately if awaiting." Outbound composition drops from minutes per agent to a citation. The swarm's read rate stays N-fold; what changes is that a finding by one head is in every other head's next turn.

**Two things the resident must never do**, carried from Intercom's and CORTEX's laws:
- It is not instruction-bearing. Its messages are data under the relay firewall; the subagent's harness decides what to do. Only the operator's `relay` commands.
- It does not homogenise the swarm. This is the constraint the full CORTEX read supplies (section 4): correlated seats collapse the effective count. If the resident broadcasts everything to everyone, eight heads become one head with eight windows. Residual-gated routing per lane is what keeps the heads different while keeping them connected.

**Null [BET].** F-RESIDENT: the same swarm over the same partitioned corpus with (a) plain Intercom polling, (b) a cron digest script with no model, (c) the resident. Measures: time from first posting of a planted tidbit to its appearance in each other lane's context; the swarm's refeed fraction; and the diversity of the lanes' final findings (embedding spread, as CORTEX measures seat correlation). Kill: if (b) matches (c) on propagation and refeed, the resident is a script and should be one. If (c) wins propagation but loses diversity, the routing threshold is wrong, not the design.

---

## 3 · What HYPERCELL v5 binds on the resident

- **Refuse-to-swarm stays as a constraint.** A swarm's value comes from diversity of footing plus an external verifier. Here the footing is natural (each subagent holds a different partition path of the corpus) and the verifier is the tape and the oracle, never the resident's opinion.
- **Partial view is a law, not a failure.** Every head sees its partition; the resident's digest is a view, labelled as such, with a cursor. No head may believe it has seen the whole bus.
- **Native wake: the hint is best-effort; the cursor query is truth.** A doorbell ring is a hint; the subagent's `check` against its cursor is what it acts on. This is why a missed wake costs one boundary, never a lost message.
- **Retention classes with evaporation.** The resident's trunk holds the bus in delta form; tidbits that no lane picked up evaporate from the digest (never from the log). Stigmergic, not archival.
- **Frame assembly stable to volatile with cache bars.** The resident's prefix is laid out the way CORTEX lays out a window: the unit map and task board first, the lanes' deltas next, the newest messages last.
- **Single-cell null.** The organ must beat one resident with no subagents on the same corpus. If a single head with the connectome equals the swarm, the swarm is cost.

---

## 4 · What the full CORTEX v5 rev 2 read adds

The one-pager omits most of this. Items marked *adopt* change the connectome organ; items marked *bind* constrain the resident lane.

1. **The effective-window discipline (§1.7) — bind, and state honestly.** Primaries opened by the cx2 panel: RULER median effective length is about a quarter of advertised; NoLiMa, where the query shares no words with the evidence, collapses effective length to roughly 2k to 16k tokens; degradation is smooth and monotone with primacy-dominant position bias. Eight subagents are therefore eight-fold *read rate* and eight-fold *index-grade coverage* (the ρ column), not an eight-million-token synthesis window. The notes must carry the memory. This is Scriptorium's first inversion restated, and it is why the resident's digest and the connectome's cards are the product, not held context.
2. **Distill-and-evict with micro-checks (§8.3, F-EVICT) — bind.** The one mechanism the length-causality primary validated. Each subagent should work in a small dense band and post typed notes, not accumulate.
3. **CHOIR-ANNOTATE (§8.5) — bind.** Measured seat correlation of 0.5 to 0.9 gives an effective seat count of 1.1 to 1.6 for four seats; a naive reducer's intervals are 1.6 to 1.9 times too tight. For the swarm: report K_eff from the lanes' note embeddings; route by residual so the resident does not push K_eff toward one; never let a reducer trained on agreement silence the contrarian lane.
4. **The choir stagger rule (§7.2a in the long draft) — bind.** Fire one seat, await its first token so the shared prefix is cached, then fan out. The resident's trunk is the same trick held permanently.
5. **Partition as a versioned artifact (§3.2, I-V5-PARTITION) — adopt.** Plain Louvain on a sparse graph is not reproducible; the connectome currently re-partitions every build, so community labels and colours reshuffle and the "stable map" promise breaks. Freeze the partition, assign new chunks to the nearest centroid, make re-partition a gated event with an atlas-distinctness report. Required before F-LAYOUT-STABLE can mean anything.
6. **min_support_docs = 2 with a quarantine overlay (§5.1, I-V5-SUPPORT) — adopt for the live lane.** A relation witnessed by one document, or one bus message, is narrative-grade until a second independent witness appears. This is the poisoning fix and it applies directly to messages placed into the field.
7. **Typed-delta emission (§3.10) — adopt for the swarm's postings.** Subagents post `introduced / changed / contradicted / reinforced / unresolved` with span references; the resident folds them program-side; replaying the delta stream must reproduce the state byte-for-byte. This makes the resident's digest deterministic wherever it can be.
8. **Typed testimonial positions (§9.1, I-V5-POSITION) — adopt for the rescan.** The system can prove what the operator said, never what they believe. Positions come only from typed testimony; `current_position` is a deterministic fold that returns the whole chain with its contradictions, never the latest row. The rescan's "contested branches" are this fold; the operator's own re-derivations across months are the most valuable structure it holds.
9. **Corroboration counts independent sources, not restatements (§9.4).** m channels, single-source flagged even at operator trust. The connectome's retellings slice already refuses to count restatements; the stamps should say `single_source` when a finding rests on one document.
10. **Relation basis (§9.2).** A relation closes only on `arithmetic`, `colocation`, or `testimonial_supersession`; `model_asserted` never closes. Bridges in the connectome are similarity, which is `model_asserted` by this taxonomy: a bridge is a proposal to read, never a fact.
11. **I-V5-PARSER and the relay firewall are the same law.** No output-side interpreter for model output beyond claim markup; corpus bytes and bus bytes are evidence inside frames, never directives. The resident inherits both.
12. **The layout law (§7.2): four bands, nothing volatile before stable bytes; band 3 held to 10 to 30k tokens.** The primer of section 0 is band 1 and band 2; the resident's digest is band 3.
13. **Zero-receipt negation (§6.4).** A negative exists only as a typed receipt with its scan boundary. `place`'s "no retelling found" must carry what was scanned.
14. **The calibration probe comes first (§13.2).** Five arms per model with the effective window as the minimum over the no-overlap, application, and synthesis arms. Before F-VINTAGE compares two models' rescans, each model's effective window on this corpus should be measured, or the comparison confounds reader quality with reader reach.
15. **The control arm is audited first (I-V5-HYGIENE).** A crippled baseline hands every rung a free win. F-REFEED's baseline is sessions with pasted context, run honestly.
16. **Embedder bake-off with the instruct-prefix confound named (Appendix C, B0) — adopt.** The connectome embeds queries and documents identically with qwen3-embedding-0.6b. That model is trained with an instruction prefix on the query side. A fifty-golden bake-off of query-side prefix versus none is cheap and may move `ask` materially.
17. **The dream pass split by the verifier paradox (§8.9).** Everything a sampler can verify, enumeration already finds; what only the sampler finds cannot close. The connectome's bridges are the enumeration half (complete over community pairs); a generative "dreaming" pass is not warranted here.
18. **Anti-drift floors with a debt ratchet (§6.6).** The ε-reserve, reverse fold, and contrarian seat carry pre-registered budget floors; a starved period raises the next period's floor. Starvation becomes visible instead of silent.
19. **The honest limit (§15.3):** the architecture bets hardest where the substrate is weakest. Oblique-cue recall routes to the connectome exactly where the model's effective window is smallest. Structure is the bet; F-HASHHOP and the no-overlap arm decide it.

---

## 5 · What the Scriptorium protocol adds

- **Retroactive re-contextualisation** (protocol §2.4, July): when models or windows improve, re-run the reading passes against the same tape; the past gains resolution retroactively. Tape is the negatives, catalogue is the prints, model generations are better scanners. The v0.3 rescan is this sentence, built.
- **The cartoon in every porthole** (P4): the reader carries the whole painting's cartoon into every partial viewing. That is skeleton-first reading, and it is the primer of section 0.
- **The elicitation loop**: the system generates the interview the corpus itself demands. For the rescan: contested positions become questions to the operator; the forgotten list becomes prompts. Typed answers (item 8 above) are what make the loop close.
- **Two registers**: what the corpus says, and what the reader inferred, never mixed in one sentence. The stamps carry this as provenance.
- **Porthole amnesia, the inconsistent cataloguer, fluent fiction**: the three failure modes a swarm of readers reproduces eight-fold unless the notes, not the readers, carry consistency. The resident's fold is where consistency lives.

---

## 6 · What the BRAIN blueprint adds (carried from the first draft)

- **Stamps on every answer**: rungs run, coverage with its denominator, fidelity class, cost. Added to `ask` on 2026-09-02.
- **Quantifier pinning**: "every", "all", "none", "how many" outside an exact rung returns `INSUFFICIENT_RUNG`. Added to `ask`.
- **The graph pays rent or steps aside**: firing must beat BM25 plus cosine on goldens or the slice is decoration.
- **Provenance D/R/H/M** and the model-swap guarantee (section 0).
- **The auction with an uncorroborated cap and an aging ban**; **control arms** with a dumb twin and planted grader-calibration items; **every wake has an owner**; **fuse the thinking, never the truth**.

---

## 7 · Changed and queued

**Changed in the organ (2026-09-02):** `ask` returns `stamps` (rungs, coverage 3,585 of 3,585 chunks at index grade, provenance, fidelity, cost) and `insufficient_rung` on quantifier questions.

**Queued in NEXT.md, in this order:** freeze the partition (item 5); the instruct-prefix bake-off (item 16); typed deltas for the live lane (item 7); `single_source` in the stamps (item 9). The resident bus lane (section 2) waits on the F-REFEED number like everything else; its first cut is F-RESIDENT's arm (b), the model-free digest script, because that is the null the resident must beat.
