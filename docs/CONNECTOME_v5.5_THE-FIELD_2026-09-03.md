# CONNECTOME v5.5 — The Field
### A meaning-based, true-3-D, live, stable, rescannable second brain over one person's documents and transcripts, engineered from the September 2026 state of the art and from measurements taken on this box

**Revision v5.5 · 2026-09-03 · proposed for build. v4 and v5 skipped by operator directive; v0.1–v0.3 (this repo, 2026-09-01) are lineage. One document; the organ `connectome.py` is implemented against it.**
**Authors:** Bo Chen (the ask: hold, attend, rescan, join; the slide rule; the primer; the corpus callosum; the Pareto screenshot of 2026-08-26) · Claude Fable 5.1 (this synthesis, after reading every pointed document whole — `docs/READING-RECEIPT_2026-09-03.md`, 21 files, 1.2 MB — and 16 direct web fetches plus five research agents on the Sept-2026 frontier).
**Register:** engineering. Every number is tagged **[M]** measured on this box, **[V]** verified on a primary web page (URL + date), **[D]** derived by arithmetic from [M]/[V], or **[BET]** a bet with its kill named. Nothing else is asserted.

---

## 0 · What this is, in one paragraph

A tape of everything the operator has written or said (documents, transcripts), embedded by a state-of-the-art local model into a semantic space, indexed three ways (dense, lexical, graph), partitioned once into a frozen community tree that grows by assignment instead of reshuffling, laid out in **hyperbolic space so that radius is resolution** (the unit map at the center, communities around it, chunks toward the rim, detail growing exponentially with distance from wherever you look), rendered in true 3-D in a browser, and driven by one loop: **every new document is placed against the field, its residual decides how much attention it earns, what it changes is written back as typed deltas, and the shape of the field biases what gets read next.** A newer model re-derives any topic from the skeleton plus surgical reads instead of re-reading the corpus. Agents share the field through Intercom, with one always-on sentry so a finding by one head is in every other head's next turn. Everything is rebuildable from the tape; nothing above the tape is truth.

**Today [M]:** 264 documents, 3,585 chunks, 17,828 transcript messages, seven relation slices, 160 bridges, 590 retellings, a working page in two geometries, an MCP server, and a place verdict in 3.0 s. **What v5.5 changes:** the embedder (0.6B → 4B/8B with the instruct prefix the model card requires), the index (Matryoshka two-pass int8 GEMM), the partition (frozen, versioned, assigned), the geometry (Lorentz fit with radius = level, focus-and-context navigation), contextual and late chunking, a local reranker, typed deltas, the sentry on the bus, a stateless MCP server on the 2026-07-28 spec, the Pareto-frontier gear-two model, and a falsifier plan with control arms.

---

## 1 · The four asks and the four answers

| Ask (operator, verbatim gist) | Answer in v5.5 | Where |
|---|---|---|
| **Hold:** keep adding forever, never overflow, compress organically like a lifetime, structure = identity | Tape + frozen partition tree + always-total unit map + hyperbolic radius-as-resolution + curriculum and vigilance | §3, §5, §6 |
| **Attend:** new material read through what is already known; structure biases attention; open but not flipped overnight | Residual-gated placement, priority r/v, contextual intake with map slice, precision-weighted updates, drift alarm with operator countersign | §6 |
| **Rescan:** a smarter model re-derives the sharpest articulation of a topic without re-reading everything | Dossier skeleton as pinned prefix → hyperbolic-ball reads → claims with derived spans → reprojection → vintage + diff | §7 |
| **Join:** N subagents = N× read rate; Intercom is the corpus callosum; the bus is too slow at turn rate | Bandwidth law, the sentry (gear one at world rate) on Intercom, typed deltas, residual-gated routing, FUSOR seam | §8 |

---

## 2 · The physics that constrains everything (2026 numbers)

- **Advertised context ≠ effective context.** NoLiMa (ICML 2025): where the question shares no words with the evidence, effective length collapses to 1K–8K tokens for most models; RULER median ≈ 25 % of advertised; Chroma's context-rot report: smooth monotone degradation, primacy-dominant. [V] arXiv:2502.05167; carried into CORTEX v5 §1.7 with primaries opened. None of those three has 2026 models in its table; the only live 2026 measurement is **Context Arena's 8-needle MRCR v2 (rendered 2026-09-03):** at 128K, GPT-5.6 Sol 92.4 %, Qwen3.8-Max 92.3 %, **Claude Opus 5 91.3 % (AUC to 128K 97.5 %, first)**, Gemini 3.7 Flash 88.6 %, **Qwen3.8-27B 81.8 % (open weights)**, Opus 4.8 75.2 %, GLM-5.3 69.3 %, **GLM-5.3-Flash 62.9 %, DeepSeek V4 Flash 62.9 %**, Sonnet 5 52.9 %, Kimi K3 38.3 %, Qwen3.5-9B 15.4 %, Haiku 4.5 13.8 %, and **Claude Opus 4.7 0.5–1.4 % at every effort**; at exactly 1M the best run is Gemini 3.7 Flash at 63.5 % and most models have not been run [V] contextarena.ai/?needles=8. The Fable 5.1 system card (2026-09-01, 212 pp) reports no MRCR at all; its long-window evidence is ProgramBench at the full 1M window: Fable 5.1 87.6 %, Fable 5 86.3 %, Opus 5 85.4 % [V] anthropic.com system card §8.11. **Law for this design:** 128K–256K is the ceiling for reliable multi-fact recall; 1M is storage, not reasoning. **Consequence:** eight 1M-token subagents are eight times the *read rate* and eight times the *addressable* index, not an 8M-token synthesis window. The notes carry the memory; the field carries the notes. The multi-agent literature says the same thing from the other side: at equal thinking tokens a single agent beats a swarm on multi-hop reasoning, and a swarm is competitive only where the single agent's effective context is degraded or more compute is spent [V] arXiv:2604.02460 (2026-04); reading a corpus larger than any effective window is exactly that case, and blackboard designs (a shared workspace, which is what Intercom plus the sentry is) report +13–57 % task success with fewer tokens than agent-to-agent chatter [V] arXiv:2510.01285, arXiv:2507.01701.
- **Reading is cheap; re-reading is a line item.** GLM-5.3-Flash: $0.075 in / $0.015 cached / $0.25 out per 1M tokens (50 % promo until 2026-09-09 24:00 UTC+8; then $0.15 / $0.03 / $0.50), 1M context, 128K output, native video/image/text/file, thinking cannot be disabled. [V] docs.z.ai/guides/overview/pricing and /guides/vlm/glm-5.3-flash, fetched 2026-09-03. Artificial Analysis Intelligence Index v4.1.1 (2026-08-26): GLM-5.3-Flash 57 points at $0.045/task, on the Pareto frontier; DeepSeek V4 Flash 0731 ≈ 52 at ≈ $0.09; Claude Opus 5 (max) ≈ 63 at ≈ $2.3. [V] operator screenshot 2026-09-03. DeepSeek V4 Flash now: $0.22 / $0.007 / $0.66 off-peak, double at peak (01–04, 06–10 UTC weekdays), 1M context, 384K out, 2,500 concurrency. [V] api-docs.deepseek.com/quick_start/pricing 2026-09-03. **The $0.14 / $0.0028 / $0.28 figures in Scriptorium and CORTEX are stale.**
- **Cache reads are the cheapest tokens on earth.** Anthropic: Fable 5.1 $10 in / **$0.25 cache read (0.025×)** / $50 out; Opus 5 $5 / $0.50 / $25; Sonnet 5 $2 / $0.20 / $10; Haiku 4.5 $1 / $0.10 / $5; 5-min write 1.25×, 1-h write 2×; batch 50 %; full 1M window at standard price. [V] platform.claude.com/docs/en/about-claude/pricing 2026-09-03. **Consequence:** a pinned skeleton (unit map + dossier) re-read fifty times costs less than one cold read. The rescan is a cached-prefix workload by design.
- **Local is free and fast enough.** This box: qwen3-embedding-0.6b-q8_0 on llama.cpp :8092 embeds **18.7 chunks/s of ~700 tokens (13.1k tokens/s)** [M]; a 3,585×3,585 cosine GEMM takes 73 ms on CPU [M]; CORTEX measured FIND over 1.67M×384 vectors in 4.88 ms on the GPU [M, CORTEX §1 bootstrap]. **Readers, measured on this card with llama.cpp b9627 while the resident embedder and browsers held 9.8 GB and ≈ 33 % load (so lower bounds) [M, 2026-09-03]:** Qwen3.5-9B Q5_K_M 4,148 tok/s prefill and 71 tok/s generation; Qwen3.5-4B Q4_K_M 6,864 / 123; Qwen3-8B Q4_K_M 5,440 / 90; a 1,664-token prefix re-sent with `cache_prompt: true` re-prefilled **1 token in 16 ms** instead of 1,664 in 332 ms; speculative decoding with a 1.7B draft accepted 70.8 % of tokens for only +8 % speed on a shared GPU. Prefill is compute-bound at ≈ 5–7k tok/s for 4–9B dense models, so a 100K-token document is a 15–25 s read at $0. **The best open reader at 128K is Qwen3.8-27B** (Apache-2.0, 2026-08-14, 262K native, image + video, 81.8 % on 8-needle at low effort); it fits resident at IQ3_XXS (10.9 GB) or Q3_K_XL (13.1 GB), not at Q4_K_M (16.5 GB), and should generate ≈ 33–40 tok/s here by bandwidth [D]. Gemma 4 26B-A4B (IQ4_XS 13.6 GB, 3.8B active, 256K, image) is the speed option; Qwen3.5-9B stays the throughput option for ≤ 32K chunks (15.4 % on 8-needle at 128K, so never for long windows) [V] huggingface.co/unsloth/Qwen3.8-27B-GGUF, contextarena.ai. The resident server's flags: `-np 2..4 -cb --cache-ram 8192 --kv-unified --cache-reuse 256 -ctk q8_0 -ctv q8_0 -fa on --slot-save-path …` (verified against `llama-server --help` of b9627) [M].
- **Partitions reshuffle unless frozen.** On the live field, Louvain across six seeds gives adjusted Rand 0.73–0.86 versus seed 0, and removing 2 % of nodes then re-running (same seed) gives 0.76 on the shared nodes [M, 2026-09-03]. One in four memberships moves every rebuild. A map that reshuffles cannot hold identity.
- **Model-emitted span offsets are unusable.** Scriptorium measured 0 % usable offsets; spans must be derived by locating quotes in the tape (`fence --derive`, 87.2 % located); the fence caught 28.5 % paraphrase-as-quote on raw v1 and 12.8 % on extracted v2. [M, C:/scriptorium/README.md 2026-09-01]
- **Residual beats uniform attention by a wide margin.** GLANCE-RACE-1/-2 on this box: residual-driven glancing catch 99.7 → 80.9 % across difficulty versus uniform 64 → 13 %; priority = residual / channel volatility; staleness is a sampler, not a priority term; a frozen loop fixates. [M, C:/NEW/eye-harness/ 2026-09-01]
- **Hyperbolic space is the right container for a hierarchy.** HypRAG (arXiv:2602.07739, Feb–Jun 2026): projecting pre-trained Euclidean embeddings into the Lorentz model (HyTE-H) gives up to 29 % gains over Euclidean baselines on RAGBench context/answer relevance, with > 20 % radial increase from general to specific concepts. HyperbolicRAG (arXiv:2511.18808): Poincaré depth-aware learner plus mutual-ranking fusion of Euclidean and hyperbolic signals. HyperRAG (ICLR 2026 submission): query-centric hyperbolic structuring. [V] fetched 2026-09-03. Radius carrying specificity is exactly the slide rule.
- **Incremental community maintenance exists.** HIT-Leiden (arXiv:2601.08554, v5 2026-06-17): bounded updates confined to the 2-hop neighbourhood of affected supernodes, up to five orders of magnitude faster than recomputation, modularity within 0.5 % of static Leiden, quality-stable over 999 update batches, 56× faster than static Leiden for Graph-RAG indexing; no public code found. [V] arxiv.org/abs/2601.08554 2026-09-03.
- **Memory systems' honest numbers.** Zep/Graphiti 63.8 % vs Mem0 49.0 % on LongMemEval (GPT-4o) [V] vectorize.io comparison 2026; HippoRAG 2 lifts MuSiQue F1 44.8 → 51.9 over NV-Embed-v2 RAG and indexes with 9M tokens versus LightRAG/GraphRAG's 115M, while structure-based methods lose 5–10 F1 on simple QA [V] emergentmind HippoRAG-2 summary 2026; LongMemEval-V2 (arXiv:2605.12493): 451 questions, haystacks to 115M tokens, baselines RAG 42.8 % → AgentRunbook-C 74.9 % at 108 s, leaderboard empty as of 2026-09-03 [V] xiaowu0162.github.io/longmemeval-v2. **Consequence:** the graph must pay rent above lexical+dense on measured queries or step aside (F-RENT).
- **Chunk context matters more than chunk boundaries.** Contextual retrieval (LLM-written chunk context + BM25 + rerank) cut top-20 retrieval failures by up to 67 %; late chunking (embed the document, pool per chunk) gains grow with document length and cost only the embedder; with strong embedders, fixed-window vs semantic chunking barely differ once late chunking is applied. [V] arXiv:2504.19754 and the 2026 chunking comparisons, fetched 2026-09-03.
- **MCP is stateless now.** The 2026-07-28 spec removed sessions and the initialize handshake; `server/discover` is mandatory; Streamable HTTP POSTs must carry `Mcp-Method` and `Mcp-Name`; list results carry `ttlMs`/`cacheScope`; tools should list in deterministic order for prompt-cache hits; Tasks moved to the `io.modelcontextprotocol/tasks` extension with polling. [V] modelcontextprotocol.io/specification/2026-07-28/changelog 2026-09-03.

