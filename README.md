# connectome

**A self-supervised model of a text stream.** Feed it everything you have written — documents, drafts, filings, notes, chat transcripts — and it builds a field: every passage embedded by meaning, related in seven layers, folded into a community tree that stays put as the corpus grows, laid out in hyperbolic space where **radius is resolution**, and driven by one loop that decides what deserves attention by how badly the field predicted it.

Nobody labels anything. **The corpus is the training signal.** The next document is the teacher, the residual is the loss, and every choice the system makes — which embedder, which chunk size, where the communities lie, what counts as new, what counts as a retelling, which position superseded which — is tuned by how well the field predicts what arrives next. Language models learned language from an unlabelled stream. This is the same trick one level up.

> **Design of record: [`docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md`](docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md)** — 71 KB, every number tagged measured **[M]**, verified **[V]**, derived **[D]**, or bet **[BET]**. Five state-of-the-art research reports (≈ 200 web searches, ≈ 470 primary-source fetches, September 2026) are under [`docs/sota/`](docs/sota/). The [reading receipt](docs/READING-RECEIPT_2026-09-03.md) hashes every source document.

---

## The measurement that grounds it

Score each document against the field built from **only the documents that came before it**. Compare with a shuffled field of the same size. On one estate — 264 documents, 3,585 chunks, 2026-06-30 to 2026-09-03:

| Arrival decile | Time-ordered field | Shuffled control | |
|---|---|---|---|
| 1st (oldest) | **0.306** | 0.421 | field predicts 27 % better |
| 2nd | **0.292** | 0.350 | 17 % better |
| middle | 0.309–0.356 | 0.281–0.332 | **worse** — new fronts opening |
| 10th (newest) | **0.221** | 0.258 | 14 % better; 23 % retellings |

The field learns its corpus, then loses when the author opens a new front, then learns again. **A corpus is not a stationary distribution; it is a stream of fronts.** A design that expects one global fixed point is wrong, and one that reshuffles on every arrival is worse. That single result sets the architecture: converge *within* a front (habituation), open provisional structure *between* fronts (vigilance), and freeze the map so it can hold an identity while both happen.

---

## Who it is for

The same organ, different corpus. The schema is induced, never chosen for a domain.

| | What it holds | What it answers |
|---|---|---|
| **Writers** | drafts, versions, notebooks, research | which passage is the sharpest articulation of a theme across nine drafts; what you already said and forgot |
| **Lawyers** | matters, filings, memos, transcripts | the position taken on an issue, when it changed, which authority superseded which, what contradicts what |
| **Researchers** | papers, notes, results, threads | what is genuinely new in an incoming paper relative to your corpus; bridges between fields nobody linked |
| **Anyone with an archive** | a decade of documents and chat logs | hand a newer model the structure and let it re-derive a topic without re-reading a billion tokens |
| **Agents** | the whole field over MCP | a read plan with spans, a residual gate on ingest, a unit map, a diff of what changed |

---

## Architecture

```
 TAPE ──────────► INDEX ──────────► FIELD ──────────► MAP ──────────► VIEWER
 append-only      dense (int8,      7 relation        Lorentz H³      native C++/CUDA
 hash-chained     two-pass MRL)     slices, frozen    radius = level  focus-and-context
 spans, origin,   + BM25/FTS5       versioned         × importance    time slider,
 trust, dedup     + graph firing    partition tree    Poincaré ball   atlas diff
      │                │                 │                 │
      └────────────────┴─────────────────┴─────────────────┘
                              │
             ┌────────────────┼─────────────────┬──────────────────┐
        ATTENTION          RESCAN            THE BUS            SERVE
        residual gate,     skeleton →        Intercom +         stateless MCP
        fronts (CUSUM),    attend →          one sentry at      (2026-07-28),
        vigilance,         articulate →      world rate,        pricebook,
        position ledger    reproject →       typed deltas       harness workers
                           vintage + diff
```

