# connectome

**A field over your documents and transcripts that machines consult and one human can see.** Every chunk is embedded locally, placed by meaning, related in layers (semantic, lexical, containment, succession, retellings), folded into communities, and rendered as a 3-D scene — Euclidean, or a Poincaré ball where the rim is infinitely far and there is always room for one more leaf. Agents get tools: a **read plan** (spans, never an answer), a **residual gate** (how badly a new document fits what you already know), and a **unit map** (what each region of the corpus believes, with citations) whose **diff** answers "what changed in my understanding?"

It is not a note-taking graph. A graph of hand-made links with a force layout carries no meaning in its positions, is read by nothing, and changes nothing. This is a fitted field with a gate on the door and a null it can lose to.

## What it does today (v0.1 organ, R1)

```
python connectome.py about                       the organ's self-description (JSON)
python connectome.py build [--transcripts 30]    chunk -> embed (local llama.cpp, cached) -> six relation slices
                                                 -> Louvain communities -> UMAP-3 + hyperbolic layouts -> store/
python connectome.py ask "question" [--json]     read plan: BM25 || vectors || one hop of graph firing -> RRF -> spans
python connectome.py place FILE [--json]         residual gate: residual per chunk, nearest communities, bridges,
                                                 priority = residual / lane volatility; verdict RETELLING|NOVEL|BRIDGING|ROUTINE|RELATED
python connectome.py codex [--dry-run] [--cap 0.25]   gear two: the unit map per community (cited) + diff vs last generation
python connectome.py dossier --topic FUSOR       the skeleton of one topic: documents in time, retellings collapsed,
                                                 bridges, dark matter, and a read plan — what a new model reads first
python connectome.py render                      store/scene.json -> scene.html (3d-force-graph, two geometries, time slider)
python connectome.py mcp                         MCP stdio server: recall, place_file, what_changed_tool, unit_map_tool
python connectome.py providers                   the gear-two lane table (unknown or unpriced lane -> refused)
```

Register the tools with your agent harness, e.g. Claude Code:

```
claude mcp add connectome -- python C:/connectome/connectome.py mcp
```

## How it works

- **Gear one is local and free:** chunking (a token-aware chunker), embeddings from a llama.cpp embedding server (`:8092`, 1024-d; results cached on disk by text hash), brute-force cosine over all chunk vectors (scan, don't seek), TF-IDF for the lexical slice, Louvain for communities, UMAP for positions (Euclidean and hyperboloid → Poincaré ball).
- **Gear two is priced, capped and fingerprinted:** one provider seam (OpenAI-compatible chat completions), a pinned price per lane, a hard USD cap per run, a receipt beside every generation. DeepSeek V4 Flash is the default; Kimi, GLM, OpenAI, OpenRouter and Gemini are rows to pin before first spend.
- **Transcripts** come from [everywhen](https://github.com/bochen2029-pixel)'s concordance shards (Claude Code and DeepSeek Harness sessions, forks deduplicated, int8 vectors) — read, never re-embedded.
- **The store is a fold.** Delete `store/` and rebuild it from the files; nothing in it is truth. The tape (your files, your transcripts) is.

## The laws it keeps

1. The tape is truth; every structure is a rebuildable fold over it.
2. Nothing here closes a claim: `ask` returns spans with coordinates; `codex` is narrative with citations.
3. Retellings are kept and counted, never mistaken for bridges (cosine ≥ 0.97 across documents is a retelling).
4. Staleness is a sampler, not a priority term; the gate weights residual by a belief-free lane volatility.
5. No organ outlives its null: every design claim ships with the experiment that can kill it (see `docs/`).

## Design

- [v0.1 — the connectome, rendered](docs/CONNECTOME_v0.1_THE-SECOND-BRAIN-RENDERED_2026-09-01.md): the audit of the parts, the survey of what exists, the estate-splat, six falsifiers.
- [v0.2 — the slide-rule connectome](docs/CONNECTOME_v0.2_THE-SLIDE-RULE-CONNECTOME_2026-09-01.md): radius is the log of resolution; never full; stability and plasticity mechanized; curriculum; the Carmack layer; the finder-organ seam; the two-gear provider seam.
- [v0.3 — the rescan](docs/CONNECTOME_v0.3_THE-RESCAN_2026-09-01.md): re-crystallizing a topic under a new model without re-reading everything — skeleton, attend, reproject, vintage and diff; the forgotten organ.

## Status, honestly

Built and exercised on one estate (≈ 260 documents, ≈ 3,600 chunks, ≈ 18k transcript messages) on one Windows box with one 16 GB GPU. The render, `ask`, `place`, `codex`, `dossier` and the MCP tools run. None of the pre-registered falsifiers has run yet; the hyperbolic radius is a manifold radius with documents placed inward by a fixed factor, not yet a true level count; lane volatility starts empty. Windows-first (forward-slash paths; UTF-8 consoles forced).

## Requirements

Python ≥ 3.12 · numpy · scikit-learn · umap-learn · networkx · rank_bm25 · tiktoken · `mcp` (for the server) · a running llama.cpp embedding server · the chunker (`C:/chunker/chunker.py`, token-aware, boundary-respecting).

MIT © 2026 Bo Chen.