---

## 3 · Data layer — the tape and the chunk

### 3.1 The tape (truth)
- One append-only, blake2b-128 hash-chained JSONL tape per archive root, **Scriptorium's format** (`doc` / `text` / `journal` / `contact` records; span coordinates `{doc_id, seq, start, end}` into NFC canonical `text` records) so the two organs share negatives and the fence. Transcripts enter as `doc` records of kind `transcript` with per-message `text` records carrying `{session, uuid, role, ts}`; everywhen's shards remain the source and are re-derived, never edited.
- **Origin and trust are stamped at intake from the channel, never from content:** `operator-doc` (trusted), `transcript-operator` (trusted, the operator's own words), `transcript-assistant` (narrative, model-authored), `imported` (untrusted). These tags ride every chunk, every edge, every stamp. **Provenance-role collapse is the top failure the 2026 memory literature names** (what the person said vs what the assistant said vs what was quoted): MemIR (2026-05) fixes it with typed atoms, MemGuard (2026-05) reports +28 % reliability and 5.8× fewer retrieved tokens from type isolation [V] arXiv:2605.25869, arXiv:2605.28009. An assistant paraphrase never becomes a claim attributed to the operator.
- **Byte-exact dedup first.** Conversational corpora are ~80 % redundant by bytes (80.34 % removed with zero measurable regression in the conversational regime, 2026-05) [V] arXiv:2605.09611; exact duplicates fold to one `text` record with a multiplicity count before anything is embedded.
- Journal every derived output (cards, verdicts, deltas, partition versions) as `derived` records with `{model_fp, prompt_hash, inputs}` so a rebuild is a model-free fold and a model swap is a re-adjudication, not a death (BRAIN L18, CORTEX A3).

### 3.2 Chunking [M/V]
- `C:/chunker/chunker.py --budget 512 --overlap 40` (the `--overlap 0` hang is a known defect; keep 40 until fixed; the estate is currently chunked at 700 and the 512-vs-700 choice is bake-off F-CHUNK). Structure-aware: heading boundaries first, oversize sections split recursively at paragraph groups. Evidence: a 36-strategy study (2026-03-07) puts paragraph-group chunking at nDCG@5 0.459 versus 0.244 for fixed characters, with moderate sizes winning [V] arXiv:2603.06976; semantic chunking's cost is not justified by consistent gains [V] arXiv:2410.13070.
- Breadcrumbs (H1 › H2 › H3) become the chunk's deterministic **contextual header**: `{doc title} › {breadcrumb} · {era: YYYY-MM} · {origin}`; the header is embedded with the chunk and indexed by BM25 (contextual retrieval, deterministic tier, $0). Anthropic's measurement: contextual embeddings cut top-20 retrieval failures 35 %, contextual BM25 49 %, plus reranking 67 % [V] anthropic.com/news/contextual-retrieval (2024-09-19).
- **Late chunking is not available with the chosen embedder.** Qwen3-Embedding (and jina-v5) use last-token pooling; late chunking (embed the whole document, mean-pool per chunk) is defined only for mean-pooled encoders [V] arXiv:2409.04701. If F-CHUNK wants it, the mean-pooled candidate is nomic-embed-text-v2-moe (official GGUF, 768-d MRL); otherwise contextual headers carry the context, which the 2025-04 comparison rates as more coherent anyway [V] arXiv:2504.19754.
- **Transcripts are indexed at three granularities**, not per message: segments of 5–15 messages with speaker labels under a session header; a per-session summary; extracted facts. Evidence: LongMemEval-V2 loses 28.6 points on static questions when the raw-slice pool is removed and gains from a notes pool (42.8 → 51.0 %) [V] arXiv:2605.12493; LMEB (2026-03, rev 2026-08) shows MTEB rank anti-correlates with dialogue retrieval (Pearson −0.496), so transcript retrieval is evaluated on the operator's own transcripts, never inferred from MTEB [V] arXiv:2603.12572.
- **Gear-two chunk context** (optional, priced): a one-sentence LLM-written context per chunk (Anthropic's recipe) on GLM-5.3-Flash — 3,585 chunks × ~1,000 tokens in ≈ 3.6M tokens ≈ **$0.27 at the promo price, $0.54 after** [D]. Cached prefix = the document; per-chunk suffix small. Only for documents whose placement residual is high (§6), never for retellings.
- **llama-server operational contract:** start the embedder with `-ub` ≥ the longest chunk (n_ubatch ≥ n_tokens or long inputs error); `/v1/embeddings` L2-normalises, `/embedding` may not: verify norms once [V] llama.cpp tools/server README, fetched 2026-09-03.

### 3.3 Sizing at three scales [D from M]
| Scale | Chunks | Vectors (1024-d int8) | Coarse (256-d int8) | Embedding time at the 0.6B rate | at ~4× slower (4B) |
|---|---|---|---|---|---|
| Estate today | 3,585 | 3.7 MB | 0.9 MB | 3 min | 12 min |
| Corpus #1 extracted (172M tok) | ≈ 250k at 700 tokens, ≈ 335k at 512 | 256–343 MB | 64–86 MB | 3.6 h | ≈ 15 h |
| Corpus #1 raw (1.75B tok) | ≈ 2.5M at 700, ≈ 3.4M at 512 | 2.6–3.5 GB | 0.6–0.9 GB | 37 h | ≈ 150 h (batch over a week, or 0.6B for raw + 4B for extracted) |

---

## 4 · Index layer — dense, lexical, rerank, and the two-pass scan

### 4.1 Embedder (local, free) [V]
- **Family:** Qwen3-Embedding (0.6B: 1024-d, MTEB-multilingual 64.33; **4B: 2560-d, 69.45; 8B: 4096-d, 70.58**, all 32K context, all Matryoshka down to 32-d; query format exactly `Instruct: {task}\nQuery:{query}`; **documents take no instruction**). [V] huggingface.co/Qwen/Qwen3-Embedding-0.6B model card, fetched 2026-09-03. GGUF builds exist for all three and run on llama-server with `--embedding --pooling last`. [V] llama.cpp discussion #16787 (Apr 2026).
- **Decision:** 4B by default (the knee of the curve: 8B adds +1.1 MMTEB for ~2× cost and 4096-d; Q8 ≈ 4.3 GB VRAM, fits beside a 9B reader on 16 GB); **0.6B is the floor and the current state.** Stored dims: 1024 (MRL-truncated, re-normalised) as the serving vector, plus a 256-d coarse head. The organ currently embeds queries **without** the instruct prefix; that is a measured-by-the-card 1–5 % loss and a B0 bake-off (F-PREFIX). The exact instruction string and model hash are stored with the index: a changed instruction is a silent model swap.
- **Paid fallback for the 172M-token pass and for swaps:** Voyage 4 (2026-01-15) is the one family with a shared embedding space across sizes (index with lite/nano, query with large); $0.02–$0.12 per M tokens and the first 200M tokens per account free, so the full corpus #1 pass costs $0–24 [V] blog.voyageai.com/2026/01/15/voyage-4, docs.voyageai.com/docs/pricing (2026-08-26). **Swap without re-embed:** Drift-Adapter maps a new model's queries into the legacy space by orthogonal Procrustes or a small affine map, retaining 95–99 % Recall@10 from a small paired sample [V] arXiv:2509.23471; the connectome keeps that as the bridge while the overnight re-embed runs.
- **Also credible, not default:** jina-embeddings-v5-text-small (MMTEB 67.0, retrieval average 63.28 vs Qwen3-0.6B 61.87; CC BY-NC; llama.cpp truncates inputs over ~512 tokens, issue #19865 closed-not-planned 2026-02-24) [V] arXiv:2602.15547; Nemotron-3-Embed-1B/8B (RTEB 72.38 / 78.5, 2026-07-16; no GGUF path confirmed) [V] huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16.
- **Candidates for the B0 bake-off, not defaults:** KaLM-Embedding-Gemma3-12B-2511 (11.76B, 3840-d MRL, #1 MMTEB Nov-2025 at 72.32; no llama.cpp path confirmed → UNVERIFIED locally) [V] HF card 2026-09-03; **WeMM-Embedding-9B** (Tencent, arXiv:2608.24053, August 2026; Qwen3.5-based, 4,096-d L2-normalised with Matryoshka truncation; text, images, video, visual documents and interleaved inputs, no audio; MMEB-v3 59.5 over all 190 tasks versus 53.5 for Qwen3-VL-Embedding-8B, with text 48.8 vs 42.5 and agent tasks 51.0 vs 38.4; Apache-2.0; `encode_query`/`encode_document` via Sentence Transformers; bf16 on CUDA, no GGUF, so ≈ 18 GB at bf16 and ≈ 9 GB at int8 under transformers, which means it time-shares the card with nothing else) [V] huggingface.co/tencent/WeMM-Embedding-9B, fetched 2026-09-03 on the operator's pointer; Qwen3-VL-Embedding-2B (hard R@1 0.945) as the small multimodal alternative [V] arXiv:2601.04720. WeMM is the first credible **single space for text and screenshots**; the bake-off asks whether its text-only retrieval on this corpus matches Qwen3-Embedding-4B, since MMEB text tasks are not MTEB. Until then text stays canonical: images and PDFs become text through GLM-5.3-Flash vision (gear two) or the local Qwen3.5-9B mmproj server (:8091, Scriptorium's), then embed as text.
- **Swap law:** embedder fingerprint on every vector; a swap re-embeds everything (hours, free) and keeps the partition (assignment re-run against new centroids computed from the same memberships); the layout is re-anchored (§5.4). No mixed-embedder index, ever.

### 4.2 Lexical
- SQLite FTS5 (BM25) over chunk text + header, replacing `rank_bm25` in memory at scale; unicode61 tokenizer with the operator's term list as a synonym table (FUSOR/fuser, etc., from transcripts' spelling drift). Learned sparse (SPLADE-class) is a gated bake-off, not a default.

### 4.3 Rerank (local, free)
- **Qwen3-Reranker-4B** (MTEB-R 69.76, MMTEB-R 72.74; 0.6B: 65.80 / 66.36) on llama-server `/v1/rerank` with `--reranking --pooling rank --embedding`, **converted from the HF repo with the current `convert_hf_to_gguf.py`**: community GGUFs lack `cls.output.weight` and return 1e-23 scores (issue #16407 still open) [V] huggingface.co/Qwen/Qwen3-Reranker-0.6B; gist by VooDisss 2026-03-09. Reranks the fused top-50 to top-10; a relevant/irrelevant pair must separate in the smoke test or the reranker is a no-op. Expected lift: +12.1 points R@5 over hybrid alone in the closest published analogue (hybrid .726 → hybrid+rerank .816) [V] arXiv:2604.01733.
- **Gated by source.** On conversational-memory retrieval a cross-encoder *reduced* Hit@1 by 6.9 points (2026-06-02) [V] arXiv:2606.04194; the reranker is off for transcript-segment candidates by default and on for documents, and F-RENT measures both.
- **Late interaction as a rescorer only, and only for long documents:** GTE-ModernColBERT-v1 (0.1B) scores LongEmbed 88.39 versus 79.17 for voyage-multilingual-2, and a 17M-parameter ColBERT holds 0.847 at 32k tokens [V] HF cards, mixedbread blog 2026-01-21; but ColBERT-class scorers collapse 86–97 % on long narrative queries (SIGIR 2026) [V] arXiv:2604.09982, so chat-style queries are condensed to ≤ 20 content words before any MaxSim stage. Storage rules it out as a first-stage index (172M token vectors × 128-d int8 ≈ 22 GB); no llama.cpp path is confirmed, so it runs under PyLate on the GPU if adopted.

### 4.4 The two-pass scan (SCAN, DON'T SEEK, with Matryoshka)
```
recall_dense(q):
  q256, q1024 = embed(instruct + q)            # MRL heads of the same vector
  s = GEMM(int8 X256, q256)                     # all N chunks; 250k×256 int8 ≈ 0.1 ms GPU, 15 ms CPU
  C = top_k(s, 2048)                            # coarse candidates
  s2 = GEMM(int8 X1024[C], q1024)               # exact rescoring of 2,048 rows
  return top_k(s2, 100)
```
No ANN index to build, tune, or rot; brute force is exact and the measured floor (CORTEX 4.88 ms at 1.67M×384 on this GPU). sqlite-vec holds the same int8 vectors on disk for portability (`vec0` int8 and binary columns) [V] alexgarcia.xyz/sqlite-vec 2026.

### 4.5 Fusion and the rent law
- **Convex combination of min-max-normalised scores (α ≈ 0.5)**, not RRF: Bruch et al. (TOIS 2023) show CC beats RRF in- and out-of-domain and RRF is sensitive to k; the 2026-04 benchmark gives R@5 BM25 .644, dense .587, RRF(k=60) .695, **CC(α=0.5) .726**, hybrid+rerank .816 [V] arXiv:2210.11934, arXiv:2604.01733. α is tuned on the goldens (a handful of examples suffice); RRF stays as the zero-tuning fallback. Graph firing (§5.6) enters as a third normalised score, then the reranker where gated on.
- **F-RENT:** each signal must lift nDCG@10 on the frozen goldens over the best pair without it by a pre-registered margin or it leaves the hot path (the graph decorates from the bench, as BRAIN §D2 says). The rent is printed per answer as the additive contribution of each signal.

---

## 5 · The field — graph, partition, geometry

### 5.1 Nodes
Chunk (T¹), document, community (T²), super-community (T³), corpus (T⁴ = the unit map). Nodes carry `{id, level, locator (partition_version, c1, c2, seq), span_list, salience, degree, origin, trust, vintage}` and **no content** (pointer law: a wrong firing costs one span read).

### 5.2 Slices (sparse CSR + CSC, resident)
| r | slice | basis | notes |
|---|---|---|---|
| 0 | semantic kNN | deterministic | top-10 by cosine ≥ 0.50, mutual-kNN symmetrised |
| 1 | retelling | deterministic | cosine ≥ 0.97 **or** MinHash 5-gram Jaccard ≥ 0.80; never counted as evidence, never a bridge; groups collapse to the earliest span for the timeline |
| 2 | containment | deterministic | chunk ∈ doc ∈ community |
| 3 | succession | deterministic | tape order within a document; message order within a session |
| 4 | lexical | deterministic | BM25 co-hits on rare terms (IDF-weighted), shrunk by count |
| 5 | provenance | deterministic | **transcript ↔ document**: a session message and a document span share an exact ≥ 12-gram → the session that produced the document. This is the edge "how ideas evolved" runs on. |
| 6 | contradiction / supersession | arithmetic over typed inputs | same entity + predicate, opposite polarity, disjoint validity — from the **position ledger** below; from Scriptorium cards when present |

**The position ledger (the middle layer the 2026 evidence demands).** Between verbatim chunks and synthesis pages sits a typed, bi-temporal claim table: `holds(entity, predicate, stance, valid_from, valid_to, created_at, expired_at, superseded_by, evidence_spans[], origin, confirmed)`. Graphiti's four timestamps and its rule (a superseding edge closes the old one's validity window; nothing is deleted) are the production reference [V] arXiv:2501.13956; TOKI (2026-06) shows that any LLM judge on the write path without typed operators and audit rows admits replay inconsistency, belief-drift skew, or audit erasure [V] arXiv:2606.06240; TSM (2026-01, rev 09-02) gains up to +12.2 points by building a semantic timeline (event time) rather than a dialogue timeline [V] arXiv:2601.07468. So: the LLM proposes `introduce | supersede | contradict | refine` with evidence; the operators are typed; every application writes an audit row; event time and tape time are separate columns.
| 7 | Hebbian | ledger fold | verified-use increments, difficulty-scaled, asymmetric decay, capped at 0.25 of total |

**Support gating (poisoning fix, CORTEX I-V5-SUPPORT):** a relation whose witnesses are all `imported`/untrusted needs ≥ 2 independent documents (independence key = doc + channel + intake event) or it lives in a quarantine slice, fireable only at deliberate budget with `unsupported: true` in the plan. Trusted single-document structure is backbone. Weight shrinkage `w = pmi · c/(c+3)` everywhere so a count-1 pair never carries ceiling weight.

### 5.3 The partition as a versioned artifact (the measured fix)
```
partition/v1:  seeded Leiden (leidenalg, pinned seed, canonical vertex order, resolution γ)
               on the backbone (r0 ∪ r4 ∪ r5, weights), size-repaired: > 2×target → bisect, < 0.5×target → agglomerate;
               centroids c_k (1024-d) and hierarchy: γ=1.0 → communities (T²), γ=0.3 → super-communities (T³)
between versions:
  assign(chunk) = argmax_k cos(x, c_k) subject to size cap; over-cap → overflow bucket (seeds the next version)
  local refinement (bounded, HIT-Leiden-shaped): only nodes within 2 hops of new nodes may move, only on modularity gain > 0,
      at most one pass per sleep; everything else is frozen
  drift = fraction of nodes whose nearest centroid ≠ their community; version event when drift > bar (registered) or quarterly
version event: new partition/vN with old→new map, distinctness report, and a re-anchored layout (§5.4); consumers pin the version
```
**Kill for the freeze [BET]:** if assignment-only communities lose more than 5 modularity points against a fresh Leiden after a quarter of growth, refinement runs weekly instead of per sleep; if they still lose, the version cadence halves. Measured today: fresh Leiden reshuffles 14–27 % of memberships between seeds [M]; the freeze trades that for a bounded, reported drift.

### 5.4 Geometry — radius is resolution
Two coordinate systems are maintained per partition version and re-anchored, never recomputed from scratch.

**Retrieval stays Euclidean; the map is hyperbolic.** The 2026 evidence for hyperbolic *retrieval* is real but modest and small-scale (HypRAG: a 149M-parameter Lorentz encoder, MTEB 56.41 vs 54.11 against an identically sized Euclidean BERT; RAGBench context relevance 0.848 vs 0.798; 3× lower ANN latency) [V] arXiv:2602.07739; HyBIRD (2026-06) concludes hyperbolic geometry is "most useful as calibrated structure over a dense anchor" [V] arXiv:2606.28336; a fixed-radius Euclidean encoder matches hyperbolic prototypes in high dimension, so some reported gains are radius regularisation in disguise [V] arXiv:2309.10013. No hyperbolic encoder exists at the 1B–8B scale of current retrievers. So the index is Euclidean (§4) and hyperbolic geometry is spent where its exponential volume is the feature: the map.

**Canonical: Lorentz H³, placed analytically, displayed on the Poincaré ball.** Coordinates live on the hyperboloid $\mathcal{L}^3$ in float64 on the CPU (Lorentz is the numerically safer model to optimise; Poincaré and Lorentz both hit float limits, and umap-learn's `output_metric="hyperboloid"` is the Euclidean parametrisation that keeps steps on the manifold) [V] arXiv:2211.00181, arXiv:2505.18973; the GPU receives only $\rho = \tanh(r/2) < 1$. Placement is arithmetic, not an optimiser, because no hyperbolic optimiser scales past ≈ 10⁵ points (hyperbolic t-SNE: 89,701 points in 45 min on CPU, 2-D) [V] arXiv:2401.13708:

```
level radii     : Δ = ln(b)/2 per level; with branching b ≈ 10, Δ ≈ 1.15 → display radii ρ ≈ 0 / 0.52 / 0.82 / 0.94
                  for corpus / super-community / community / chunk (H³ volume grows ≈ e^{2r}, so each level has b× the volume of the one above)
within a level  : r_i = r_level − ½ ln(k_i / k̄_level), clipped to ±Δ/2, where k_i is importance (PageRank on the kNN graph,
                  citations in the position ledger) — the Krioukov law: radius encodes expected degree, angle encodes similarity
angle           : the unit-normalised Euclidean UMAP-3 coordinate of the node; children constrained to their parent's hyperbolic cone
                  (Munzner's H3 construction, 300k edges in 1998, re-done with embeddings)
rim             : chunks below a focus-dependent importance cut go past ρ ≈ 0.94 and are drawn as density, not as pickable instances
```
Precedents: Krioukov et al. 2010 (radius ↔ degree, angle ↔ similarity) [V] arXiv:1006.5169; popularity-versus-similarity growth (radius ∝ ln t, new links minimise hyperbolic distance) [V] arXiv:1106.0286; HypLoRA finds the same inside LLMs (frequent abstract tokens near the origin, rare specific ones far out) [V] arXiv:2410.04010; HypRAG measures +20.2 % norm from most general to most specific concepts [V]. **Pooling happens on the manifold:** naïvely averaging Euclidean vectors then projecting collapses toward the origin [V] HypRAG §limitations. **Measured before assuming tree-likeness [M, 2026-09-03]:** four-point Gromov δ on 2,000 chunks of the live field (chordal distance on the unit sphere, 299,109 random quadruples): median 0.019, p90 0.047, p99 0.074, max 0.133 against a diameter of 1.376, i.e. **δ/diameter ≈ 0.054 at p99**, roughly twice a random 1024-d control (0.029), whose δ is artificially small by concentration of measure. The raw embedding space is therefore not tree-like enough to carry a hyperbolic optimiser; the hierarchy is imposed by the partition tree and the embeddings supply only the angle, exactly the analytic placement above. (The only 2025–26 δ study is on protein models, not text [V] arXiv:2512.20926; this is the corpus's own number.)

**The slide rule is the Poincaré map itself.** Display radius $\rho = \tanh(r/2)$ is strictly below 1 for every hyperbolic distance, so adding documents can never overflow the ball; resolution degrades toward the rim as $1/(1-\rho^2)$, which is the log compression the operator asked for.

**Angular layout: Euclidean UMAP-3** (cuML 26.08, 2026-08-05, deterministic kNN and a serial-optimise option since 26.06; 10⁶ × 768-d in under a minute on one consumer GPU; `init=` accepts the previous coordinates) [V] github.com/rapidsai/cuml/releases, umap-learn API. This is also the "cloud" view.

**Hierarchy tooling:** EVōC (0.3.1, 2026-03-27) gives multi-resolution `cluster_layers_` over embedding vectors and Toponymy (0.5.3, 2026-08-17; llama.cpp backend) names each layer, the open-source form of Clio's facet → embed → hierarchy → LLM-label pattern [V] pypi.org/project/evoc, pypi.org/project/toponymy, arXiv:2412.13678. Community IDs come from the frozen partition (§5.3), warm-started with `initial_membership` and stabilised by FastEnsemble consensus (10 seeds, co-classification threshold 0.8, tested to 3.8M nodes) [V] PLOS Complex Systems 2025-10-01; Leiden "admits exponentially many near-optimal partitions" on sparse graphs, and deterministic k-core hierarchies (KDD 2026) are the trial alternative for the document layer [V] arXiv:2603.05207.

**Stability law (F-LAYOUT-STABLE):** new nodes are placed immediately by `UMAP.transform()` (their angle) and the analytic radius (their level and importance); nothing else moves. Periodic re-fits use ParametricUMAP with ≈ 1 % of old points as landmarks (`landmark_loss_weight` ≈ 0.01), the documented mechanism that keeps the space consistent while admitting a new cluster [V] umap-learn transform_landmarked_pumap; AlignedUMAP's `update()` looks backward only and retains all data, so it suits batch streams, not an ever-growing corpus; parametric maps lose local structure (ParamRepulsor) so the non-parametric fit stays the reference [V] arXiv:2411.15894. After any re-fit: orthogonal Procrustes (rotation + uniform scale, no reflection) onto the shared nodes' previous coordinates, then hysteresis (a node moves only if its hyperbolic displacement exceeds 0.1 Δ). **Bar:** median displacement of unchanged nodes ≤ 2 % of the ball radius per build; a version event may exceed it and says so.

**Navigation:** focus-and-context by hyperbolic translation (a Lorentz boost moving the focused node to the origin), the 3-D form of the Lamping–Rao hyperbolic browser: what you look at is sharp, everything else compresses toward the rim and stays visible. Level of detail is free: draw T³ spheres sized by log(members), expand T² within radius 1.2 of the focus, chunks within 0.6.

**Attention budget by geometry (the slide rule as a dial):** a read plan spends its token budget on chunks inside a hyperbolic ball of radius $\rho$ around the query focus; because volume grows exponentially with $\rho$, the dial from "structure only" to "exhaustive" is one scalar, and the anytime behaviour (more budget → strictly more of the same neighbourhood) is monotone by construction.

### 5.5 Bridges (proposals, never findings)
A bridge is a pair with cosine ≥ 0.62 across super-communities whose r1 (retelling) relation is absent and whose documents are distinct. Bridges are `model_asserted` in CORTEX's taxonomy: they propose a read; they never close a claim. The 160 bridges on the estate [M] are read plans.

### 5.6 Firing
```
fire(seed, hops=3): a0 = span-projected dense top-m ∪ exact lexical hits ∪ nodes already in the window
  mask scope (-inf) before any top-k
  a ← α Σ_r w_r · SpMSpV(T_r, a) + (1-α-β) a0   # PPR restart, sparse frontier
  k-WTA; hub suppression by 1/log(degree); time decay
returns a read plan + salience annotation + absence markers (communities at centroid only), never an answer
```

---

## 6 · Attention — the residual loop (what makes it a brain and not a database)

### 6.1 Placement
For every new chunk $x$: residual $r = 1 - \max_j \cos(x, X_j)$ excluding the retelling slice; community entropy $H$ of its top-10 neighbours' communities; lane volatility $v$ = EMA of residuals from the same source lane; **priority $p = r/v$** (GLANCE-RACE-2: residual over belief-free channel volatility beat every other arm [M]). Verdicts, thresholds as registered in v0.1: RETELLING $r<0.05$ · ROUTINE $r<0.30$ · RELATED · BRIDGING ($H$ high, two super-communities) · NOVEL $r>0.45$. Habituation: $P_o = 1/\mathrm{EMA}[r^2]$ per lane so a chatty source does not monopolise. **Measured today:** `place` on a 16-chunk document runs in 3.0 s and returns verdict, residual, bridges, lane [M].

### 6.2 Contextual intake (the second reading at the door)
A chunk with $p$ above the registered bar is read **with its map slice** (its community gist, its top-k neighbours' headers, its era, the unit map line for its super-community) by gear one (local 9B) or gear two (GLM-5.3-Flash), emitting a **typed delta** (§8.3) and, when Scriptorium is present, a card with claims as (subject, predicate, polarity, time) tuples whose quotes are span-derived by the fence. A retelling gets no read; a NOVEL chunk gets the full slice. Scriptorium's inversion made continuous: the notes carry the memory; the corpus is read again only where the residual says so.

**Novelty is decided at the claim grain, not the chunk grain.** The chunk residual is the cheap first gate; a chunk that passes is decomposed into atomic content units and each unit is checked against the position ledger and the ACU bank of what is already held, weighted by salience (NovAScore's shape: 0.626 point-biserial with human novelty judgements) [V] arXiv:2409.09249. A running-centroid distance is a prior for ranking only, since it is orthogonal to quality (r = −0.002) [V] arXiv:2603.01791. Near-duplicate paraphrase beyond MinHash runs as a cascade (projection hashing → attention-weighted MinHash → LLM adjudication at < 1 % neural cost) [V] arXiv:2607.01601. Entity graphs extracted by LLMs are too noisy to carry this (Graphiti's own entity dedup F1 is 0.674) [V] github.com/getzep/graphiti/releases v0.29.1; retelling detection runs on claims and spans, never on extracted entities.

### 6.3 Stability–plasticity
- **Curriculum:** trust tier decides order and weight. The operator's own top documents build the first partition version; transcripts and imports arrive after the partition exists and are *assigned*, never allowed to re-partition on arrival.
- **Vigilance (ART):** a NOVEL chunk becomes a community candidate only after $m=3$ independent witnesses (documents, channels) fall within cosine 0.6 of it; until then it sits in the overflow bucket with `provisional: true`.
- **Two stores (CLS):** fast store = Hebbian ledger, lane EMAs, overflow bucket (changes nightly); slow store = partition versions and the unit map (change only at version events).
- **Precision-weighted belief:** a position's update step is $\Delta \propto 1/\text{corroboration}$; a claim with five independent witnesses moves one fifth as far on one contradicting document as a claim with one witness. Single-source claims are flagged `single_source` on every stamp (CORTEX I-V5-CORROBORATE).
- **Drift alarm (frozen references + CUSUM):** community mass shares and the top-50 term distribution per community are frozen at each version; a CUSUM ($k=0.5\sigma$, $h=5\sigma$) trips a *review*, never an auto-refreeze; re-freezing requires the operator's countersign (BRAIN §B4). The brain does not flip overnight; the operator can flip it in one command.
- **Belief revision is proposed, never auto-applied.** The 2026 evidence is unambiguous: models track legitimate updates but resist unjustified drift poorly or the reverse (BeliefShift, 2,400 human-annotated trajectories: GPT-4o BRA 0.83 / DCS 0.61, Claude 3.5 DCS 0.81 / BRA 0.74) [V] arXiv:2603.23848; memory-induced sycophancy is measurable [V] arXiv:2607.01071; larger models detect temporal conflicts but the reasoning rarely reaches their final answer (ACL 2026 Findings) [V] aclanthology.org/2026.findings-acl.103. Therefore `supersede | contradict | refine` edges on the position ledger carry `confirmed: false` until the operator confirms (one command, batched in the morning brief); unconfirmed edges are retrievable and rendered as such, never silently applied to the unit map. A second brain that auto-updated positions from transcripts would drift toward whatever was said last.
- **Anti-capture floors:** systematic permuted sweep of every chunk once per period (14.9× cheaper than random for the same guarantee [D, CORTEX §3.8]); reverse-order fold; null-prior occasion; ε-reserve of 2 % of every read plan for lowest-salience communities; a shuffled control. Skipped floors stamp `anti_drift_stale: true`.
- **Forgetting curve:** Hebbian decay toward a floor, never to zero; lazy on touch; a monthly plasticity budget $\Sigma|\Delta w|$ with a z-alarm (a poisoning burst and a dying graph look the same on that one number).
- **Attention audit:** nightly, sample what placement refused to read (RETELLING/ROUTINE) and grade it against next-day citations with planted probes; a judge that cannot find the probes dies (BRAIN j8).

### 6.4 The unit map and the pages (always total, rebuildable)
A 4,000-token (envelope 2–8k) deterministic rendering: kernel (who this is for, in the operator's words, pinned), the partition tree with one line per super-community and a counts line per community, the ten freshest NOVEL placements, the open contradictions, the forgotten list, and the vintage. Every tape day is inside some line at some depth (F-UNIT: a withheld slice must show as a hole). Regenerated nightly; **the diff is a first-class artifact** (`unit_map.diff`), taped and shown in the render as the atlas-diff overlay. It is the pinned prefix of every session and every rescan.

Below the unit map sit **pages**: one per community (Clio-style cluster description) and one per topic articulation (§7.2), each carrying `{model_fp, prompt_hash, sources, vintage}` so a newer model re-derives by replaying raw → claims → page. This is the LLM-wiki pattern (raw sources immutable; an LLM-owned wiki of summaries, concept and overview pages; a lint pass for contradictions, stale claims and orphans; an append-only log) run on 15,259 PDFs → 16,294 pages in one published instance [V] gist joonan30, rev 2026-08; the wiki's own measurement found BM25 locating the primary source in 118/120 searches at 0.68 ms against 113/120 at 678 ms for vectors. **Merging upward feeds source passages, not only child summaries:** recursive merging amplifies hallucination past 100K tokens and context-aware merging beats it consistently (ACL 2025 Findings) [V] arXiv:2502.00977. Sleep-time consolidation is the right cadence (≈ 5× less test-time compute at equal accuracy, 2.5× cheaper amortised, the benefit growing with query predictability, which is high for a personal archive) [V] arXiv:2504.13171.

---

## 7 · Recall and the rescan

### 7.1 Rungs, stamped
| Rung | Mechanism | Cost | Guarantee |
|---|---|---|---|
| R0 | unit map in the prefix | 0 | always-total at stated resolution |
| R1 | FTS5 BM25 + typed joins (timeline, containment, provenance) | ms | exact over extracted structure |
| R1+ | graph elevation: firing merged into R1, contribution stamped | ms | importance-sampled *where* |
| R2 | dense two-pass ∥ BM25 → RRF → reranker → spans from the tape | 0.5–2 s | exact spans, partial coverage |
| R3 | dossier sweep: hyperbolic ball around the topic, all communities touched, contrarian seat on dark cells | ¢–$ | exact within scope |
| R4 | full sweep of a scope (gear two, batch) | $ | exhaustive |

Every answer carries `stamps = {rungs, coverage n/N with N stated, fidelity, cost, single_source, insufficient_rung}`; quantifier questions (every/all/none/how many) resolve at ≥ R3 or return `INSUFFICIENT_RUNG` (implemented 2026-09-02 [M]).

**Router law from the 2026 benchmarks:** hierarchy pays for aggregation and multi-fact reasoning and loses on fact lookup and detail-heavy summarisation. GraphRAG-Bench (ICLR 2026): basic RAG with rerank 60.92 on fact retrieval vs Microsoft GraphRAG 49.29, but 42.93 vs 50.93 on complex reasoning; HippoRAG 2 leads reasoning at ≈ 1,000 tokens per query where GraphRAG-global spends ≈ 331,000; on summarisation GraphRAG collapses (ROUGE-L 22.98 vs 78.54) [V] arXiv:2506.05690; WildGraphBench agrees [V] arXiv:2602.02053. So fact questions go to R2 flat; "what do I hold on X" goes to R3 pages and firing; the router never sends a lookup through the tree.

### 7.2 The rescan loop (new model, same corpus)
```
scope(topic)      → the hyperbolic ball: communities whose gist or top terms hit the topic, plus provenance-linked sessions
skeleton          → dossier: timeline (retellings collapsed to earliest), communities, eras by month, bridges out,
                    dark matter (spans never cited), contested positions (r6), the forgotten (cited early, absent late),
                    read_plan_first (highest residual per era). Pinned as prefix: ≈ 20–60k tokens.
attend            → reads by residual against the skeleton, budget along ρ; one contrarian seat on the darkest cells;
                    distill-and-evict: each read leaves a note with a span ref, the raw span leaves the window
articulate        → claims with quotes; quotes are located in the tape by the fence (derived spans), never trusted from the model
reproject         → every view (document, session) is scored for residual against the articulation:
                    reconciled | superseded (with the superseding span) | branch (a live alternative) | forgotten (never re-derived)
vintage + diff    → articulation vN, model_fp, receipts; diff against vN-1 by section; the diff is the deliverable
```
**Accuracy ladder** (highest first): receipt-closed claim (span located) > independently corroborated (m ≥ 2 independent documents) > supersession-aware reconstruction (a later typed position overrides an earlier one) > lone narrative. Retellings are weightless. The operator's contradictions across time are the payload, not noise: `current_position(entity, predicate)` returns the whole chain with its contradictions, never the latest row alone (CORTEX I-V5-POSITION).

**Elicitation:** contested positions and forgotten items become questions to the operator; answers append to the tape as testimony with a date (Scriptorium's LIVE annex). The highest-value tokens are the ones not yet recorded.

**Cost of one rescan [D]:** skeleton 40k tokens pinned + 150 reads × 2k tokens + 20k output. On GLM-5.3-Flash promo: ≈ $0.03; on Opus 5: 340k in × $5 + 20k × $25 ≈ $2.2 (with the skeleton cached after the first call: less); on Fable 5.1: ≈ $4.4 first, then skeleton reads at $0.25/M. **F-VINTAGE:** same skeleton, two instruments, blind-rated against the same spans.

**Instrument and window rules (from the 2026 measurements above):** every attend call stays ≤ 128K–200K tokens of skeleton plus reads, whatever the advertised window; the articulation instrument is **Opus 5 by default** (91.3 % at 128K, first by area under the curve), **Fable 5.1 when an Opus 5 run falls short on the goldens** (+2.2 ProgramBench points at the full window for 2× the price, and cache reads at 0.025×), never Opus 4.7 (0.5–1.4 %), never Haiku 4.5 (200K window, 4,096-token cache minimum, retirement not before 2026-10-15). Gear-two readers for the surgical reads are GLM-5.3-Flash or DeepSeek V4 Flash (both 62.9 % at 128K, enough for chunked reads), or the local Qwen3.8-27B. GPT-5.6 Sol (92.4 %) is an alternative synthesis instrument at $4/$0.40/$20 through 2026-11-21, with the trap that requests above 272K input are billed at 2× input and 1.5× output and its usable input caps at 922K [V] developers.openai.com pricing and model pages 2026-09-03. Fable availability is a risk to plan around (access suspended 2026-06-12 to 2026-07-01), so the Opus 5 fallback is wired, never assumed [V] anthropic.com/news/redeploying-fable-5.

**Calibration first (F-PROBE):** before comparing models, measure each model's effective window on this corpus with a no-lexical-overlap arm (NoLiMa-shaped) and a synthesis arm; budgets per rescan are set from the minimum, per model, with vintage. NoLiMa's public table has not moved since 2025-07-17 (GPT-4.1 effective 16K, 64.7 at 128K; Gemini 2.5 Flash 2K), so there is no verified effective-length number for any 2026 model [V] github.com/adobe-research/NoLiMa; the probe is the only honest source. Token budgets are model-versioned: Claude models from Opus 4.7 onward use a tokenizer that yields ≈ 30 % more tokens for the same text [V] platform.claude.com pricing page 2026-09-03.

**Long context is the right tool exactly here.** Over a curated topic bundle (skeleton + reads), long-context models remain highly competitive (EvoMemBench 2026-05) and full-context matches verbatim RAG within noise (MemDelta 49.8 vs 47.2, p = 0.34) [V] arXiv:2605.18421, arXiv:2606.29914; recite-then-answer adds up to 4 points [V] arXiv:2510.05381. Distill-and-evict is where the frontier is moving (Chroma Context-1, a 20B self-pruning search agent, 0.88/0.97 vs 0.58 base, 2026-03; Still, 8–200× KV compaction with +8–22 on RULER, 2026-06) [V] trychroma.com/research/context-1, arXiv:2606.07878; the attend step keeps notes with span refs and evicts raw spans. Cartridges (ICLR 2026; multi-cartridge +10–31 points, 3–4× fewer prompt tokens, but naive mixing collapses to chance and weights are required) are a future gear: topic bundles stay cartridge-ready, nothing depends on them [V] arXiv:2506.06266, arXiv:2606.04557.

---

## 8 · The corpus callosum — agents on Intercom with one sentry

### 8.1 The bandwidth law and the diagnosis
N subagents at 1M tokens = N× read rate and N× addressable index; effective synthesis per head stays 2K–250K depending on shape (§2). Intercom is already the bus (v0.2.3: lanes, `await`, `claim/release` CAS, `handoff/takeover` capsules, `pin`, `replay --json`, the relay firewall, the doorbell contract "at end-of-turn run `check --me`; non-empty output is injected as the next context") [V] C:/Intercom/INTERCOM-SPEC.md, docs/WAKE-ADAPTERS.md. Writes are milliseconds; the polling engine is 0.03 ms per poll against 108 ms process overhead [M, Intercom NOTES v0.1.8]. The lag is **composition** (minutes to write a message), **polling** (turn boundaries), and **per-look cost** (a forward pass over a growing log). Operator ruling: ≤ 10 concurrent subagents; stagger waves [V] reference-intercom-bus.md 2026-08-20.

### 8.2 The sentry (gear one, world rate)
One daemon principal `connectome-sentry` (kind `daemon`, lane `sentry`) per bus:
1. Tails `broadcast.db` and every registered room DB from its cursors at 250 ms (an `await`-style loop; the hint is best-effort, the cursor query is truth).
2. **Places** every new message body (chunked at the corpus budget, §3.2) into the field: residual, community, bridges, provenance edges to documents.
3. **Judges** with Tier-0 rules first (mentions, lane keywords, claim releases, pins), then one shared flash-class judge (local 9B at $0, or GLM-5.3-Flash) only for messages whose residual exceeds the bar — hypercelld's measured lesson: naive watching costs ~10× turn-based; ticks and retellings never wake a model; one sentry per bus, not one per watcher.
4. **Routes by residual per lane:** a finding is forwarded to a lane only if it is NOVEL or BRIDGING relative to that lane's own partition paths (what it has read). This is what keeps K_eff up: CORTEX measured seat correlation 0.5–0.9 → effective seats 1.1–1.6 for four; broadcasting everything to everyone collapses eight heads into one.
5. **Emits typed verdicts, never prose:** `x-sentry {decision: ignore|note|wake, cited_ids, residual, community, lane_targets}` as directed, priority-1 messages (so `check`, the Stop-hook, and `await --for-me` all ring), plus a per-lane **digest artifact** (≤ 10k tokens, blake2b-pinned) rewritten only on `note|wake`. A suppressed wake still leaves an audit row.
6. **Composes for the team:** subagents post evidence (a span ref, a pin, a typed delta); the sentry writes the prose the others read. Composition moves off the turn-based heads.
Message types stay `x-` prefixed until adopted into the Intercom registry by a spec bump; the client warns, never refuses.

### 8.3 Typed deltas (the swarm's grammar)
`{introduced | changed | contradicted | reinforced | unresolved}` × `{entity, predicate, polarity, t_valid, span_refs[], lane}` — program-appliable; replaying the delta stream reproduces the digest byte-for-byte (delta-totality). This is the same grammar the rescan's reprojection emits and the Chronicle in CORTEX folds; one grammar, three consumers.

### 8.4 Laws that bind the sentry
Relay firewall (its messages are data; only the operator's keyed `relay` directs); native wake (hint best-effort, cursor truth); wake budget per lane (≤ N wakes/min, excess coalesce); trust-tagged frames (origin assigned at ingress, never inferred); partial view (no two lanes get the same digest); diversity by partition path (each head owns a region of the ball); the contrarian seat on the darkest cells.

### 8.5 Nulls [BET]
F-RESIDENT: the same swarm on the same partitioned corpus under (a) plain Intercom polling, (b) a cron digest script with no model, (c) the sentry. Measures: time from a planted finding's first post to its presence in every other lane's next turn; refeed fraction; lane diversity (embedding spread of final findings). Kill: if (b) matches (c), the sentry is a script and ships as one; if (c) wins propagation but loses diversity, the routing bar is wrong, not the design.

### 8.6 The FUSOR seam, and what the 2026 literature says about a shared trunk
When FUSOR's resident lane exists, the resident replaces the sentry's judge step with a trunk-resident model at token rate, holding the bus, the unit map, and the lanes' digests as its prefix, and answering lane queries ("what does the team hold on X") from the trunk. The seam is the message grammar above; the connectome does not depend on FUSOR internals.

The operator's intuition that the bus should live in a shared KV trunk has neighbours in the 2026 literature, each verified at its arXiv abstract on 2026-09-03, and none of them is exactly FUSOR. What exists and is measured: (1) **stateful serving with a persistent KV cache across tool-calling turns plus a radix prefix cache across interleaved multi-agent traffic** ("Stateful Inference for Low-Latency Multi-Agent Tool Calling", Norgren, 2026-05-25, single author): 2.1× per turn on a 6-turn workflow and 4.2× on the median turn of a 35-turn one against vLLM and SGLang, with the abstract's own note that the gain "comes from stateful reuse and speculation, not caching" [V] arXiv:2605.26289; (2) **KV-cache time-to-live retention across tool pauses** ("Continuum", Li, Stoica et al., 2025-11-04, rev. 2026-05-25): over 8× better average job completion on SWE-Bench, BFCL and OpenHands agents with Llama-3.1 8B/70B, Gemma-3 12B and GLM-4.5 [V] arXiv:2511.02230; (3) **prefix-aware scheduling and eviction for coding agents** ("CacheWise", Tiwari, Peter, Mahajan, Shen et al., 2026-06-15): real traces show sessions "repeatedly reuse large prefixes"; 2–2.6× fewer evictions and up to 3.5× faster sessions in vLLM [V] arXiv:2606.16824; (4) **per-agent Q4 KV caches persisted to disk and restored into attention** on an Apple M4 Pro ("Agent Memory Below the Prompt", Shkolnikov, 2026-02-17, single author, edge devices): time-to-first-token cut 22–136× (Gemma 3 12B), 4× more agent contexts than FP16, perplexity within ±3 % [V] arXiv:2603.04428; (5) **quantised KV handoff between agents** ("QKVShare", Honavar and GVSL, 2026-05-05): 397 ms versus 1,030 ms re-prefill at 8K on Llama-3.1-8B, with the abstract itself calling for "stronger controller ablations" [V] arXiv:2605.03884; (6) a **survey of latent communication** (embeddings, hidden states, or KV caches exchanged directly between agents; "Beyond tokens", Liu, 2026-06-04, rev. 2026-07-15, single author) that categorises eighteen methods from 2024–2026 along what is communicated, how sender and receiver are aligned, and how it is fused (including "cache restoration"), and reports no benchmark [V] arXiv:2606.05711. **Read honestly:** (1)–(3) are production-shaped and from serving groups; (4)–(6) are single-author or early preprints on edge devices. All of them reuse or hand off a KV cache *between turns or between agents*; none implements one resident trunk that many heads read at token rate while it keeps ingesting, which is FUSOR's claim. The literature says the prefix-reuse half of that claim is real and cheap; the always-on resident half is still the operator's own bet [BET], and F-RESIDENT (§8.5) is its kill. **Gear one already has the cheap half of this today:** llama-server's host-memory prompt cache (`--cache-ram`, unified KV, slot save/restore to disk) re-prefills a shared prefix in milliseconds (measured 16 ms for a 1,664-token prefix) [M], and llama.cpp master carries DeepSeek V4's built-in DSpark draft heads for speculative decoding. The prefix-sharing economics for ten workers on one 100K-token prefix, input side, within cache TTL [D from the 2026-09-03 price sheets]: Fable 5.1 $10.00 → $1.48; Opus 5 $5.00 → $1.08; Sonnet 5 $2.00 → $0.43; GPT-5.6 Sol $4.00 → $0.86; DeepSeek V4 Flash off-peak $0.22 → $0.03; Kimi K3 $3.00 → $0.57; local ≈ $0 with one 24 s prefill then 16 ms per hit. The swarm's shared skeleton is therefore almost free on every gear; what costs money is the reads, and the residual gate is what rations them.

---

## 9 · Render — true 3-D, functional first, beautiful later

- **Stack:** three.js **WebGPURenderer r185** (2026-07-01; r184 2026-04-16 removed per-frame allocations; TSL shaders compile to WGSL and GLSL; automatic WebGL2 fallback; native Gaussian-splat meshes merged for r186, not yet tagged on 2026-09-03) [V] GitHub releases API, radiancefields 2026-08-10. **Nodes are instanced quads, never `gl.POINTS`:** WebGPU's `point-list` topology has no point size [V] W3C WebGPU spec. Lorentz coordinates sit in a persistent storage buffer; the focus-and-context re-centring is one 4×4 Lorentz boost uniform, so moving the focus uploads nothing. Instanced attributes cannot grow after creation (three.js issue #29966), so buffers are allocated at 2× the current node count [V]. Picking is GPU id-buffer (render ids offscreen, read one pixel), as cosmos.gl 3.4.0 does for hover on 10⁵ points [V] github.com/cosmosgl/graph/releases 2026-07-27. Per-frame budget ≈ 2M instances (Apple's Embedding Atlas holds 60 fps to 4M points and 25 fps past 10M on an M1 Pro with WebGPU) [V] arXiv:2505.06386; beyond the budget the rim is a density texture; a Spark 2.x level-of-detail splat cloud (64K-splat chunks, 0.5–2.5M budget per device) is the experiment, not the plan [V] worldlabs.ai Spark 2.0 2026-04-14. Labels appear by zoom level with map-style de-overlap (datamapplot 0.7.3 + Toponymy layers) [V]. `3d-force-graph` remains the shipped prototype (ceiling ≈ 10⁴ nodes; its largest example is ≈ 4k) and the 2-D overview uses `@cosmos.gl/graph` (MIT), not `@cosmograph/cosmos` (CC-BY-NC-4.0). Not used for the 3-D core: deck.gl (WebGPU "not production ready", picking not ported) [V] deck.gl developer guide; cuGraph ForceAtlas2 (2-D only) [V] docs.rapids.ai 26.08.
- **Prior art, checked (2026-09-03):** no project renders embedding-similarity edges in 3-D over a person's documents. All six Obsidian 3-D graph plugins draw wikilinks only; the two "Smart Connections Visualizer" plugins that draw semantic edges are 2-D; mcp-memory-service (Orrery-style 3-D) and TrustGraph's 3-D explorer render memory snippets and triples, not documents; GraphRAG Workbench (React Three Fiber, d3-force-3d) renders GraphRAG output; Cosmograph and Nomic Atlas are 2-D. Every 3-D tool re-runs a force simulation from random seeds each session: the identity-holding layout (§5.4) has no prior implementation [V] `docs/sota/SOTA_second-brain-prior-art_2026-09-03.md`. Physics workers worth lifting for scale inside a browser: Fast 3D Graph (AssemblyScript Barnes–Hut, 20k nodes ≈ 75 FPS) and New 3D Graph (Rust/WASM SIMD, 50k+ nodes at 60 FPS), both MIT. Licence trap: `@cosmos.gl/graph` is MIT while `@cosmograph/cosmos` is CC-BY-NC-4.0, same engine.
- **Anchoring primitives:** AlignedUMAP (`relations` across slices, `alignment_regularisation`, incremental `update`) and parametric UMAP `transform()` place new points into a fixed map; d3-force-3d `fx/fy/fz` pins a node so the force layout relaxes only locally. These are the two published primitives for §5.4's stability law; the Lorentz refinement runs on top of them.
- **Views:** Poincaré ball (canonical, focus-and-context), Euclidean cloud, per-slice layers, community hulls, bridges as amber arcs, retellings as dim ghosts.
- **Time:** the tape replays; nodes appear in tape order; the slider is a cursor into the tape; the atlas-diff overlay shows what moved since the last vintage.
- **Inspector:** verbatim spans, stamps, provenance chain (session → document), position chain with contradictions.
- **Never:** free prose inside the map (the unit map lines are render-normalised, imperative patterns stripped: the atlas guard), and no layout that is not reproducible from the store.
- **F-3D-VS-2D** stays registered: the operator finds planted bridges faster in the ball than in a 2-D graph, or the 3-D claim is decoration and says so.

---

## 10 · The MCP surface (2026-07-28 spec)
Stateless server: `server/discover` implemented; every request carries protocol version and client capabilities in `_meta`; tools listed in deterministic order with `ttlMs`/`cacheScope`; Streamable HTTP POSTs require `Mcp-Method`/`Mcp-Name`; stdio for Claude Code. Tools: `recall(q, budget, scope, as_of)`, `place(path|text)`, `dossier(topic)`, `what_changed(since)`, `unit_map()`, `rescan(topic, instrument)` as a `io.modelcontextprotocol/tasks` extension task polled with `tasks/get`, `elicit(topic)` returning the open questions, `verify(claim, spans)`. No output-side interpreter: model text is parsed under one grammar (claim markup); nothing in corpus or bus bytes is a directive (CORTEX I-V5-PARSER = Intercom §11).

**SDKs and clients (2026-09-03):** Python `mcp` 2.1.1 implements 2026-07-28; the TypeScript v2 SDK is `@modelcontextprotocol/client` and `/server` 2.0.0 (2026-07-27), replacing the monolithic `@modelcontextprotocol/sdk` whose latest is still 1.30.0 on the v1 line [V] pypi.org/pypi/mcp, registry.npmjs.org. Claude Code runs the v2 runtime by default since v2.1.232 (stdio servers negotiate only with `MCP_PROTOCOL_NEGOTIATION=auto`; the v2 runtime is off on Bedrock/Vertex/Foundry) [V] code.claude.com/docs/en/mcp; OpenCode 1.18.x pins sdk 1.29.0, a 2025-11-25 client; the DeepSeek harness consumes MCP over stdio and HTTP with its revision unstated. So the server speaks 2026-07-28 and keeps the 2025-11-25 handshake as a fallback until the other harnesses move. **Workers through any harness:** `claude --bare -p … --json-schema … --max-budget-usd …` (usage and cost in the JSON result), `opencode run "…" --format json` (with `opencode serve` + `--attach` to avoid MCP cold boots; any OpenAI-compatible endpoint including llama-server is a provider), `dsh --profile headless "…"` or the `deepseek-harness-sdk` 0.1.2a3 Python package (2026-09-01), which Scriptorium's harness lane already uses [V] code.claude.com/docs/en/headless, opencode.ai/docs/cli, deepseek-harness.github.io.

---

## 11 · Economics (two gears, priced on today's sheets) [V/D]

| Job | Gear | Model | Unit cost | Estate today | Corpus #1 (250k chunks) |
|---|---|---|---|---|---|
| Embeddings | one | Qwen3-Embedding 4B/8B, llama.cpp | $0 | 12 min | 15 h |
| Rerank | one | Qwen3-Reranker-4B | $0 | — | — |
| Chunk context (contextual retrieval) | two | GLM-5.3-Flash | $0.075/M in, $0.25/M out (promo) | $0.27 | $19 |
| Cards (claims, quotes, links), NOVEL/BRIDGING chunks only (≈ 20 %) | two | GLM-5.3-Flash | same | $0.10 | $8 |
| Unit map + community gists nightly | one/two | 9B local or Flash | $0.01/night | — | — |
| Sentry judge (residual-gated) | one | Qwen3.5-9B local | $0 | — | — |
| Rescan of one topic | two | Opus 5 / Fable 5.1 / Flash | see §7.2 | $0.03–$4.4 | same |
| Vision on screenshots/PDF pages | two | GLM-5.3-Flash (native) or DeepSeek V4 Flash Vision | per-token | pennies | dollars |

Provider table (USD per 1M tokens: input miss / cache hit / output; fetched 2026-09-03 from the vendors' own pages):

| Lane | Miss / hit / out | Context, cache rules, notes |
|---|---|---|
| GLM-5.3-Flash | 0.075 / 0.015 / 0.25 promo to 2026-09-09 24:00 UTC+8, then 0.15 / 0.03 / 0.50 | 1M / 128K out; native video, image, file; thinking cannot be disabled; MIT weights (320B, 18B active) |
| GLM-5.3 | 1.40 / 0.26 / 4.40 | 1M; text; 69.3 % at 128K |
| DeepSeek V4 Flash (0731) | 0.22 / 0.007 / 0.66 off-peak, ×2 at 01–04 and 06–10 UTC weekdays | 1M / 384K out; automatic cache, hours to days; MIT weights; Vision-Exp variant at the same price with ≤ 384 billable tokens per image |
| DeepSeek V4 Pro (0813) | 0.66 / 0.022 / 1.98 off-peak | 60.4 % at 128K: not better than Flash for reading |
| Claude Fable 5.1 | 10 / 0.25 / 50 | 1M / 128K; cache read 0.025×; write 1.25× (5 min) or 2× (1 h); min 512 tokens; availability risk noted in §7.2 |
| Claude Opus 5 | 5 / 0.50 / 25 | 1M / 128K; 91.3 % at 128K; the synthesis default |
| Claude Sonnet 5 | 2 / 0.20 / 10 (permanent; the 09-01 increase was cancelled) | 1M / 128K; cache min 1,024; 52.9 % at 128K: cards and structured extraction, not long synthesis |
| Claude Haiku 4.5 | 1 / 0.10 / 5 | 200K; cache min 4,096; 13.8 % at 128K; retirement not before 2026-10-15: **not used** |
| GPT-5.6 Sol | 4 / 0.40 / 20 promo to 2026-11-21 | 1.05M window but 922K max input; > 272K input bills the whole request at 2× in / 1.5× out; 30-min cache only |
| Gemini 3.8 Flash | 0.75 / 0.075 / 3.75 (doubles 2027-01-01) | 1M; text, image, video, audio, PDF; explicit cache storage $0.50 per M tokens per hour; the only lane measured above 60 % at exactly 1M (3.7 Flash 63.5 %) |
| Kimi K3 | 3 / 0.30 / 15 | 1M; image + video; 38.3 % at 128K; weights under a revenue-triggered licence |
| Qwen3.8-Max (API) / Qwen3.8-27B (hosted) | 2 / 0.25 / 6 · from 0.25 / – / 2.20 | 92.3 % / 81.8 % at 128K; 27B is Apache-2.0 and runs locally (§2) |
| Anthropic batch | −50 % on input and output; the full 1M window at standard rates on 4.6+ | |
| Local llama-server | 0 | Qwen3.5-9B for chunks ≤ 32K; Qwen3.8-27B IQ3/Q3 for quality; prefix re-prefill 16 ms measured |

**Pricebook law:** every row carries its date and URL; an undated or unknown lane is refused, never guessed; promos are booked with their end date (three of the rows above expire within ninety days). Third-party price pages for DeepSeek were wrong on 2026-09-03 (still quoting $0.14 / $0.0028 / $0.28); only vendor pages are booked.

---

## 12 · Evidence — the falsifiers that decide (pre-registered before running)

| Falsifier | Claim killed if | Measure |
|---|---|---|
| **F-REFEED** (master) | the connectome is a picture | refeed fraction (share of operator tokens that are context re-supply) does not fall over two weeks of sessions equipped with `unit_map` + `recall` vs the two weeks before; from everywhen |
| **F-VINTAGE** | smarter model, same corpus buys nothing | FUSOR rescan on two instruments from the same skeleton, blind-rated against the same spans |
| **F-RENT** | the graph is decoration | firing lifts nDCG@10 on 100 goldens over BM25∥dense by the registered margin, else out of the hot path |
| **F-PREFIX** | the instruct prefix is noise | recall@20 with vs without the query instruction on the goldens. **First measurement [M, 2026-09-03], n = 28 free goldens** (transcript messages that quote a document span verbatim by 12-gram, 1–3 targets each), dense retrieval over the 3,585-chunk field with the 0.6B embedder: recall@1 0.429 → 0.464, @5 0.750 → 0.750, @10 0.750 → 0.786, @20 0.786 → 0.821 with the instruction. The BM25 control saturates (0.857 / 1.000 / 1.000 / 1.000) because 12-gram goldens are lexical by construction, so it is a ceiling, not a comparison. Consistent with the card's +1–5 %; the prefix ships; a 100-golden re-run with semantic goldens is B0 |
| **F-CHUNK** | late chunking is noise here | recall@20 late-chunked vs header-only on long documents |
| **F-PLACE** | the residual verdict is theatre | 100 held-out files, blind operator labels {new, retold, bridging}; verdict agreement ≥ registered bar; the uniform-sampling arm loses |
| **F-LAYOUT-STABLE** | the map reshuffles | frozen partition ARI ≥ 0.95 under a quarter of growth (fresh Leiden measured 0.76 [M]); median node displacement ≤ 2 % of radius per build |
| **F-BRIDGE** | bridges are noise | planted cross-community links recovered at the registered rate; false-bridge rate on retellings = 0 |
| **F-NOVEL** | novelty detection is noise | planted novel vs retold documents separated at the registered bar |
| **F-OVERFLOW** | never-overflows is a slogan | a 10× inflated twin keeps the unit map ≤ 8k tokens, `place` ≤ 5 s, recall p95 ≤ 2 s |
| **F-RESIDENT** | the sentry is a script | §8.5 |
| **F-SPANS** | quotes are fiction | fence catch rate on planted paraphrase-as-quote ≥ the Scriptorium floor (28.5 % measured on raw) |
| **F-PROBE** | model comparisons are confounded | per-model effective window measured before F-VINTAGE |
| **F-3D-VS-2D** | 3-D is decoration | §9 |
| **F-CONTROL** | a dumb twin is as good | BM25 + keyword graph twin; commercial null (an Obsidian AI plugin or NotebookLM fed the same files); blind grading with planted items |

Thresholds go into `connectome.lock` before the runs; each `TODO` names the check it disables while unset.

**Probe design, from the 2026 evaluation literature:** knowledge-point probes cross fact × age × (current state / earlier state / trajectory) × (evidence present / missing / contradicted), because when memory systems fail the evidence was retrievable ten times more often than it was missing (MemTrace, 13 configurations) [V] arXiv:2606.17328; the scoring target is stated with every number, since target choice alone changes nDCG on 83–94 % of queries and 71 % of relaxed credit was unjustified on audit [V] arXiv:2605.24060; dense-versus-lexical lift on personal notes is measured with the BM25 floor pinned by construction or the lift is an artefact of entity-token overlap [V] arXiv:2605.29630 (the F-PREFIX goldens above are exactly that artefact for BM25, which is why they are a ceiling). Leaderboard numbers are not evidence: LoCoMo fits inside every current window and its vendor scores in the 90s are within noise of each other; LoCoMo-Plus drops the same models ≈ 20 points; MemoryArena's best agent scores 0.19 [V] arXiv:2602.10715, arXiv:2602.16313.

---

## 13 · Build order (from what exists)

**Exists [M]:** `connectome.py` with build/ask/place/codex/dossier/render/mcp/providers; stamps and quantifier pinning; proto caches; the page.

- **B0 · Instruments (days 1–2):** 100 goldens frozen from the estate (four quadrants + negative + cross-community); `connectome.lock` thresholds; **F-PREFIX**, **F-CHUNK**, embedder bake-off (0.6B/4B/8B; KaLM if a llama.cpp path exists); the reranker server; per-model **F-PROBE** on GLM-5.3-Flash, Opus 5, Fable 5.1. Control twin built and audited first.
- **B1 · Ground (days 3–5):** tape in Scriptorium format with origin/trust; FTS5; two-pass int8 GEMM; instruct prefix; provenance slice (transcript ↔ document 12-grams); support gating; `place` with typed verdict + delta; typed negatives on absence.
- **B2 · The frozen field (days 6–9):** seeded Leiden partition/v1 with hierarchy; assignment + bounded refinement; drift meter; Lorentz fit with radial prior; anchored re-layout; **F-LAYOUT-STABLE** measured; unit map with diff.
- **B3 · Attention (days 10–13):** priority r/v, habituation, curriculum, vigilance, precision-weighted positions, CUSUM alarm with countersign, permuted sweep, attention audit; contextual intake on gear one/two; **F-PLACE**, **F-NOVEL**, **F-BRIDGE**.
- **B4 · Rescan (days 14–17):** dossier → pinned skeleton → hyperbolic-ball reads → fence-derived spans → reprojection → vintage + diff; elicitation questions; **F-VINTAGE** on FUSOR under two instruments.
- **B5 · The bus (days 18–21):** the sentry daemon on Intercom (Tier-0 rules, residual-gated local judge, typed verdicts, per-lane digests); **F-RESIDENT** with arms (a)/(b)/(c); FUSOR seam documented.
- **B6 · Render (days 22–26):** WebGPU instanced ball with focus-and-context, layers, time slider, atlas diff, inspector; **F-3D-VS-2D**.
- **B7 · Corpus #1 (after B0–B4 have receipts):** cold embed of the 172M-token extracted tape (≈ 15 h at 4B), partition/v1 on the operator's top documents first, then assignment of the rest; **F-OVERFLOW** on a 10× twin.
- **Gate:** **F-REFEED** two-week measurement; publish the number either way.

---

## 13a · What exists elsewhere, and what does not (prior-art verdict, 2026-09-03)
Nothing clonable meets 70 % of the target. Closest: Graphiti/Zep (≈ 65 %: bi-temporal edges, invalidation, dedup, hybrid search, MCP; no rendering, triples not prose, FalkorDB/Neo4j under Docker), Cognee (≈ 60 %: embedded SQLite + LanceDB + Kuzu on native Windows, MCP; no supersession model, 2-D), claude-obsidian (≈ 55 %: claim ledgers with contradiction and freshness, the LLM-wiki loop; BM25 only, 2-D, Windows writes need WSL), mcp-memory-service (≈ 55 %: 3-D view, `contradicts` edges, NLI; memory snippets not documents). Retrieval, rendering, MCP and local storage are commodities with MIT/Apache parts; fact-grain supersession and dedup are solved by Graphiti/Mem0 and are **borrowed** here (the position ledger's schema and invalidation rule; Mem0's ADD/UPDATE/DELETE/NOOP loop generalised to the idea grain). The unbuilt core, and the reason this repo exists, is the semantic 3-D layout that holds identity as material arrives and biases what an agent attends to, plus idea-grain novelty verdicts over prose. Full table with dates, licences and Windows traps: `docs/sota/SOTA_second-brain-prior-art_2026-09-03.md`.

## 14 · What v0.1–v0.3 got wrong, and what survives

Wrong: re-partitioning every build (measured 14–27 % reshuffle); embedding queries without the model card's instruction; treating similarity bridges as findings; the "Hypercom" framing around reasoning (the operator's point is bandwidth); the implicit "8M effective context"; prices carried from July. Survives: the residual gate and the eye-harness numbers; the retellings slice; the succession and containment slices; the two geometries; typed negatives; the rescan as Scriptorium's retroactive re-contextualisation made routine; stamps and quantifier pinning.

## 15 · Honest limits
The field selects; it does not attend to the corpus at full resolution (10¹⁷ pair interactions are out on physics). A fully cited articulation can still be wrong by omission; corroboration counts and the contrarian seat attack that, nothing closes it. Hyperbolic radius encodes level by construction and specificity only as well as the fit; F-LAYOUT-STABLE measures stability, not truth. The sentry moves composition off the heads but cannot make a turn-based head read faster than its turn. Effective context is the binding constraint and it moves with every model version. None of this is real continuity; it is a complete, ordered, relation-aware, honest injection that a new model can trust and drill.

---

## Appendix A · Evidence table (primary sources, fetched 2026-09-03)
| Item | Date | Source | Key number | Changes |
|---|---|---|---|---|
| Qwen3-Embedding 0.6B/4B/8B | card, 2025-06 | huggingface.co/Qwen/Qwen3-Embedding-0.6B | 64.33 / 69.45 / 70.58 MTEB-multi; MRL 32–1024; `Instruct:…\nQuery:`; docs no prefix | §4.1 |
| llama.cpp Qwen3 embedding | 2025-10 → 2026-04 | github.com/ggml-org/llama.cpp/discussions/16787 | `--embedding --pooling last`; prefix passed in text | §4.1 |
| Qwen3 reranker on llama-server | 2026 | gist.github.com/VooDisss/42bce4eb5c76d3c325633886c5e348ee | `/v1/rerank`, `pooling=rank`, conversion fix | §4.3 |
| KaLM-Embedding-Gemma3-12B-2511 | 2025-11 | huggingface.co/tencent/KaLM-Embedding-Gemma3-12B-2511 | MMTEB 72.32 #1; 3840-d MRL | §4.1 bake-off |
| Qwen3-VL-Embedding | 2026-01 | arxiv.org/abs/2601.04720 | 2B hard R@1 0.945 | §4.1 |
| Contextual vs late chunking | 2025-04 / 2026 | arxiv.org/abs/2504.19754; denser.ai; medium/KX | −67 % top-20 failures (contextual+rerank); late chunking gains with length | §3.2 |
| HypRAG (Lorentz dense retrieval) | 2026-02/06 | arxiv.org/abs/2602.07739 | up to +29 % relevance; +20 % radial general→specific | §5.4 |
| HyperbolicRAG | 2025-11 | arxiv.org/abs/2511.18808 | Poincaré + mutual-ranking fusion | §5.4 |
| HyperRAG | ICLR 2026 sub. | openreview.net/forum?id=PSrABo8b1z | query-centric hyperbolic graph | §5.4 |
| HIT-Leiden | 2026-01/06 | arxiv.org/abs/2601.08554 | 5 orders of magnitude; ±0.5 % modularity; 999 batches | §5.3 |
| Zep/Graphiti vs Mem0 | 2026 | vectorize.io/articles/mem0-vs-zep; arxiv 2501.13956 | 63.8 % vs 49.0 % LongMemEval | §2 |
| HippoRAG 2 | 2025–26 | emergentmind.com/topics/hipporag-2; arxiv 2502.14802 | MuSiQue F1 44.8→51.9; 9M vs 115M index tokens | §2, §4.5 |
| LongMemEval-V2 | 2026-05 | xiaowu0162.github.io/longmemeval-v2 | 451 q; 115M-token haystacks; baselines 42.8–74.9 % | §2 |
| MCP 2026-07-28 | 2026-07-28 | modelcontextprotocol.io/specification/2026-07-28/changelog | stateless; discover; headers; ttlMs; tasks extension | §10 |
| three.js WebGPU | 2026-03 | utsubo.com/blog/threejs-2026-what-changed | r171 prod; r184 alloc fix; >1M particles | §9 |
| Cosmograph | 2026 | cosmograph.app/docs-general/concept | million-node GPU layout in seconds (2-D) | §9 |
| Qwen3.6 local | 2026-07 | unsloth.ai/docs/models/qwen3.6 | 27B needs 15–18 GB at 3–4 bit | §2 |
| GLM-5.3-Flash | 2026-08/09 | docs.z.ai (pricing; vlm/glm-5.3-flash); Artificial Analysis 2026-08-26 | 0.075/0.015/0.25 promo; 57 pts @ $0.045/task; 1M ctx; native multimodal | §2, §11 |
| DeepSeek V4 | 2026-08-16 sheet | api-docs.deepseek.com/quick_start/pricing | Flash 0.22/0.007/0.66 off-peak; peak ×2 | §2, §11 |
| Anthropic pricing | 2026-09 | platform.claude.com/docs/en/about-claude/pricing | Fable 5.1 cache read 0.025×; Sonnet 5 $2/$10 standard | §2, §11 |
| Louvain instability | 2026-09-03 | this box, `store/field.npz` | ARI 0.73–0.86 seeds; 0.76 at +2 % | §2, §5.3 |
| Embedding throughput | 2026-09-03 | this box, :8092 | 18.7 chunks/s; 13.1k tok/s | §2, §3.3 |
| `place` latency | 2026-09-03 | this box | 3.0 s / 16 chunks | §6.1 |
| Eye harness | 2026-09-01 | C:/NEW/eye-harness/ | residual 99.7→80.9 % vs uniform 64→13 %; r/v | §6.1 |
| Scriptorium fence | 2026-09-01 | C:/scriptorium/README.md | 28.5 % / 12.8 % paraphrase-as-quote; 0 % usable model offsets | §7.2 |

Research-agent reports are filed under `docs/sota/` and cited where they changed a decision:
- `SOTA_embeddings-retrieval_2026-09-03.md` (46 searches, ~75 primary fetches): changed §3.2 (no late chunking with last-token models; 512-token structure-aware chunks; transcript granularities), §4.1 (4B is the knee; Voyage 4 shared space as paid fallback; Drift-Adapter for swaps), §4.3 (self-converted Qwen3-Reranker; reranker gated off for transcripts; ColBERT only as a long-document rescorer), §4.5 (convex combination over RRF). Its box-specific throughput numbers are estimates; the measured ones in this document supersede them.
- `SOTA_agent-memory-graphrag_2026-09-03.md` (40 searches, ~95 primary fetches): changed §3.1 (provenance-role typing; byte-exact dedup first), §5.2 (the bi-temporal position ledger with typed operators and audit rows), §6.2 (claim-grain novelty; near-dup cascade; no entity graphs as the novelty substrate), §6.3 (supersession proposed, operator-confirmed), §6.4 (pages; context-aware merging; sleep-time cadence), §7.1 (router law from GraphRAG-Bench), §7.2 (long context over curated bundles; distill-and-evict frontier; tokenizer versioning), §12 (probe design; scoring targets; leaderboard refusal).
- `SOTA_second-brain-prior-art_2026-09-03.md` (25 searches, ~110 primary fetches incl. GitHub/PyPI release APIs): §9 (no prior 3-D semantic render over personal documents; anchoring primitives; WASM physics workers; licence traps) and §13a.
- `SOTA_geometry-render_2026-09-03.md` (45 searches, ~80 primary fetches): rewrote §5.4 (retrieval Euclidean, map hyperbolic; Lorentz float64 with analytic placement Δ = ln(b)/2 and importance → radius; UMAP-3 angles; EVōC/Toponymy hierarchy; consensus Leiden; landmark ParametricUMAP + Procrustes + hysteresis) and §9 (r185, instanced quads, boost uniform, id-buffer picking, 2M-instance budget, licence and library exclusions). Its date corrections (GitHub API over HTML pages) are adopted.
- `SOTA_models-economics-agents_2026-09-03.md` (~40 searches, ~110 primary fetches, Context Arena rendered headless, the 212-page Fable 5.1 system card full-text searched, llama-bench and a speculative-decoding and prompt-cache test run on this GPU): changed §2 (Context Arena numbers; the 128K–256K ceiling law; measured local readers; Qwen3.8-27B as the local quality reader; resident-server flags; the multi-agent literature on the bandwidth framing), §7.2 (instrument and window rules; Opus 5 default, Fable 5.1 on shortfall, never Opus 4.7 or Haiku 4.5; GPT-5.6 Sol's surcharge trap), §8.6 (shared-KV bus literature; prefix-sharing economics), §10 (SDK versions, harness support, worker invocations) and §11 (the provider table with expiries and cache minimums).