**The loop, in one sentence:** a new document is placed against the field, its residual sets its priority, high-priority passages are read *with their map slice* (the community's gist, the neighbours, the era), what changed is written back as typed deltas, and the shape of the field biases what gets read next.

**The rescan:** hand a newer model the skeleton of a topic — timeline with retellings collapsed, communities, eras, bridges, dark matter, contested positions, the forgotten — as a pinned prefix, let it read surgically by residual inside a hyperbolic ball, articulate with quotes located in the tape by deterministic code, then reproject every source view against the articulation (reconciled / superseded / branch / forgotten). Cost of one topic: **$0.03 on a flash model, ≈ $2.20 on a frontier one** — instead of re-reading the corpus.

---

## Measured, on one box

RTX 4070 Ti SUPER 16 GB, Windows, llama.cpp b9627. All numbers reproducible from the repo.

| | |
|---|---|
| Embedding throughput (Qwen3-Embedding-0.6B Q8) | 18.7 chunks/s ≈ **13.1k tok/s** |
| Brute-force cosine, 3,585² | **73 ms** (CPU) |
| `place` verdict on a 16-chunk document | 3.0 s today → **≤ 100 ms** target (native) |
| Local reader prefill / generation (Qwen3.5-9B Q5) | 4,148 / 71 tok/s |
| Shared-prefix re-prefill with prompt cache | 1,664 tokens → **16 ms** |
| Louvain community stability across seeds | ARI **0.73–0.86** → the partition must be frozen |
| Gromov δ / diameter of the embedding space (p99) | **0.054** → not a tree; hierarchy is imposed, not fitted |
| Query instruction prefix (n = 28 free goldens) | recall@10 0.750 → **0.786** |

And from the frontier, September 2026 (why the design caps every read at 128K–256K tokens): measured 8-needle recall at 128K is **91.3 %** for the best frontier model, **81.8 %** for the best open one, **62.9 %** for the cheap flash lanes, and **≈ 1 %** for one widely-used model. A 1M-token window is storage, not reasoning.

---

## What runs today

The v0.1 Python organ, built and exercised on one estate (264 documents, 3,585 chunks, 17,828 transcript messages, 160 bridges, 590 retellings):

```
python connectome.py about                     the organ's self-description (JSON)
python connectome.py build [--transcripts 30]  chunk → embed (local) → 7 slices → communities → layouts → store/
python connectome.py ask "question" [--json]   read plan: BM25 ∥ vectors ∥ graph firing → fusion → spans + stamps
python connectome.py place FILE [--json]       residual gate: RETELLING | ROUTINE | RELATED | BRIDGING | NOVEL
python connectome.py dossier --topic X         the skeleton a newer model reads first
python connectome.py codex [--cap 0.25]        the unit map per community, cited, with a diff vs the last generation
python connectome.py render                    scene.html — two geometries, layers, time slider, inspector
python connectome.py mcp                       MCP server: recall, place_file, dossier, what_changed, unit_map
python connectome.py providers                 the priced lane table (unknown or undated lane → refused)
```

```bash
claude mcp add connectome -- python C:/connectome/connectome.py mcp
```

**Not yet built:** the frozen versioned partition, the analytic Lorentz placement, the position ledger, the sentry on the bus, the native viewer, and the 10¹⁰-token tier. Those are the milestones below. The browser page shipped here is a prototype and becomes a thin export.

### The native core — M0 gate passing

[`native/`](native/) holds the C++20/CUDA core, built in the operator's own conventions (archs 89/90/120, static runtimes, Ninja from the VS 2022 environment, machine-checkable gates).

```powershell
scripts\build.ps1 -Native          # configure + build for this machine's GPU
scripts\gate.ps1 -Milestone M0     # 5/5 ctest, cross-process digest equality, doctor
build\cx.exe doctor                # what this machine has and is missing
build\cx.exe bench --n 2000000     # the two-pass scan, measured
```

The int8 two-pass scan is implemented and gated. Measured on this box, 2026-09-03:

| coarse pass over | CPU reference | GPU, copied per query | **GPU resident** |
|---|---|---|---|
| 250k chunks (30.5 MiB) | 9.00 ms | 13.05 ms | **0.29 ms — 102 GiB/s** |
| 2M chunks (244 MiB) | 68.37 ms | 88.61 ms | **2.02 ms — 118 GiB/s** |

Every path returns **bit-identical** scores: int32 sums of int8 products with a fixed-topology warp reduction and no float atomics, so determinism is a property of the arithmetic rather than a tolerance. An exact brute-force scan of two million chunks in two milliseconds is why there is no ANN index here to build, tune, or let rot. The middle column is kept in the benchmark on purpose: copying the matrix per query loses to the CPU, which is precisely the shape the design refuses.

---

## Build order (machine-gated, no kickoff document)

Each milestone has a gate that exits 0 or the milestone is not done. A session reads the spec, the receipt, and the gate log, and continues.

- **M0 · Native skeleton ✓** — CMake in the operator's conventions (archs 89/90/120, static runtimes), tape reader, int8 two-pass scan, `doctor`. *Gate: byte-identical scans across runs and against the reference.*
- **M1 · The loss ✓** — temporal-holdout harness (build before *t*, score after *t*, shuffled control), gated. Reproduces the convergence table above and detects the estate's one front: 2026-08-10, `MEANDER-SPEC` through the BLACKBOX burst, 21 documents. `harness/README.md` carries the receipt and the three defects fixed along the way. *Carried forward:* the embedder and chunk-size arms.
- **M2 · The frozen field** — consensus Leiden partition v1, assignment + bounded refinement, drift meter, provenance slice, position ledger with typed operators and audit rows.
- **M3 · The map and the viewer** — UMAP-3 angles, analytic Lorentz placement, Procrustes + hysteresis, native viewer at 60 fps.
- **M4 · Attention** — learned quantiles, fronts, vigilance, habituation, typed deltas, unit map with diff, pages.
- **M5 · The rescan** — skeleton → surgical reads → fence-derived spans → reprojection → vintage and diff.
- **M6 · The bus** — the sentry on Intercom, typed verdicts, per-lane digests, harness workers.
- **M7 · Scale** — 172M tokens, then the 10¹⁰-token tier with NVMe-mapped vectors.

---

## Why this does not exist yet

Checked against the field on 2026-09-03 ([full survey](docs/sota/SOTA_second-brain-prior-art_2026-09-03.md)): retrieval, 3-D rendering, MCP and local storage are commodities; bi-temporal supersession is solved by Graphiti and borrowed here. But **no project renders embedding-similarity edges in 3-D over a person's own documents** — every "3-D graph" plugin draws hand-made links — **every 3-D tool re-runs its force layout from random seeds each session**, and **nobody decides novelty at the idea grain over prose**. The identity-holding layout that biases what an agent attends to is the unbuilt core, and it is what this repo is for.

---

## The laws it keeps

1. **The tape is truth.** Every structure above it is a rebuildable fold. Delete the store; rebuild from the files.
2. **Nothing closes a claim.** `ask` returns spans; the unit map is narrative with citations; quotes are located in the tape by deterministic code, never trusted from a model.
3. **No human label gates anything.** Evaluation is temporal holdout with a shuffled control. Ratings are more tape.
4. **Retellings are kept and counted**, never mistaken for bridges. **Staleness is a sampler, not a priority.**
5. **The map holds still.** The partition is a versioned artifact; nodes move only past a displacement threshold; a version event says so.
6. **Supersession is proposed, and the future confirms it.** A memory that updates from whatever was said last drifts toward the last speaker.
7. **No organ outlives its null.** Every claim ships with the experiment that kills it — fourteen of them, all label-free.

---

## Documentation

- **[v5.5 — The Field](docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md)** — the design of record.
- [Reading receipt](docs/READING-RECEIPT_2026-09-03.md) — 21 source documents, 1.2 MB, hashed.
- State of the art, September 2026: [embeddings & retrieval](docs/sota/SOTA_embeddings-retrieval_2026-09-03.md) · [agent memory & GraphRAG](docs/sota/SOTA_agent-memory-graphrag_2026-09-03.md) · [geometry & rendering](docs/sota/SOTA_geometry-render_2026-09-03.md) · [models & economics](docs/sota/SOTA_models-economics-agents_2026-09-03.md) · [prior art](docs/sota/SOTA_second-brain-prior-art_2026-09-03.md).
- Lineage: [v0.1 rendered](docs/CONNECTOME_v0.1_THE-SECOND-BRAIN-RENDERED_2026-09-01.md) · [v0.2 the slide rule](docs/CONNECTOME_v0.2_THE-SLIDE-RULE-CONNECTOME_2026-09-01.md) · [v0.3 the rescan](docs/CONNECTOME_v0.3_THE-RESCAN_2026-09-01.md) · [notes on adjacent architectures](docs/NOTES_BRAIN-HYPERCELL-HYPERCOM_2026-09-02.md).

## Requirements

Today: Python ≥ 3.12 · numpy · scikit-learn · umap-learn · networkx · rank_bm25 · tiktoken · `mcp` · a llama.cpp embedding server · a token-aware chunker. Specified: CUDA 12.9+/13.x, CMake ≥ 3.27, MSVC 2022 or Clang, an NVIDIA GPU (compute 89/90/120). Optional paid lanes are priced, capped, dated and refused when unknown.

MIT © 2026 Bo Chen.
