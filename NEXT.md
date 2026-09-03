# NEXT — where this stands and how to proceed
**Written 2026-09-01 (late), for whoever opens this repo next: Bo, a new session, or anyone else. Nothing here is private. Read this, then `README.md`, then `docs/` in version order.**

## Where it stands tonight

- **The organ runs.** `connectome.py` has `about`, `build`, `ask`, `place`, `codex`, `dossier`, `render`, `mcp`, `providers`. Built on one estate: ≈ 264 documents, ≈ 3,585 chunks, six relation slices, ten communities, 160 bridges, 590 retellings kept apart, ≈ 18k transcript messages from everywhen's shards. A warm rebuild takes ≈ 100 s.
- **The page renders** in two geometries (Euclidean, Poincaré ball) with a time slider, layers, search, an inspector that shows spans verbatim, and the bridge list.
- **Gear two works** under a hard cap: one unit-map generation on DeepSeek V4 Flash cost $0.0041 and produced ten cited community paragraphs.
- **The MCP server works** (verified by handshake): `recall`, `place_file`, `dossier_tool`, `what_changed_tool`, `unit_map_tool`.
- **The designs** are in `docs/`: v0.1 (the render and the survey), v0.2 (the slide-rule geometry, the stability law, the Carmack layer, the finder seam, the provider seam), v0.3 (the rescan: re-crystallizing a topic under a new model).
- **Nothing pre-registered has run.** Every falsifier in the three designs is still a promise. That is the honest status and the reason for the order below.

## The recommendation, in order

1. **Use it for a week before building more.** Register the server (`claude mcp add connectome -- python C:/connectome/connectome.py mcp`) and start sessions by calling `unit_map_tool` and `recall` before pasting context. Measure the **refeed fraction** — the share of the operator's tokens that are context re-supply to sessions — from transcripts before and after (everywhen can compute it). This is F-REFEED, the null every rung must beat. If it does not fall, further organs are decoration.
2. **Run the first rescan on FUSOR under two instruments** (F-VINTAGE). `dossier --topic FUSOR` gives the skeleton; a session with the MCP tools can do the loop by hand: read the skeleton, pull spans by residual through `recall`, write an articulation with chunk citations. Once on DeepSeek Flash (cents), once on the strongest model available; blind-rate the two against the same spans. This decides whether "smarter model, same corpus" buys anything for a topic the operator knows cold.
3. **Cards through Scriptorium's harness lane** (≈ $0.20 for the markdown corpus on Flash): claims with polarity and time → the claim table, supersession edges, the forgotten list, honest reprojection. This is what turns the skeleton from documents into evidence.
4. **The live lane:** tail the current session at boundaries, `place` each new chunk, post NOVEL and BRIDGE verdicts to Intercom. Makes the connectome present rather than consulted. Wait for step 1 to show sessions read what it writes.
5. **Render work only after function:** true level radius in the Poincaré ball, anchored re-layout (F-LAYOUT-STABLE), the 3-D versus 2-D test on the operator (F-3D-VS-2D).
6. **Corpus #1 last:** ≈ 10 h of local embedding for the 172-million-token extracted tape, only after steps 1–3 have receipts.

Two small things on the way: replace the hard-coded `ROOTS` with a manifest fed by facet tapes (`facet --paths ...`), so adding documents is a query rather than an edit; and let the chunker's `--overlap 0` fix land so the build can drop the `--overlap 40` workaround.

**What not to do:** no v0.4, no new stratum, no second product surface until F-REFEED and F-VINTAGE have numbers.

## How to start a session on this

1. `python C:/connectome/connectome.py about` — the organ's state and health.
2. Read `docs/CONNECTOME_v0.3_THE-RESCAN_2026-09-01.md`, then v0.2, then v0.1.
3. Requirements: the embedding server on `:8092` (llama.cpp, qwen3-embedding-0.6b), `C:/chunker`, `DEEPSEEK_API_KEY` in the environment for gear two, everywhen's shards for transcripts. Windows: forward-slash paths in every shell command; consoles forced to UTF-8.
4. If the store is missing or stale: `python C:/connectome/connectome.py build --transcripts 30` (≈ 100 s warm, ≈ 15 min cold). Run it detached; it can exceed a tool's 10-minute cap when cold.

## A note for later: the transcript converter

Bo has hundreds of coding sessions whose content is now inside JSON transcripts. **everywhen already does most of the conversion**: it folds every Claude Code and DSH transcript into per-day SQLite shards (spine messages, tool-call gists, fork dedup by uuid, FTS5, int8 vectors). A future "filter out all the text and make sense of it" is a reader over those shards plus the connectome's `place` and `dossier`, not a new parser. Not tonight.

## The metric that decides everything

The refeed fraction. If sessions equipped with these tools need less hand-fed context, and if a new model's articulation of a known topic is preferred blind, the connectome is a memory. If not, it is a picture, and this file should say so in its next revision.
