# CONNECTOME v5.5 — The Field
### A self-supervised model of a text stream: meaning-based, true-3-D, native C++/CUDA, live, stable, rescannable, general across any corpus, engineered from the September 2026 state of the art and from measurements taken on this box

**Revision v5.5, final crystallisation · 2026-09-03 · the design of record and the implementation target. v4 and v5 skipped by operator directive; v0.1–v0.3 (this repo, 2026-09-01) and the v5.5 draft of earlier today are lineage.**
**Authors:** Bo Chen (the asks: hold, attend, rescan, join; the slide rule; the primer; the corpus callosum; the correction that the schema must learn itself the way language models learned language; the native-CUDA directive; the harness; the embedder) · Claude Fable 5.1 (this synthesis, after reading every pointed document whole — `docs/READING-RECEIPT_2026-09-03.md`, 21 files, 1.2 MB — five research reports on the September-2026 frontier under `docs/sota/`, and nine measurements on this machine).
**Register:** engineering. Every number is **[M]** measured on this box, **[V]** verified on a primary web page (URL and date), **[D]** derived by arithmetic from [M]/[V], or **[BET]** a bet with its kill named. Nothing else is asserted.

---

## 0 · The one idea

Language models learned language from a stream of text with no labels: the stream supervised itself, the next token was the teacher, and the structure that emerged (attention over what came before) was never hand-tuned. The connectome is the same object one level up. **Its stream is documents and transcripts arriving in time. Its teacher is the next document. Its loss is the residual: how badly the field, as it stands at time t, predicts what arrives at t+1.** Everything the connectome learns (which embedder and chunking predict the future best, where communities lie, what counts as a retelling, what counts as new, what deserves attention, which positions superseded which) is learned by reducing that loss on the corpus's own future, never by asking a person to label anything. People can rate things; ratings are more tape. Nothing gates on them.

Measured today on the operator's estate, 264 documents dated 2026-06-30 to 2026-09-03, 3,585 chunks [M]: when each document is scored against the field built from the documents *before* it, the time-ordered field predicts the next document better than a shuffled field of the same size in the first two deciles of arrival (mean residual 0.306 vs 0.421, 0.292 vs 0.350) and in the last (0.221 vs 0.258), and worse in the middle deciles (mid-July to mid-August), when the operator opened new fronts. The newest decile is 23 % retellings. **The corpus is a non-stationary stream of fronts.** The field converges *within* a front and must open new structure *between* fronts; a design that expects one global fixed point is wrong, and a design that reshuffles on every arrival is worse. Everything below follows from that.

**What it is, concretely:** a tape of everything (documents, transcripts, later images and PDFs as text), embedded locally into one semantic space, indexed three ways (dense, lexical, graph), partitioned once into a versioned community tree that grows by assignment, laid out in hyperbolic space so that radius is resolution (the unit map at the centre, communities around it, chunks toward the rim, detail growing exponentially with distance from wherever you look), rendered natively in 3-D by a C++/CUDA viewer, driven by one loop (place the new thing, let its residual decide how much attention it earns, write back what changed as typed deltas, let the shape bias what is read next), rescannable by any newer model from the skeleton plus surgical reads, and shared with agents through Intercom with one always-on sentry. Everything above the tape is a fold over the tape; nothing above the tape is truth.

**Who it is for:** anyone whose corpus outgrew every window and every human reader. The same organ serves a writer (drafts and their retellings, a theme's sharpest articulation across versions), a law firm (matters, filings, holdings, conflicting authorities, positions per matter and their supersession by later rulings), a researcher (papers, notes, results, hypotheses superseded, bridges across fields), an organisation (decisions and who said what), and the operator's own estate (design documents, chat transcripts, the FUSOR arc). Domains differ only in what the corpus contains; the schema is induced from the corpus, not chosen for it (§2.4).

**Today [M]:** the v0.1 organ runs (build, ask, place, codex, dossier, render, mcp, providers) on the estate with seven relation slices, 160 bridges, 590 retellings and 17,828 transcript messages; a `place` verdict takes 3.0 s; the page renders in two geometries. **What v5.5 changes:** the learning law and the label-free evidence (§2, §12), the embedder (WeMM 4B/9B unified text+image, Qwen3-Embedding as the llama.cpp lane, with the instruction the card requires), the index (Matryoshka two-pass int8 GEMM), the partition (frozen, versioned, assigned, consensus-stabilised), the geometry (analytic Lorentz placement, radius = level and importance), contextual headers, a local reranker gated by source, the bi-temporal position ledger, typed deltas, the sentry on the bus, a native C++/CUDA core and viewer in the operator's own build conventions, the DeepSeek harness as the worker runtime, a stateless MCP server on the 2026-07-28 spec, the Pareto-frontier gear-two model, and a build plan with machine-checkable gates instead of a kickoff.

---

## 1 · The four asks and the four answers

| Ask (operator, verbatim gist) | Answer | Where |
|---|---|---|
| **Hold:** keep adding forever, never overflow, compress organically like a lifetime, structure = identity | Tape + frozen partition tree + always-total unit map + hyperbolic radius-as-resolution + curriculum and vigilance by fronts | §4, §6, §7 |
| **Attend:** new material read through what is already known; structure biases attention; open but not flipped overnight | Residual-gated placement, priority r/v, contextual intake with the map slice, precision-weighted positions, drift alarm | §7 |
| **Rescan:** a smarter model re-derives the sharpest articulation of a topic without re-reading everything | Dossier skeleton as pinned prefix → hyperbolic-ball reads → claims with derived spans → reprojection scored against held-out documents → vintage + diff | §8 |
| **Join:** N subagents = N× read rate; Intercom is the corpus callosum; the bus is too slow at turn rate | Bandwidth law, the sentry at world rate on Intercom, typed deltas, residual-gated routing, the FUSOR seam, harness workers | §9 |

---

## 2 · The learning law

### 2.1 Signal, parameters, loss
- **Signal:** the tape in arrival order. Free supervision the tape already contains: time (arrival and event time), succession (what follows what inside a document or session), **provenance** (a session message and a document span that share an exact 12-gram: the session that produced the document), exact and near duplicates (retellings), the operator's own citations and quotations, and the operator's own later documents (the corpus cites itself).
- **Parameters:** everything above the tape: embedder and chunk policy, contextual headers, relation slices and their weights, the partition and its hierarchy, the layout, the residual thresholds, the priority weights, the Hebbian ledger, the position ledger, the pages and the unit map, the router.
- **Loss:** for a document D arriving at t+1 and the field F_t built from everything before it, $L(D \mid F_t) = \text{mean over chunks of } (1 - \max_j \cos(x, X_j))$ at the chunk grain, plus the share of D's atomic claims absent from the position ledger at the claim grain. Lower is better *for prediction*; the connectome is the thing that minimises expected future loss **without ever changing the tape**: it can only change how it indexes, organises, and attends.
- **Holdout is time.** Every evaluation is temporal: build on documents before t, score on documents after t, compare with a shuffled-order control at matched corpus size (the first F-CONVERGE run is §0; the falsifiers are §12). No human labels enter any gate. Where a human rates, the rating is appended to the tape as testimony with a date and is one more signal the future can confirm or refute.

### 2.2 Thresholds are quantiles of the corpus's own distributions, re-estimated as it grows
The retelling bar is the trough of the corpus's bimodal top-1 cosine distribution (0.97 today [M]); the NOVEL / ROUTINE bars are quantiles of the residual distribution over the trailing window (registered at the 90th and 40th percentiles, re-estimated nightly); the bridge bar is the quantile above which cross-community pairs occur less often than chance; the drift bar for the partition is set from the measured reshuffle rate of fresh Leiden on this corpus (ARI 0.73–0.86 between seeds [M]) so that a version event fires when assignment drift exceeds what fresh clustering would itself disagree about. A corpus of legal filings, diary entries, or drafts gets different numbers from the same rule.

### 2.3 What learns, what stays frozen, and why
- **Learn by the loss:** embedder choice and prefix (§5.1), chunk budget (§4.2), fusion weight α (§5.5), slice weights and hop count (§6.6), the priority weights (§7.1), the reranker gate (§5.3), the router (§8.1). Each is a small parameter set tuned on temporal holdout, the way a language model's hyperparameters are, and each ships with its measured effect on future residual.
- **Learn by the corpus's structure, not the loss:** the partition (§6.3) and the pages (§7.5), because they are the *map*, and a map that re-optimises itself against every arrival stops being a map. They change only at version events, whose cadence is itself a measured parameter.
- **Frozen by construction:** the tape, the fence (a quote is located in the tape by deterministic code or it is not a quote; model-emitted offsets measured 0 % usable [M, Scriptorium]), typed negatives, the pointer law (a node holds no content), and provenance-role typing (an assistant's paraphrase never becomes a claim attributed to the operator).

### 2.4 Schema induction (general purpose by construction)
The community tree is induced from embeddings (§6.3); community and topic names are written by a model from members and re-written at version events (Clio's pattern; EVōC/Toponymy are the open tools) [V]; entity and predicate vocabularies for the position ledger are induced by extraction, then consolidated by embedding-cluster plus exact-quote evidence (never surface-string identity); eras are change points on the community-mass time series; the operator's kernel line ("who this is for, in their words") is the only hand-written text and it is optional. Scriptorium's P1 discovery pass is the batch form of this; here it runs continuously, and the induced schema carries a fingerprint so a re-induction is a new version, never a mutation.

### 2.5 The fronts law (from the measurement)
**Implemented and gated at M1 [M].** The detector compares a window of arrivals (8 documents) against the trailing field (40) in units of the trailing dispersion; a front opens above z = 1 and closes when the corpus stops surprising its own recent past. On the estate this finds exactly one front — 2026-08-10, `MEANDER-SPEC-v0.1` through the BLACKBOX burst, 21 documents, peak z +1.07 — sitting in the same deciles where the shuffled control beats arrival order, so two independent instruments agree. The first version of this detector used a per-document CUSUM and never fired (max 0.88 against a 5σ bar): document residuals are tightly packed (quartiles 0.277–0.356), so one document is a fraction of a σ and the statistic drains before it accumulates. **A front is a window-scale phenomenon, not a document-scale one**, and that is a measured correction rather than a tuning choice.

A stream of fronts needs two rates: **within a front** the residual falls and retellings rise, so attention should decay (habituation); **between fronts** a burst of NOVEL chunks arrives that no community explains, so the field must open provisional structure quickly (vigilance) and confirm it only when independent witnesses accumulate. Both rates are measured from the tape (§7.3): the burst detector is a CUSUM on the residual series per lane; a front is declared when residual exceeds the trailing 90th percentile for m consecutive documents, and closed when the retelling share exceeds its own trailing 90th percentile. This is where Kimi's attention-residual idea and the eye-harness result meet: the residual, not the raw signal, is what should drive attention, and a loop that never re-measures its residual fixates (GLANCE-RACE-2 [M]).

### 2.6 Sycophancy is the failure mode of a self-supervised memory, and the guard is also self-supervised
A field that updates positions from whatever was said last drifts toward the last speaker; 2026 evidence says models detect such conflicts but rarely act on them (BeliefShift, MemSyco-Bench, ACL 2026 Findings) [V] arXiv:2603.23848, arXiv:2607.01071, aclanthology.org/2026.findings-acl.103. So `supersede | contradict | refine` edges on the position ledger are **proposed with evidence and scored by the future**: a proposed supersession is confirmed when later documents keep citing the new position and stop citing the old one, and demoted when the reverse happens; the operator may confirm in one command, but the default confirmation is the corpus's own subsequent behaviour, and every edge carries `confirmed_by ∈ {future, operator, none}`.

---

## 3 · Physics (2026 numbers that constrain everything)

- **Effective context.** NoLiMa (ICML 2025): effective length 1K–8K tokens without lexical overlap; RULER median ≈ 25 % of advertised; Chroma: monotone degradation, primacy-dominant [V] arXiv:2502.05167; none of the three has 2026 models. The live 2026 measurement is Context Arena's 8-needle MRCR v2 at 128K (rendered 2026-09-03): GPT-5.6 Sol 92.4 %, Qwen3.8-Max 92.3 %, **Claude Opus 5 91.3 %** (AUC to 128K 97.5 %, first), Gemini 3.7 Flash 88.6 %, **Qwen3.8-27B 81.8 % (open weights)**, Opus 4.8 75.2 %, GLM-5.3 69.3 %, **GLM-5.3-Flash 62.9 %, DeepSeek V4 Flash 62.9 %**, Sonnet 5 52.9 %, Kimi K3 38.3 %, Qwen3.5-9B 15.4 %, Haiku 4.5 13.8 %, **Opus 4.7 0.5–1.4 %**; at exactly 1M the best run is Gemini 3.7 Flash at 63.5 % [V] contextarena.ai/?needles=8. The Fable 5.1 system card (2026-09-01, 212 pp) reports no MRCR; its full-window evidence is ProgramBench: Fable 5.1 87.6 %, Fable 5 86.3 %, Opus 5 85.4 % [V]. **Law:** 128K–256K is the ceiling for multi-fact recall; 1M is storage. Eight 1M-token subagents are eight times the read rate and the addressable index, not an 8M-token synthesis window; at equal thinking tokens a single agent beats a swarm on multi-hop reasoning and a swarm wins only where the single agent's effective context is degraded [V] arXiv:2604.02460, which is exactly reading a corpus larger than any window; blackboard designs report +13–57 % task success with fewer tokens than agent-to-agent chatter [V] arXiv:2510.01285, arXiv:2507.01701.
- **Reading is cheap; re-reading is a line item.** GLM-5.3-Flash $0.075 / $0.015 cached / $0.25 out per M tokens (50 % promo to 2026-09-09 24:00 UTC+8; then 0.15 / 0.03 / 0.50), 1M context, 128K out, native video/image/text/file, thinking cannot be disabled; Artificial Analysis Intelligence Index v4.1.1 (2026-08-26): 57 points at $0.045 per task, on the Pareto frontier [V] docs.z.ai, operator screenshot. DeepSeek V4 Flash $0.22 / $0.007 / $0.66 off-peak, ×2 at 01–04 and 06–10 UTC weekdays [V] api-docs.deepseek.com. **The $0.14 / $0.0028 / $0.28 figures in Scriptorium and CORTEX are stale.**
- **Cache reads are the cheapest tokens.** Fable 5.1 $10 / **$0.25 (0.025×)** / $50; Opus 5 $5 / $0.50 / $25; Sonnet 5 $2 / $0.20 / $10 (permanent); 5-min write 1.25×, 1-h write 2×; batch −50 %; full 1M at standard price [V] platform.claude.com pricing 2026-09-03. A pinned skeleton read fifty times costs less than one cold read.
- **Local is free and fast.** This box, llama.cpp b9627, RTX 4070 Ti SUPER 16 GB, measured with the resident embedder and browsers holding 9.8 GB (lower bounds) [M]: qwen3-embedding-0.6b-q8_0 on :8092 embeds 18.7 chunks/s of ~700 tokens (13.1k tok/s); Qwen3.5-9B Q5_K_M 4,148 tok/s prefill / 71 tok/s generation; Qwen3.5-4B Q4 6,864 / 123; Qwen3-8B Q4 5,440 / 90; a 1,664-token shared prefix re-prefilled in **16 ms** with `cache_prompt: true`; a 3,585² cosine GEMM 73 ms on CPU; CORTEX measured FIND over 1.67M×384 vectors in 4.88 ms on the GPU. Qwen3.8-27B (Apache-2.0, 2026-08-14, 262K native, image+video, 81.8 % at 128K) fits resident at IQ3_XXS 10.9 GB or Q3_K_XL 13.1 GB, not at Q4_K_M 16.5 GB, and should generate ≈ 33–40 tok/s here by bandwidth [D] [V] huggingface.co/unsloth/Qwen3.8-27B-GGUF. Resident server flags verified against `llama-server --help`: `-np 2..4 -cb --cache-ram 8192 --kv-unified --cache-reuse 256 -ctk q8_0 -ctv q8_0 -fa on --slot-save-path …` [M].
- **Partitions reshuffle unless frozen.** Louvain across six seeds on the live field: ARI 0.73–0.86 versus seed 0; removing 2 % of nodes and re-running: 0.76 on shared nodes [M]. One in four memberships moves every rebuild.
- **The raw embedding space is not a tree.** Four-point Gromov δ on 2,000 chunks: δ/diameter 0.054 at p99, about twice a random-cloud control [M]. The hierarchy is imposed by the partition; embeddings supply angles (§6.4).
- **Quotes cannot be trusted from a model.** Scriptorium's fence caught 28.5 % paraphrase-as-quote on the raw tape and 12.8 % on the extracted one; model-emitted offsets were 0 % usable; spans are derived by locating quotes in the tape (87.2 % located) [M, C:/scriptorium/README.md].
- **Residual beats uniform attention.** GLANCE-RACE-1/-2: residual-driven glancing catch 99.7 → 80.9 % across difficulty vs uniform 64 → 13 %; priority = residual / channel volatility; staleness is a sampler; a frozen loop fixates [M, C:/NEW/eye-harness/].
- **Hyperbolic space is the right container for a hierarchy, and the wrong index.** HypRAG (Lorentz, 149M params): MTEB 56.41 vs 54.11 for an equal Euclidean encoder, +29 % context relevance on RAGBench, +20 % radial norm from general to specific [V] arXiv:2602.07739; HyBIRD: hyperbolic geometry is "most useful as calibrated structure over a dense anchor" [V] arXiv:2606.28336; some reported hyperbolic gains are radius regularisation [V] arXiv:2309.10013. No hyperbolic encoder exists at the 1B–8B scale of current retrievers.
- **Incremental community maintenance exists.** HIT-Leiden: bounded updates in the 2-hop neighbourhood of affected supernodes, up to five orders of magnitude faster than recomputation, modularity within 0.5 % [V] arXiv:2601.08554 (no public code); LD-Leiden 48.8× over warm-started leidenalg at 214M vertices [V] arXiv:2502.18497; FastEnsemble consensus (10 seeds, co-classification 0.8) [V] PLOS Complex Systems 2025-10-01; Leiden admits exponentially many near-optimal partitions on sparse graphs [V] arXiv:2603.05207.
- **Memory systems' honest numbers.** Zep/Graphiti 63.8 % vs Mem0 49.0 % on LongMemEval [V]; HippoRAG 2 lifts MuSiQue F1 44.8 → 51.9 and indexes with 9M tokens vs 115M for LightRAG/GraphRAG [V] arXiv:2502.14802; hierarchy helps aggregation and multi-fact reasoning and hurts fact lookup (GraphRAG-Bench: basic RAG 60.92 vs GraphRAG 49.29 on facts; 42.93 vs 50.93 on reasoning; HippoRAG 2 at ≈ 1K tokens/query vs GraphRAG-global ≈ 331K) [V] arXiv:2506.05690; verbatim retrieval plus redundancy pruning matches engineered memory (Nano-Memory; MemDelta: an embedding swap alone moves accuracy 6.2 points) [V] arXiv:2604.11628, arXiv:2606.29914.
- **Chunk context beats chunk boundaries.** Contextual retrieval cut top-20 failures 35 % (embeddings), 49 % (with BM25), 67 % (with rerank) [V] anthropic.com/news/contextual-retrieval; paragraph-group chunking nDCG@5 0.459 vs 0.244 fixed; semantic chunking's cost is unjustified [V] arXiv:2603.06976, arXiv:2410.13070; late chunking needs mean pooling, which Qwen3-Embedding and jina-v5 do not use [V] arXiv:2409.04701.
- **MCP is stateless now.** The 2026-07-28 spec: no sessions or handshake, `server/discover`, `Mcp-Method`/`Mcp-Name` headers, `ttlMs`/`cacheScope`, deterministic tool order, Tasks as an extension [V] modelcontextprotocol.io changelog; Python `mcp` 2.1.1 and TypeScript `@modelcontextprotocol/client|server` 2.0.0 implement it; Claude Code runs v2 by default since v2.1.232; OpenCode pins sdk 1.29 (v1) [V].

---

## 4 · Data layer — the tape and the chunk

### 4.1 The tape (truth)
- One append-only, blake2b-128 hash-chained JSONL tape per archive root in **Scriptorium's format** (`doc` / `text` / `journal` / `contact` records; spans `{doc_id, seq, start, end}` into NFC canonical `text`), so the two organs share negatives and the fence. Transcripts enter as `doc` records of kind `transcript` with per-message `text` records `{session, uuid, role, ts}`; everywhen's shards remain the source.
- **Origin and trust are stamped at intake from the channel, never from content:** `operator-doc`, `transcript-operator`, `transcript-assistant` (narrative), `imported` (untrusted). Provenance-role collapse is the top failure the 2026 memory literature names; typed atoms fix it (+28 % reliability, 5.8× fewer retrieved tokens) [V] arXiv:2605.25869, arXiv:2605.28009.
- **Byte-exact dedup first:** conversational corpora are ~80 % redundant by bytes (80.34 % removed with zero regression) [V] arXiv:2605.09611; duplicates fold to one `text` record with a multiplicity count.
- Every derived output (cards, verdicts, deltas, partition versions, pages) is a journaled `derived` record with `{model_fp, prompt_hash, inputs}`: a rebuild is a model-free fold; a model swap is a re-adjudication.

### 4.2 Chunking
- `C:/chunker/chunker.py --budget 512 --overlap 40` (the `--overlap 0` hang is a known defect; the estate is chunked at 700 today; 512 vs 700 is decided by future residual, F-CHUNK). Structure-aware: heading boundaries, then paragraph groups.
- **Contextual header, deterministic, $0:** `{doc title} › {breadcrumb} · {era: YYYY-MM} · {origin}`, embedded with the chunk and indexed by BM25. A model-written one-sentence context (Anthropic's recipe) is added only for chunks whose placement residual is high (§7), on gear two: 3,585 chunks ≈ $0.27 at the promo price [D].
- **Transcripts at three granularities:** segments of 5–15 messages under a session header, a per-session summary, extracted claims. LongMemEval-V2 loses 28.6 points when the raw-slice pool is removed; LMEB shows MTEB rank anti-correlates with dialogue retrieval (−0.496), so transcript retrieval is judged only by this corpus's own future [V] arXiv:2605.12493, arXiv:2603.12572.
- **llama-server contract:** `-ub` ≥ the longest chunk; `/v1/embeddings` L2-normalises, `/embedding` may not [V].

### 4.3 Sizing across corpora [D from M]
| Corpus profile | Chunks (512 tok) | Serving vectors (1024-d int8) | Coarse head (128-d int8) | Where they live |
|---|---|---|---|---|
| Estate today (3.6k chunks) | 3.6k | 3.7 MB | 0.5 MB | VRAM |
| Personal archive, extracted (172M tok) | ≈ 335k | 343 MB | 43 MB | VRAM |
| Personal archive, raw (1.75B tok) | ≈ 3.4M | 3.5 GB | 0.4 GB | VRAM (coarse) + VRAM or host (full) |
| Law firm or research group (10¹⁰ tok) | ≈ 2×10⁷ | 20 GB | 2.5 GB | coarse head in VRAM; full vectors memory-mapped on NVMe, rescoring reads ≤ 2k rows per query |
Embedding time at the measured 0.6B rate: 172M tokens ≈ 3.6 h; at ≈ 4× slower (4B class) ≈ 15 h; 10¹⁰ tokens ≈ 9 days at 0.6B or ≈ 35 days at 4B, so the 10¹⁰ profile embeds with the small model first and upgrades by front. Placement, partition assignment and layout are O(n); nothing in the design is quadratic in corpus size except the analysis passes that are explicitly scoped (§6.5).

---

## 5 · Index layer

### 5.1 Embedders (both, not either)
- **Unified text + image, default:** **WeMM-Embedding-4B** (Tencent, arXiv:2608.24053, August 2026; Qwen3.5-based; 2,560-d L2-normalised with Matryoshka truncation; text, images, video, visual documents, interleaved; MMEB-v3 58.2 over 190 tasks vs 50.9 for Qwen3-VL-Embedding-2B; Apache-2.0; `encode_query`/`encode_document`) and **WeMM-Embedding-9B** (4,096-d; MMEB-v3 59.5 vs 53.5 for Qwen3-VL-Embedding-8B) for cold builds when the card is free [V] huggingface.co/tencent/WeMM-Embedding-4B and -9B, fetched 2026-09-03. No GGUF yet: they run under transformers on the GPU (4B ≈ 5 GB at int8, 9B ≈ 9 GB) through a small OpenAI-compatible shim so the rest of the stack sees one `/v1/embeddings` contract. Weights are fetched with `C:/fetcher` (the operator's HF downloader).
- **Text lane on llama.cpp:** Qwen3-Embedding-4B (2,560-d, MTEB-multilingual 69.45; 8B 70.58 for +1.1 at ~2× cost; 0.6B 64.33 is the current state) with the card's query instruction `Instruct: {task}\nQuery:{query}` on queries only and none on documents [V] huggingface.co/Qwen/Qwen3-Embedding-0.6B; GGUFs run with `--embedding --pooling last` [V] llama.cpp discussion #16787. **F-PREFIX first measurement [M]:** on 28 free goldens (transcript messages quoting a document span by 12-gram), the instruction lifted dense recall@1 0.429 → 0.464, @10 0.750 → 0.786, @20 0.786 → 0.821 with the 0.6B model. The prefix ships; the definitive comparison is by future residual (§12).
- **Stored dims:** 1024 (MRL-truncated, re-normalised) as the serving vector and a 128-d coarse head; the exact instruction string and model hash are stored with the index (a changed instruction is a silent model swap). Which embedder serves which corpus is **learned by the loss** (F-EMBED): the one whose field predicts the corpus's own future best wins, per corpus, per version.
- **Swaps:** overnight re-embed (free), with Drift-Adapter (orthogonal Procrustes or a small affine map from a paired sample; 95–99 % of Recall@10 retained) as the bridge while it runs [V] arXiv:2509.23471; Voyage 4's shared space and 200M free tokens are the paid fallback for a 172M-token pass ($0–24) [V] blog.voyageai.com 2026-01-15. Candidates on the bench: KaLM-Embedding-Gemma3-12B (MMTEB 72.32, no llama.cpp path confirmed), Nemotron-3-Embed-1B/8B (RTEB 72.38 / 78.5, GGUF unknown), jina-v5-small (llama.cpp truncates over ~512 tokens) [V] `docs/sota/SOTA_embeddings-retrieval_2026-09-03.md`.

### 5.2 Lexical
SQLite FTS5 (BM25) with the contextual header up to ≈ 10⁷ chunks; beyond that a native inverted index in the CUDA core (§10), with `C:/everywhere` (the operator's GPU content grep, 1.4 s over a 172M-token tape [M, CORTEX]) as the exact rung and verifier of last resort. Learned sparse (SPLADE-class) is a bench item.

### 5.3 Rerank, gated by source
Qwen3-Reranker-4B (MTEB-R 69.76) on llama-server `/v1/rerank` with `--reranking --pooling rank --embedding`, converted from the HF repo with the current `convert_hf_to_gguf.py` (community GGUFs lack `cls.output.weight` and return 1e-23 scores; issue #16407 open) [V]; a relevant/irrelevant pair must separate in the smoke test. Expected lift on documents ≈ +12 points R@5 over hybrid alone [V] arXiv:2604.01733; on conversational memory a cross-encoder *reduced* Hit@1 by 6.9 points [V] arXiv:2606.04194, so the gate is learned per source by the loss (documents on, transcripts off, until the future says otherwise). Late interaction (ColBERT-class) is a long-document rescorer only, with chat-style queries condensed to ≤ 20 content words first (long queries collapse MaxSim by 86–97 %) [V] arXiv:2604.09982.

### 5.4 The two-pass scan (SCAN, DON'T SEEK, with Matryoshka)
```
recall_dense(q):
  q128, q1024 = embed(instruct + q)             # MRL heads of one vector
  s  = GEMM(int8 X128, q128)                     # all N chunks; 2×10^7 × 128 int8 = 2.5 GB in VRAM, ≈ 4 ms
  C  = top_k(s, 2048)
  s2 = GEMM(int8 X1024[C], q1024)                # exact rescoring of 2,048 rows (NVMe-mapped beyond VRAM)
  return top_k(s2, 100)
```
Exact, no ANN index to build or rot; brute force is the measured floor (4.88 ms at 1.67M×384 [M, CORTEX]). sqlite-vec holds the same int8 vectors on disk for portability [V].

**Implemented and gated at M0, measured on this box 2026-09-03 [M]** (`native/`, CUDA 13.1, warp-per-row `__dp4a`, fixed-topology shuffle reduction):

| coarse pass over | CPU reference | GPU, copied per query | **GPU resident** | exactness |
|---|---|---|---|---|
| 250k chunks (30.5 MiB) | 9.00 ms | 13.05 ms | **0.29 ms — 102 GiB/s** | bit-identical |
| 2M chunks (244 MiB) | 68.37 ms | 88.61 ms | **2.02 ms — 118 GiB/s** | bit-identical |

Three consequences, all measured rather than argued. **(a)** An exact scan of two million chunks costs two milliseconds, so the ANN index the rest of the field builds is unnecessary at every scale this design targets; extrapolating the resident row to §4.3's largest tier (2×10⁷ chunks, 2.5 GB coarse) gives ≈ 21 ms per query [D]. **(b)** The transfer *is* the cost: a GPU path that re-uploads the matrix per query loses to the CPU (13.05 vs 9.00 ms), which is why the coarse head is resident at every corpus scale (§10.3) and why the benchmark keeps the losing row in view. **(c)** Determinism is a property of the arithmetic, not a tolerance: int32 sums of int8 products under a fixed reduction topology with no float atomics make the GPU result equal the CPU reference exactly, on every run and every supported architecture, which is what makes the M0 gate meaningful.

### 5.5 Fusion and rent
Convex combination of min-max-normalised scores (α ≈ 0.5, tuned by the loss), not RRF: CC beats RRF in and out of domain and RRF is k-sensitive [V] arXiv:2210.11934; the 2026-04 benchmark gives R@5 BM25 .644, dense .587, RRF .695, **CC .726**, hybrid+rerank .816 [V] arXiv:2604.01733. Graph firing enters as a third normalised score. **F-RENT:** every signal must reduce future residual (and the label-free recall proxies of §12) beyond the best pair without it, or it leaves the hot path; its additive contribution is printed on every answer.

---

## 6 · The field — graph, partition, geometry

### 6.1 Nodes
Chunk (T¹), document, community (T²), super-community (T³), corpus (T⁴, the unit map). A node carries `{id, level, locator (partition_version, c1, c2, seq), span_list, salience, degree, origin, trust, vintage}` and **no content** (a wrong firing costs one span read).

### 6.2 Slices (CSR + CSC, resident)
| r | slice | basis | notes |
|---|---|---|---|
| 0 | semantic kNN | deterministic | top-10 by cosine ≥ 0.50, mutual-kNN symmetrised |
| 1 | retelling | deterministic | cosine ≥ the learned trough (0.97 today) **or** MinHash 5-gram Jaccard ≥ 0.80; never evidence, never a bridge; groups collapse to the earliest span on the timeline |
| 2 | containment | deterministic | chunk ∈ doc ∈ community |
| 3 | succession | deterministic | tape order within a document; message order within a session |
| 4 | lexical | deterministic | BM25 co-hits on rare terms, count-shrunk |
| 5 | provenance | deterministic | **transcript ↔ document** by exact ≥ 12-gram: the session that produced the document; the tape's own citations |
| 6 | contradiction / supersession | arithmetic over typed inputs | from the position ledger below |
| 7 | Hebbian | ledger fold | verified use (a later document or session cites the span), difficulty-scaled, asymmetric decay, capped at 0.25 |

**The position ledger** (the middle layer between verbatim chunks and pages): `holds(entity, predicate, stance, valid_from, valid_to, created_at, expired_at, superseded_by, evidence_spans[], origin, confirmed_by)`. Graphiti's four timestamps and its rule (a superseding edge closes the old one's validity window; nothing is deleted) are the reference [V] arXiv:2501.13956; an LLM judge on the write path without typed operators and audit rows admits replay inconsistency, drift skew, or audit erasure [V] arXiv:2606.06240; event time and tape time are separate columns, and a semantic timeline gains up to +12.2 points over a dialogue timeline [V] arXiv:2601.07468. **Support gating:** a relation witnessed only by untrusted sources needs ≥ 2 independent documents or lives in a quarantine slice; weights are count-shrunk (`w = pmi · c/(c+3)`) so a count-1 pair never carries ceiling weight (CORTEX I-V5-SUPPORT).

### 6.3 The partition as a versioned artifact
```
partition/v1: seeded Leiden (pinned seed, canonical vertex order) on the backbone (r0 ∪ r4 ∪ r5), size-repaired (> 2×target bisected, < 0.5×target agglomerated);
              hierarchy by resolution (γ 1.0 → T², γ 0.3 → T³); centroids per community; FastEnsemble consensus over 10 seeds, co-classification 0.8
between versions:
  assign(chunk) = argmax_k cos(x, c_k) subject to size caps; over-cap → overflow bucket (seeds the next version)
  bounded local refinement, HIT-Leiden-shaped: only nodes within 2 hops of new nodes may move, only on modularity gain, one pass per sleep
  drift = fraction of nodes whose nearest centroid ≠ their community; version event when drift > the learned bar (§2.2) or a front closes (§2.5)
version event: partition/vN with the old→new map, a distinctness report, re-induced names, and a re-anchored layout (§6.4); consumers pin the version
```
**Kill [BET]:** if assignment-only communities trail a fresh consensus Leiden by more than 5 modularity points after a quarter of growth, refinement runs weekly; if they still trail, the cadence halves. Deterministic k-core hierarchies (KDD 2026) are the trial alternative for the document layer [V] arXiv:2603.05207.

### 6.4 Geometry — radius is resolution
**Retrieval stays Euclidean; the map is hyperbolic** (§3). Coordinates live on the Lorentz hyperboloid $\mathcal{L}^3$ in float64 on the CPU (the safer model to compute in; umap-learn's `output_metric="hyperboloid"` is the same Euclidean parametrisation) [V] arXiv:2211.00181, arXiv:2505.18973; the GPU receives only $\rho = \tanh(r/2) < 1$. Placement is arithmetic, because no hyperbolic optimiser scales past ≈ 10⁵ points (hyperbolic t-SNE: 89,701 points in 45 min, 2-D) [V] arXiv:2401.13708, and because the field's own δ (§3) says the raw space is not a tree:
```
level radii    : Δ = ln(b)/2 per level; with branching b ≈ 10, Δ ≈ 1.15 → display radii ρ ≈ 0 / 0.52 / 0.82 / 0.94 for corpus / T³ / T² / chunk
                 (H³ volume grows ≈ e^{2r}: each level has b× the volume of the one above)
within a level : r_i = r_level − ½ ln(k_i / k̄_level), clipped to ±Δ/2; k_i = importance (PageRank on the kNN graph, citations in the ledger):
                 the Krioukov law, radius encodes expected degree, angle encodes similarity
angle          : the unit-normalised Euclidean UMAP-3 coordinate; children constrained to their parent's cone (Munzner's H3, 300k edges in 1998)
rim            : chunks below a focus-dependent importance cut go past ρ ≈ 0.94 and are drawn as density, not as pickable instances
```
Precedents: [V] arXiv:1006.5169 (radius ↔ degree), arXiv:1106.0286 (radius ∝ ln t; new links minimise hyperbolic distance), arXiv:2410.04010 (HypLoRA: frequent abstract tokens near the origin inside LLMs), HypRAG (+20 % norm general → specific). Pooling happens on the manifold (naïve Euclidean averaging then projection collapses toward the origin) [V]. **The slide rule is the Poincaré map itself:** $\rho = \tanh(r/2) < 1$ for every hyperbolic distance, so adding documents can never overflow the ball, and resolution degrades toward the rim as $1/(1-\rho^2)$.

**Angles:** Euclidean UMAP-3 (cuML 26.08, deterministic kNN and a serial-optimise option since 26.06; 10⁶ × 768-d in under a minute on one consumer GPU; `init=` warm-starts from the previous coordinates) [V] github.com/rapidsai/cuml/releases; at version events only. **Stability (F-LAYOUT-STABLE):** new nodes are placed immediately by `UMAP.transform()` (angle) and the analytic radius (level, importance); nothing else moves. Periodic re-fits use ParametricUMAP with ≈ 1 % of old points as landmarks (`landmark_loss_weight` ≈ 0.01) [V] umap-learn docs; then orthogonal Procrustes onto the shared nodes' previous coordinates; then hysteresis (a node moves only if its hyperbolic displacement exceeds 0.1 Δ). **Bar:** median displacement of unchanged nodes ≤ 2 % of the ball radius per build; a version event may exceed it and says so.

### 6.5 Bridges (proposals, never findings)
A pair with cosine ≥ the learned bridge bar across super-communities, no retelling relation, distinct documents. Bridges are `model_asserted` in CORTEX's taxonomy: read plans, never facts. The 160 on the estate [M] are read plans. Bridge enumeration is the one pass that is quadratic in community count, not chunk count (cells = communities²; 15.4M cells at 5,570 communities sweep in 0.04–0.10 s at invariant units [M, CORTEX §6.2]); it is complete, so no sampled "dream" pass is needed (the verifier paradox: anything a sampler could verify, enumeration already finds).

### 6.6 Firing
```
fire(seed, hops=3): a0 = span-projected dense top-m ∪ exact lexical hits ∪ nodes already in the window
  mask scope before any top-k
  a ← α Σ_r w_r · SpMSpV(T_r, a) + (1-α-β) a0      # PPR restart on the sparse frontier; 0.15–0.3 ms at spec sizing vs 7–17 ms dense [M, CORTEX]
  k-WTA; hub suppression by 1/log(degree); time decay
returns a read plan + salience annotation + absence markers, never an answer
```
Slice weights and hop count are learned by the loss (§2.3).

---

## 7 · Attention — the residual loop

### 7.1 Placement
For a new chunk $x$: residual $r = 1 - \max_j \cos(x, X_j)$ excluding the retelling slice; community entropy $H$ of its top-10 neighbours; lane volatility $v$ (EMA of residuals from the same source lane); **priority $p = r/v$** [M, GLANCE-RACE-2]. Verdicts by the learned quantiles (§2.2): RETELLING · ROUTINE · RELATED · BRIDGING · NOVEL. Habituation $P_o = 1/\mathrm{EMA}[r^2]$ per lane. `place` on a 16-chunk document: 3.0 s today [M]; the native path (§10) targets ≤ 100 ms.

### 7.2 Novelty at the claim grain
The chunk residual is the cheap gate; a chunk that passes is decomposed into atomic claims and each is checked against the position ledger and an atomic-claim bank, salience-weighted (NovAScore's shape: 0.626 point-biserial with human novelty) [V] arXiv:2409.09249; a running-centroid distance ranks but never decides (orthogonal to quality, r = −0.002) [V] arXiv:2603.01791; near-duplicate paraphrase runs as a hashing → attention-weighted MinHash → adjudication cascade at < 1 % neural cost [V] arXiv:2607.01601; LLM-extracted entity graphs are too noisy to carry this (Graphiti's own dedup F1 0.674) [V], so retelling detection runs on claims and spans.

### 7.3 Fronts, vigilance, habituation (the two rates)
Per lane, a CUSUM on the residual series ($k = 0.5\sigma$, $h = 5\sigma$ on the trailing window) declares a **front** when residual exceeds the trailing 90th percentile for m consecutive documents and closes it when the retelling share exceeds its trailing 90th percentile. In a front: a NOVEL chunk becomes a **provisional community** immediately (so the map can hold it), confirmed when $m = 3$ independent witnesses (documents or channels) fall within cosine 0.6 of it, dissolved back into the overflow bucket otherwise. Out of a front: habituation decays attention on the lane. The estate's measured fronts (§0) are the first receipt for this rule.

### 7.4 Contextual intake and the write-back
A chunk with $p$ above the learned bar is read **with its map slice** (community gist, neighbours' headers, era, the unit map line) by gear one (local reader) or gear two (GLM-5.3-Flash), emitting a **typed delta** (§9.3) and a card whose quotes are located in the tape by the fence. A retelling gets no read. Precision-weighted positions: a position's update step is $\Delta \propto 1/\text{corroboration}$; single-source claims carry `single_source` on every stamp. Supersession is proposed and scored by the future (§2.6). Anti-capture floors run on a budget the loss cannot starve: a systematic permuted sweep of every chunk once per period (14.9× cheaper than random for the same guarantee [D, CORTEX]), a reverse-order fold, a null-prior occasion, a 2 % ε-reserve in every read plan, and a nightly attention audit that grades what placement refused to read against next-day citations with planted probes synthesised from held-out provenance pairs (no human labels).

### 7.5 The unit map and the pages (always total, rebuildable)
A 4,000-token (envelope 2–8k) deterministic rendering: the kernel line, the partition tree (one line per T³, a counts line per T²), the ten freshest NOVEL placements, open contradictions, the forgotten list (cited early, absent late), open fronts, the vintage. Every tape day is inside some line at some depth (F-UNIT). Regenerated nightly; **the diff is a first-class artifact**, taped and rendered as the atlas-diff overlay; it is the pinned prefix of every session and rescan. Below it, **pages**: one per community and one per topic articulation, each with `{model_fp, prompt_hash, sources, vintage}` so a newer model re-derives by replaying raw → claims → page (the LLM-wiki pattern; one published instance ran 15,259 PDFs → 16,294 pages with a supersede check and a lint pass) [V] gist joonan30 rev 2026-08. Merging upward feeds source passages, not only child summaries (recursive merging amplifies hallucination past 100K tokens) [V] arXiv:2502.00977. Sleep-time consolidation is the cadence (≈ 5× less test-time compute at equal accuracy; the benefit grows with query predictability) [V] arXiv:2504.13171.

---

## 8 · Recall and the rescan

### 8.1 Rungs, stamps, the router law
| Rung | Mechanism | Cost | Guarantee |
|---|---|---|---|
| R0 | unit map in the prefix | 0 | always-total at stated resolution |
| R1 | FTS5 BM25 + typed joins (timeline, containment, provenance) | ms | exact over extracted structure |
| R1+ | firing merged into R1, contribution stamped | ms | importance-sampled *where* |
| R2 | two-pass dense ∥ BM25 → CC → reranker (gated) → spans from the tape | 0.5–2 s | exact spans, partial coverage |
| R3 | dossier sweep: the hyperbolic ball around the topic, contrarian seat on dark cells | ¢–$ | exact within scope |
| R4 | full sweep of a scope (gear two, batch) | $ | exhaustive |
Every answer carries `stamps = {rungs, coverage n/N, fidelity, cost, single_source, insufficient_rung}`; quantifier questions resolve at ≥ R3 or return `INSUFFICIENT_RUNG` [M]. **Router law from the 2026 benchmarks:** fact questions go to R2 flat; "what do I hold on X" goes to R3 pages and firing; a lookup never goes through the tree (§3). The router's shape classifier is learned by the loss under caps.

### 8.2 The rescan loop (new model, same corpus)
```
scope(topic)   → the hyperbolic ball: communities whose gist or top terms hit the topic, plus provenance-linked sessions
skeleton       → dossier: timeline (retellings collapsed to earliest), communities, eras, bridges out, dark matter (never-cited spans),
                 contested positions, the forgotten, open fronts, read_plan_first. Pinned prefix ≈ 20–60k tokens.
attend         → reads by residual against the skeleton, budget along ρ; one contrarian seat on the darkest cells;
                 distill-and-evict: every read leaves a note with a span ref; each call ≤ 128K–200K tokens (§3)
articulate     → claims with quotes; quotes located in the tape by the fence, never trusted from the model
reproject      → every view (document, session) scored for residual against the articulation:
                 reconciled | superseded (with the superseding span) | branch (a live alternative) | forgotten (never re-derived)
vintage + diff → articulation vN with model_fp and receipts; diff against vN−1 by section; the diff is the deliverable
```
**Accuracy ladder:** receipt-closed claim > independently corroborated (m ≥ 2 independent documents) > supersession-aware reconstruction > lone narrative; retellings weightless. **Testimony:** the system can prove what the operator said, never what they believe; `current_position` returns the whole chain with its contradictions; self-contradiction across years is the most valuable structure the corpus holds (CORTEX I-V5-POSITION). **Elicitation:** contested positions and the forgotten become questions; answers append to the tape as dated testimony.

**The label-free score of an articulation (F-VINTAGE):** hold out the documents after t; an articulation built from the field at t is better than another iff it lowers the reprojection residual of the held-out documents (their claims are already in the articulation, or superseded by it, rather than absent). A newer model earns its price by that number, not by a rater; blind ratings are welcome as extra tape.

**Instruments and windows:** Opus 5 by default (91.3 % at 128K, first by AUC); Fable 5.1 when an Opus run falls short on the future-residual score (+2.2 ProgramBench points at the full window for 2× the price; cache reads 0.025×); never Opus 4.7 (0.5–1.4 %); never Haiku 4.5 (200K, 4,096-token cache minimum, retiring not before 2026-10-15). Gear-two readers: GLM-5.3-Flash or DeepSeek V4 Flash (62.9 % at 128K, enough for chunked reads) or the local Qwen3.8-27B. GPT-5.6 Sol (92.4 %) is an alternative at $4/$0.40/$20 through 2026-11-21 with a 2× input / 1.5× output surcharge above 272K and a 922K input cap [V]. Fable access was suspended 2026-06-12 to 2026-07-01, so the Opus fallback is wired, not assumed [V] anthropic.com/news/redeploying-fable-5. Long context is the right tool exactly over a curated bundle (EvoMemBench; MemDelta full-context 49.8 vs verbatim RAG 47.2, p = 0.34) [V]; recite-then-answer adds up to 4 points [V] arXiv:2510.05381; distill-and-evict is the frontier (Chroma Context-1; Still, 8–200× KV compaction) [V]; Cartridges (topic KV caches) are a future gear that needs weights, and topic bundles stay cartridge-ready [V] arXiv:2506.06266.

**Cost of one rescan [D]:** skeleton 40k pinned + 150 reads × 2k + 20k out: ≈ $0.03 on GLM-5.3-Flash promo; ≈ $2.2 on Opus 5 (less with the skeleton cached); ≈ $4.4 first on Fable 5.1, then skeleton reads at $0.25/M.

---

## 9 · The corpus callosum — agents on Intercom with one sentry

### 9.1 The diagnosis
Intercom v0.2.3 (lanes, `await`, `claim/release` CAS, `handoff/takeover` capsules, `pin`, `replay --json`, the relay firewall, the doorbell contract: run `check --me` at end of turn, inject non-empty output) [V] C:/Intercom. Writes are milliseconds; polling is 0.03 ms per poll against 108 ms of process overhead [M, NOTES v0.1.8]. The lag is **composition** (minutes to write a message), **polling** (turn boundaries), **per-look cost** (a forward pass over a growing log). Operator ruling: ≤ 10 concurrent subagents, stagger waves [V] reference-intercom-bus.md.

### 9.2 The sentry (gear one, world rate)
One daemon principal `connectome-sentry` per bus: tails every registered room from its cursors at 250 ms (hint best-effort, cursor truth); **places** every new message into the field; **judges** with Tier-0 rules first, then one shared local judge only above the residual bar (hypercelld's measured lesson: naive watching costs ~10× turn-based; ticks and retellings never wake a model; one sentry per bus, not per watcher); **routes by residual per lane** (a finding is forwarded only where it is NOVEL or BRIDGING relative to that lane's own partition paths, which is what keeps effective seat count up: measured seat correlation 0.5–0.9 gives K_eff 1.1–1.6 for four [M, CORTEX §8.5]); **emits typed verdicts, never prose** (`x-sentry {decision, cited_ids, residual, community, lane_targets}` as directed priority-1 messages so `check`, the Stop-hook and `await --for-me` ring; a per-lane digest ≤ 10k tokens, blake2b-pinned, rewritten only on note|wake; a suppressed wake leaves an audit row); **composes for the team** (subagents post evidence, the sentry writes the prose). Types stay `x-` until adopted by a spec bump.

### 9.3 Typed deltas (one grammar, three consumers)
`{introduced | changed | contradicted | reinforced | unresolved} × {entity, predicate, polarity, t_valid, span_refs[], lane}`, program-appliable; replaying the stream reproduces the digest byte-for-byte. The rescan's reprojection, the sentry, and the position ledger all speak it.

### 9.4 Workers: the DeepSeek harness
Workers run on the operator's clone of the DeepSeek harness (`C:/deepseek-harness-master`, MIT; to be copied into `C:/sandbox/` for the build): `dsh --profile headless "job"` runs one persisted session and prints the answer; `dsh --profile sdk` serves JSON-RPC over stdio to the Python package `deepseek-harness-sdk` (0.1.2a3, 2026-09-01), which bundles the runtime; profiles are ordered stacks of plugin-bundle patch layers, so the connectome's tools ride as a profile, not a fork [V] C:/deepseek-harness-master/apps/cli/README.md, python/README.md. Scriptorium's harness lane (laws HM-1..HM-10, chars/4 metering at the pricebook) is the precedent. Claude Code (`claude --bare -p … --json-schema … --max-budget-usd`) and OpenCode (`opencode run --format json`, any OpenAI-compatible endpoint as a provider) are the other two lanes; all three are metered by the same pricebook.

### 9.5 Laws and the null
Relay firewall (the sentry's messages are data; only the operator's keyed `relay` directs); native wake; wake budget per lane; trust-tagged frames; partial view (no two lanes get the same digest); diversity by partition path; the contrarian seat. **F-RESIDENT [BET]:** the same swarm under (a) plain polling, (b) a cron digest script with no model, (c) the sentry; measures: time from a planted finding's first post to its presence in every other lane's next turn (bus logs), refeed fraction (transcripts), lane diversity (embedding spread of final findings); kill: if (b) matches (c), the sentry is a script and ships as one.

### 9.6 The FUSOR seam, honestly
When FUSOR's resident lane exists, the resident replaces the sentry's judge with a trunk-resident model at token rate holding the bus, the unit map and the digests as its prefix. The literature has neighbours, each verified at arXiv on 2026-09-03: stateful serving with a persistent KV across tool turns plus a radix prefix cache across interleaved multi-agent traffic (2.1× per turn, 4.2× on the median turn of a 35-turn workflow; "stateful reuse and speculation, not caching") [V] arXiv:2605.26289; KV time-to-live retention across tool pauses (> 8× job completion) [V] arXiv:2511.02230; prefix-aware eviction for coding agents (2–2.6× fewer evictions, 3.5× faster sessions) [V] arXiv:2606.16824; per-agent Q4 KV persisted to disk on an M4 Pro (time-to-first-token 22–136×) [V] arXiv:2603.04428; quantised KV handoff between agents (397 vs 1,030 ms at 8K, with its own call for stronger ablations) [V] arXiv:2605.03884; a survey of eighteen latent-communication methods with no benchmark [V] arXiv:2606.05711. All reuse or hand off a KV cache between turns or agents; **none implements one resident trunk many heads read at token rate while it keeps ingesting.** The prefix-reuse half of FUSOR's claim is real and cheap (gear one's `--cache-ram` re-prefills in 16 ms [M]); the always-on resident half is the operator's bet, and F-RESIDENT is its kill. Prefix-sharing for ten workers on one 100K prefix within TTL [D]: Fable 5.1 $10 → $1.48; Opus 5 $5 → $1.08; Sonnet 5 $2 → $0.43; GPT-5.6 Sol $4 → $0.86; DeepSeek V4 Flash $0.22 → $0.03; local ≈ $0.

---

## 10 · The native core and the viewer (C++/CUDA, no browser, no Vulkan)

### 10.1 Why native, and the conventions it inherits
The processing hot path and the viewer are native C++20 / CUDA 17, built the way the operator's own repos are built: CMake ≥ 3.27, `CMAKE_CUDA_ARCHITECTURES 89 90 120` (Ada, Hopper, Blackwell), static CUDA and MSVC runtimes so the executable ships alone, GLFW 3.4 + GLAD + Dear ImGui via FetchContent, Ninja from the VS 2022 developer shell, OptiX optional [M, C:/Buddhabrot_CUDA/CMakeLists.txt]; determinism rules from the booster core: `-fmad=false` where results feed fingerprints, no float atomics on reduction paths, fixed-topology block reductions then a serial fold in ascending block order, Philox counter-based seeds, per-architecture bit-identity as the hard gate and CPU↔GPU parity toleranced [M, C:/Booster_Lander_Simulator/core/guidance_mppi_cuda.cu]; a frame loop that never blocks (two prioritised streams: presentation never waits on compute; view changes crossfade from a reprojection of the previous frame; 143 fps vsync-locked in Buddhabrot v4) [M, C:/Buddhabrot_CUDA/README.md]; procedural scenes with a local-LLM director off the frame thread and bit-identical replay of every AI decision as a recorded event [M, C:/backrooms/README.md]. The browser page shipped in v0.1 becomes a thin export, not the product.

### 10.2 Modules
| Module | Owns | Hot-path kernels |
|---|---|---|
| `cx-tape` | the tape, chunker seam, FTS5 / native inverted index, journal | blake2b chain; n-gram provenance matcher |
| `cx-index` | vectors (coarse head in VRAM, full int8 on NVMe-mapped memory), two-pass scan, CC fusion, reranker seam | int8 GEMM + top-k; rescoring gather; BM25 scoring |
| `cx-field` | slices (CSR/CSC), support gating, firing, partition assignment, bounded refinement, bridges, ledgers | SpMSpV PPR; kNN on the coarse head; centroid assignment; community-pair sweep |
| `cx-place` | residual, verdicts, priority, fronts (CUSUM), habituation | batched cosine against the field; per-lane EMA |
| `cx-map` | Lorentz coordinates, analytic placement, Procrustes + hysteresis, LOD | O(n) placement; boost matrices; Poincaré projection |
| `cx-view` | the viewer: GLFW/OpenGL 4.6 window, CUDA–GL interop buffers, instanced quads or impostor spheres, id-buffer picking, ImGui inspector, time slider, atlas-diff overlay, focus-and-context by one Lorentz boost uniform | instance buffer write; density texture for the rim; picking |
| `cx-serve` | MCP server (stateless, 2026-07-28; stdio and Streamable HTTP; a 2025-11-25 fallback handshake), pricebook, meters | — |
| `cx-sentry` | the Intercom daemon (Python first, native later) | — |
Cold paths that stay in Python at version events: UMAP-3 angles (cuML), consensus Leiden (leidenalg/igraph), page and name generation (gear one/two), embedding under transformers (WeMM) or llama.cpp (Qwen3). The seam between hot and cold is the store on disk; nothing hot imports Python.

### 10.3 VRAM and scale tiers
Coarse heads (128-d int8) resident for every profile in §4.3 (0.5 MB → 2.5 GB); full 1024-d int8 resident up to the raw personal archive (3.5 GB) and NVMe-mapped beyond; CSR slices ≈ 50 nnz per node (≈ 8 bytes each: 2×10⁷ nodes → 8 GB, host-resident with a VRAM working set by community); render buffers ≈ 32 bytes per instance for ≤ 2M instances (64 MB) plus the density texture. The card is shared with a reader or an embedder, never both at once; the arbitration rule is measured free VRAM at start (CORTEX §13.9).

### 10.4 The viewer, functional first
Poincaré ball (canonical, focus-and-context), Euclidean cloud, per-slice layers, community hulls, bridges as amber arcs, retellings as dim ghosts; time slider = tape replay; atlas-diff overlay; inspector with verbatim spans, stamps, the provenance chain (session → document) and the position chain with contradictions; labels by zoom with de-overlap; never free prose inside the map (unit-map lines are render-normalised, imperative patterns stripped). Prior art checked 2026-09-03: no project renders embedding-similarity edges in 3-D over a person's documents (all six Obsidian 3-D plugins draw wikilinks; the semantic visualisers are 2-D; the 3-D memory viewers render snippets or triples), and every 3-D tool re-runs a force simulation from random seeds per session [V] `docs/sota/SOTA_second-brain-prior-art_2026-09-03.md`. Performance references: Embedding Atlas holds 60 fps to 4M points on an M1 Pro [V] arXiv:2505.06386; SuperSplat renders 10M splats at 124 fps on an M4 Max [V]; a native CUDA viewer on this card should exceed both. **F-3D-VS-2D** is label-free: time-to-find for links synthesised from held-out provenance pairs, ball versus 2-D, from interaction logs.

### 10.5 Tools for the build sessions
`C:/kernel.sh` (the operator's browser) for the web, `C:/fetcher` for Hugging Face downloads, `C:/peek` for localhost, sockets and anything a harness fences off; `C:/chunker`, `C:/everywhere`, `C:/everything`, `C:/Intercom` at their fixed paths as subprocesses, never imported; the DeepSeek harness clone in `C:/sandbox/` as the worker runtime. Forward slashes in every shell command.

---

## 11 · Economics (two gears, priced on today's sheets) [V/D]

| Job | Gear | Model | Estate today | 172M-token archive |
|---|---|---|---|---|
| Embeddings | one | WeMM-4B / Qwen3-Embedding-4B, local | 12 min | 15 h |
| Rerank | one | Qwen3-Reranker-4B, local | — | — |
| Chunk context on high-residual chunks | two | GLM-5.3-Flash | $0.27 | $19 |
| Cards for NOVEL/BRIDGING chunks (≈ 20 %) | two | GLM-5.3-Flash | $0.10 | $8 |
| Unit map, pages, names, nightly | one | Qwen3.8-27B / 9B local | $0 | $0 |
| Sentry judge (residual-gated) | one | local | $0 | $0 |
| Rescan of one topic | two | Opus 5 / Fable 5.1 / Flash | $0.03–$4.4 | same |
| Vision (screenshots, PDF pages) | one/two | WeMM (embed) · GLM-5.3-Flash or DeepSeek Vision-Exp (read) | pennies | dollars |

| Lane | Miss / hit / out per 1M tokens | Notes (fetched 2026-09-03) |
|---|---|---|
| GLM-5.3-Flash | 0.075 / 0.015 / 0.25 promo to 2026-09-09, then 0.15 / 0.03 / 0.50 | 1M / 128K; native multimodal; 62.9 % at 128K; MIT weights |
| GLM-5.3 | 1.40 / 0.26 / 4.40 | 69.3 % at 128K |
| DeepSeek V4 Flash (0731) | 0.22 / 0.007 / 0.66 off-peak, ×2 peak | 1M / 384K; Vision-Exp at the same price, ≤ 384 billable tokens per image |
| DeepSeek V4 Pro (0813) | 0.66 / 0.022 / 1.98 off-peak | 60.4 % at 128K: not better than Flash for reading |
| Claude Fable 5.1 | 10 / 0.25 / 50 | cache read 0.025×; min 512; availability risk |
| Claude Opus 5 | 5 / 0.50 / 25 | 91.3 % at 128K; the synthesis default |
| Claude Sonnet 5 | 2 / 0.20 / 10 | 52.9 % at 128K; cards, not synthesis; cache min 1,024 |
| Claude Haiku 4.5 | 1 / 0.10 / 5 | not used |
| GPT-5.6 Sol | 4 / 0.40 / 20 promo to 2026-11-21 | 922K input cap; 2× / 1.5× above 272K; 30-min cache |
| Gemini 3.8 Flash | 0.75 / 0.075 / 3.75 (doubles 2027-01-01) | multimodal incl. audio and PDF; explicit-cache storage $0.50 per M tokens per hour |
| Kimi K3 | 3 / 0.30 / 15 | 38.3 % at 128K; revenue-triggered licence |
| Qwen3.8-Max / Qwen3.8-27B hosted | 2 / 0.25 / 6 · from 0.25 / – / 2.20 | 92.3 % / 81.8 % at 128K; 27B Apache-2.0 |
| Local llama-server | 0 | Qwen3.5-9B for ≤ 32K chunks; Qwen3.8-27B IQ3/Q3 for quality |
**Pricebook law:** every row carries date and URL; an undated or unknown lane is refused; promos are booked with their end date (three rows expire within ninety days); only vendor pages are booked.

---

## 12 · Evidence without labels

Every falsifier below is computable from the tape, the bus logs, and the interaction logs. Thresholds are registered in `connectome.lock` before the runs, as quantiles or ratios, never as absolute numbers a person chose.

| Falsifier | Claim killed if | Measure (no labels) | First number |
|---|---|---|---|
| **F-CONVERGE** (master) | the field does not learn its corpus | per-document residual against the time-ordered field vs a shuffled field at matched size, by arrival decile; within-front residual must fall and retelling share rise; between fronts the vigilance rule must open structure the future confirms | time-ordered beats shuffled at −27 %, −17 % (first two deciles) and −14 % (last); loses by +3…+21 % mid-span, where fronts opened; newest decile 23 % retellings [M, 264 docs] |
| **F-REFEED** | the connectome is a picture | share of operator tokens that are context re-supply, from transcripts, two weeks before vs after sessions carry `unit_map` + `recall` | not yet run |
| **F-EMBED / F-PREFIX / F-CHUNK** | a choice is noise | future residual and provenance-pair recall (12-gram goldens are free and lexical by construction, so BM25 is their ceiling) under each choice | prefix: +3.5 pts recall@1/10/20, n = 28 [M] |
| **F-RENT** | a signal is decoration | ablate the signal; future residual and provenance recall must worsen beyond the registered margin | not yet run |
| **F-PLACE** | verdicts are theatre | chunks called NOVEL must acquire future neighbours and future citations at a higher rate than ROUTINE; RETELLING must acquire none; the uniform-sampling arm must lose | not yet run |
| **F-LAYOUT-STABLE** | the map reshuffles | frozen partition ARI ≥ 0.95 under a quarter of growth (fresh Leiden measured 0.76 [M]); median displacement ≤ 2 % of radius per build | seeds: 0.73–0.86; +2 %: 0.76 [M] |
| **F-BRIDGE / F-NOVEL** | bridges or novelty are noise | links synthesised from held-out provenance pairs are recovered at the registered rate; false-bridge rate on retellings = 0; planted documents (held-out retellings vs held-out new fronts) separate | not yet run |
| **F-VINTAGE** | a smarter model buys nothing | reprojection residual of held-out documents against articulations from two instruments on the same skeleton | not yet run |
| **F-OVERFLOW** | never-overflows is a slogan | a 10× inflated twin keeps the unit map ≤ 8k tokens, `place` ≤ 5 s (native ≤ 100 ms), recall p95 ≤ 2 s | not yet run |
| **F-RESIDENT** | the sentry is a script | §9.5 | not yet run |
| **F-SPANS** | quotes are fiction | fence catch rate on model-synthesised paraphrase-as-quote ≥ the Scriptorium floor (28.5 % on raw) | fence exists [M] |
| **F-PROBE** | model comparisons are confounded | per-model effective window on this corpus with a no-lexical-overlap arm, before F-VINTAGE | not yet run |
| **F-3D-VS-2D** | 3-D is decoration | §10.4 | not yet run |
| **F-CONTROL** | a dumb twin is as good | BM25 + keyword-graph twin and an off-the-shelf memory product fed the same files, scored by the same future-residual and provenance measures | not yet run |
Probe design follows MemTrace (fact × age × current/earlier/trajectory × evidence present/missing/contradicted; when systems fail the evidence was retrievable ten times more often than missing) [V] arXiv:2606.17328; the scoring target is stated with every number (target choice alone changes nDCG on 83–94 % of queries) [V] arXiv:2605.24060; dense-versus-lexical lift is measured with the BM25 floor pinned by construction [V] arXiv:2605.29630; leaderboards are not evidence (LoCoMo fits inside every window; LoCoMo-Plus drops the same models ≈ 20 points) [V].

---

## 13 · Build order, machine-gated (the way the operator's native repos are built)

There is no kickoff document during the build. Each milestone has a gate script that exits 0 or the milestone is not done; a fresh session reads this file, the receipt, and the gate log, and continues. A per-use-case kickoff (a writer's vault, a firm's matters) is written **after** the organ exists, from the schema induction of that corpus.

**Exists [M]:** `connectome.py` (build, ask, place, codex, dossier, render, mcp, providers) with stamps and quantifier pinning; the proto caches; the page; F-PREFIX and F-CONVERGE first numbers; the Louvain and δ measurements.

- **M0 · Native skeleton. ✓ PASSING (2026-09-03).** CMake project in the Buddhabrot conventions; `cx-index`'s int8 two-pass scan with a resident device matrix and a deterministic top-k; contract headers for `cx-tape`, `cx-field`, `cx-map`, `cx-place` compiled and invariant-checked; a `doctor` verb (device, model-server ports, fixed-path organs, corpus). *Gate:* `scripts/gate.ps1 -Milestone M0` — 5/5 ctest (parity, determinism, tie-break, planted-row two-pass, contracts), cross-process digest `9574b5dae6191b39` identical in two separate processes, doctor reporting. Receipt and numbers: `native/README.md`. *Carried to M1:* the tape reader itself (the scan currently runs on a synthetic corpus and on vectors handed to it).
- **M1 · The loss. ✓ PASSING (2026-09-03).** The temporal-holdout harness (`harness/`): arrival order from the tape with no guessed dates, the residual curve, F-CONVERGE against shuffled controls at matched size, and window-vs-trailing front detection. *Gate:* `scripts/gate.ps1 -Milestone M1` — the harness's own acceptance tests (no-lookahead under truncation, determinism and block-size independence, a planted front recovered at position 54 against 59, the four degenerate corpora, order-matters), then F-CONVERGE and the front detector on the live estate. §0's numbers reproduce. **One front detected**, opening 2026-08-10 at `MEANDER-SPEC-v0.1` and running 21 documents through the BLACKBOX burst of 08-16/17, which sits precisely in the deciles where the shuffled control wins: the loss and the detector agree from independent directions. Receipt: `harness/README.md`. *Carried to M2:* F-EMBED, F-PREFIX and F-CHUNK arms (the embedder seam is written and the local server is up; the comparison needs a second embedder pulled and a re-embed of the corpus).
- **M2 · The frozen field.** Consensus Leiden partition/v1 with hierarchy and names; assignment and bounded refinement; the drift meter; provenance slice; support gating; the position ledger with typed operators and audit rows. *Gate:* F-LAYOUT-STABLE on a quarter of simulated growth (held-out documents replayed in time order).
- **M3 · The map and the viewer.** UMAP-3 angles at version events; analytic Lorentz placement; Procrustes and hysteresis; `cx-view` with the ball, layers, time slider, inspector, id picking. *Gate:* 60 fps at the estate's size and at a 10× synthetic inflation; F-3D-VS-2D harness runnable.
- **M4 · Attention.** `cx-place` with learned quantiles, fronts (CUSUM), vigilance, habituation, contextual intake with typed deltas, the unit map with diff, pages. *Gate:* F-PLACE and F-NOVEL on held-out documents; F-UNIT hole test.
- **M5 · The rescan.** Dossier → pinned skeleton → hyperbolic-ball reads → fence-derived spans → reprojection → vintage and diff; elicitation questions; F-PROBE per instrument. *Gate:* F-VINTAGE on FUSOR under two instruments scored by held-out reprojection residual.
- **M6 · The bus.** `cx-sentry` on Intercom with typed verdicts and per-lane digests; DSH profile with the connectome's tools; F-RESIDENT arms (a)/(b)/(c). *Gate:* propagation and diversity numbers from the bus logs.
- **M7 · Scale.** The 172M-token extracted archive (≈ 15 h embed), then the 10¹⁰ profile on a synthetic twin: NVMe-mapped vectors, native inverted index, tiered VRAM. *Gate:* F-OVERFLOW.
- **Standing:** F-REFEED measured over two weeks once M4 is live; F-CONTROL beside every run.

---

## 14 · What exists elsewhere, what earlier revisions got wrong, and the limits

**Prior art (2026-09-03):** nothing clonable meets 70 % of the target; Graphiti ≈ 65 % (bi-temporal edges, invalidation, dedup, hybrid search, MCP; no rendering, triples not prose, Docker under WSL here), Cognee ≈ 60 % (embedded SQLite + LanceDB + Kuzu on native Windows; no supersession model, 2-D), claude-obsidian ≈ 55 % (claim ledgers, the LLM-wiki loop; BM25 only, 2-D, Windows writes need WSL), mcp-memory-service ≈ 55 % (3-D view, `contradicts` edges; snippets not documents). Retrieval, rendering, MCP and storage are commodities; fact-grain supersession and dedup are borrowed from Graphiti and Mem0; the unbuilt core is the identity-holding 3-D layout that biases attention plus idea-grain novelty over prose [V] `docs/sota/SOTA_second-brain-prior-art_2026-09-03.md`.

**Wrong in v0.1–v0.3 and in this morning's draft:** re-partitioning every build (14–27 % reshuffle measured); embedding queries without the card's instruction; treating similarity bridges as findings; framing the swarm around reasoning instead of bandwidth; the implicit "8M effective context"; July prices; hand-labelled goldens as a gate; a kickoff brief during implementation; a WebGPU renderer as the product; a hyperbolic optimiser over a space whose δ says it is not a tree; overstating the shared-KV literature as FUSOR's trunk.

**Limits:** the field selects; it does not attend to the corpus at full resolution. A fully cited articulation can still be wrong by omission; corroboration counts and the contrarian seat attack that, nothing closes it. The learning law measures prediction of the corpus's own future, which is what a second brain is for, and is not a proof of truth about the world. Hyperbolic radius encodes level by construction and specificity only as well as the importance score. The sentry moves composition off the heads but cannot make a turn-based head read faster than its turn. Effective context is the binding constraint and it moves with every model version. None of this is real continuity; it is a complete, ordered, relation-aware, honest injection that a new model can trust and drill, and that converges on the corpus it is given.

---

## Appendix A · Evidence table (primary sources, fetched 2026-09-03 unless dated)
| Item | Date | Source | Key number | Changes |
|---|---|---|---|---|
| Convergence, time vs shuffled | 2026-09-03 | this box, 264 docs | −27 / −17 / −14 % first two and last deciles; +3…+21 % mid-span; 23 % retellings newest decile | §0, §2.5, §12 |
| Louvain instability | 2026-09-03 | this box | ARI 0.73–0.86 seeds; 0.76 at +2 % | §3, §6.3 |
| Gromov δ | 2026-09-03 | this box, 2,000 chunks | δ/diam 0.054 p99 (control 0.029) | §3, §6.4 |
| F-PREFIX | 2026-09-03 | this box, n = 28 | recall@10 0.750 → 0.786 | §5.1 |
| Embedding throughput; `place` latency | 2026-09-03 | this box | 18.7 chunks/s; 3.0 s / 16 chunks | §3, §7.1 |
| Native two-pass scan (M0) | 2026-09-03 | this box, `native/`, CUDA 13.1 | resident coarse pass 0.29 ms @ 250k, 2.02 ms @ 2M (102–118 GiB/s); copy-per-query 13.05 ms loses to CPU 9.00 ms; all paths bit-identical | §5.4, §10, §13 |
| Front detection (M1) | 2026-09-03 | this box, `harness/` | one front on the estate: opens 2026-08-10 at MEANDER-SPEC, 21 documents, peak z +1.07 against the trailing field; a per-document CUSUM never fires (max 0.88 vs 5σ) because a front is window-scale | §2.5, §7.3, §13 |
| Local readers; prompt cache; speculation | 2026-09-03 | this box, llama.cpp b9627 | 9B 4,148 / 71; prefix re-prefill 16 ms; draft acceptance 70.8 % for +8 % | §3 |
| WeMM-Embedding-4B / 9B | 2026-08 | huggingface.co/tencent/WeMM-Embedding-4B, -9B; arXiv:2608.24053 | MMEB-v3 58.2 / 59.5; Qwen3.5-based; MRL; Apache-2.0 | §5.1 |
| Qwen3-Embedding family | 2025-06 | huggingface.co/Qwen/Qwen3-Embedding-0.6B | 64.33 / 69.45 / 70.58; `Instruct:…\nQuery:`; docs no prefix | §5.1 |
| Qwen3-Reranker + GGUF fix | 2025-06 / 2026-03 | huggingface.co/Qwen/Qwen3-Reranker-0.6B; gist VooDisss; llama.cpp #16407 | 69.76 MTEB-R; community GGUFs 1e-23 | §5.3 |
| Fusion CC vs RRF | 2022–2026 | arXiv:2210.11934; arXiv:2604.01733 | CC .726 vs RRF .695; rerank .816 | §5.5 |
| Contextual retrieval; chunking; late chunking | 2024–2026 | anthropic.com; arXiv:2603.06976; arXiv:2410.13070; arXiv:2409.04701; arXiv:2504.19754 | −67 % failures; 0.459 vs 0.244; mean pooling required | §4.2 |
| Transcript retrieval | 2026 | arXiv:2605.12493; arXiv:2603.12572; arXiv:2606.04194 | −28.6 pts without raw pool; LMEB −0.496; reranker −6.9 Hit@1 | §4.2, §5.3 |
| HypRAG; HyperbolicRAG; HyBIRD; radius laws | 2010–2026 | arXiv:2602.07739; 2511.18808; 2606.28336; 1006.5169; 1106.0286; 2410.04010; 2211.00181; 2401.13708 | +29 %; +20 % norm; float64; 10⁵ ceiling for optimisers | §3, §6.4 |
| Leiden maintenance and consensus | 2025–2026 | arXiv:2601.08554; 2502.18497; PLOS CS 2025-10-01; arXiv:2603.05207 | 10⁵× faster; 48.8×; 10 seeds / 0.8; non-uniqueness | §3, §6.3 |
| Layout stability primitives | docs | umap-learn (transform, landmarked ParametricUMAP, AlignedUMAP); arXiv:2411.15894 | 1 % landmarks, weight 0.01 | §6.4 |
| Memory literature | 2025–2026 | arXiv:2501.13956; 2606.06240; 2601.07468; 2506.05690; 2604.11628; 2606.29914; 2409.09249; 2607.01601; 2603.23848; 2607.01071; findings-acl.103; 2502.00977; 2504.13171; 2606.17328; 2605.24060; 2605.29630; 2605.09611; 2605.25869; 2605.28009 | as cited | §2, §6, §7, §8, §12 |
| Effective context 2026 | 2026-09-03 | contextarena.ai/?needles=8; Fable 5.1 system card | 128K: Opus 5 91.3, GPT-5.6 Sol 92.4, Qwen3.8-27B 81.8, Flash 62.9, Opus 4.7 ≈ 1; 1M: 63.5 | §3, §8 |
| Swarm and blackboard | 2025–2026 | arXiv:2604.02460; 2510.01285; 2507.01701 | single agent at equal tokens; +13–57 % | §3, §9 |
| Shared-KV neighbours | 2025–2026 | arXiv:2605.26289; 2511.02230; 2606.16824; 2603.04428; 2605.03884; 2606.05711 | 2.1–4.2×; > 8×; 3.5×; 22–136×; 397 vs 1,030 ms; survey | §9.6 |
| Prices | 2026-09-03 | docs.z.ai; api-docs.deepseek.com; platform.claude.com; developers.openai.com; ai.google.dev; platform.kimi.ai; openrouter.ai | as tabled | §3, §11 |
| MCP and harnesses | 2026-07/09 | modelcontextprotocol.io changelog; pypi mcp; npm; code.claude.com; opencode.ai; deepseek-harness docs | stateless; SDK 2.x; dsh profiles | §3, §9.4, §10.2 |
| Native conventions | 2026 | C:/Buddhabrot_CUDA; C:/Booster_Lander_Simulator; C:/backrooms | archs 89/90/120; static runtimes; determinism rules; two-stream frame loop | §10 |
| Scriptorium fence; eye harness; CORTEX measurements | 2026-08/09 | C:/scriptorium/README.md; C:/NEW/eye-harness/; CORTEX v5 | 28.5 % / 12.8 %; 99.7→80.9 vs 64→13; FIND 4.88 ms; SpMSpV 0.15–0.3 ms | §3, §6, §7 |

## Appendix B · Research reports (filed under `docs/sota/`, cited where they changed a decision)
Embeddings and retrieval (46 searches, ~75 fetches) → §4.2, §5. Agent memory and GraphRAG (40 / ~95) → §2.6, §4.1, §6.2, §7.2, §7.5, §8.1, §12. Prior art (25 / ~110 incl. GitHub and PyPI release APIs) → §10.4, §14. Geometry and render (45 / ~80) → §6.4, §10.4. Models, economics and agents (~40 / ~110, Context Arena rendered headless, the Fable 5.1 system card full-text searched, llama-bench and cache tests on this GPU) → §3, §8.2, §9.6, §11. All five ran out of the session's 200-search quota and finished on direct fetches; their unverified items are marked in the files.
