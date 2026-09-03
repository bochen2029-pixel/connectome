#!/usr/bin/env python
"""
connectome -- the estate's connectome as an organ: a field over the tape, consulted by machines, rendered for one human.

  python C:/connectome/connectome.py about                     the organ's self-description as JSON (what `peek env` reads)
  python C:/connectome/connectome.py build [--transcripts N]   fold the corpus: chunk -> embed (local :8092, cached) -> slices
                                                               -> communities -> positions (Euclidean + Poincare) -> store/
                                                               --transcripts N adds everywhen's spine messages from the last N days
                                                               (their int8 vectors read from the concordance shards, never re-embedded)
  python C:/connectome/connectome.py ask "question" [--k 8] [--json]
                                                               a READ PLAN, never an answer: BM25 || vector || 1-hop graph -> RRF -> spans
  python C:/connectome/connectome.py place FILE [--json]      the residual gate: how badly a new document fits the field
                                                               (residual per chunk, nearest communities, bridges, priority = r / v)
  python C:/connectome/connectome.py codex [--provider deepseek] [--cap 0.25] [--dry-run]
                                                               gear two: the unit map (what each community believes) + its diff
  python C:/connectome/connectome.py render                    store/scene.json -> scene.html (the page)
  python C:/connectome/connectome.py mcp                       MCP stdio server: recall / place / what_changed / unit_map
  python C:/connectome/connectome.py providers                 the provider table (gear two lanes; unknown lane -> REFUSED)

Laws inherited: the tape is truth and the store is a fold (delete store/, rebuild); nothing here closes a claim -- every
answer is spans with coordinates; gear one (local) is the always-available floor; gear two is priced, capped, fingerprinted.
"""
import argparse
import glob
import hashlib
import json
import math
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "store")
PROTO = os.path.join(HERE, "proto")
CHUNK_DIR = os.path.join(PROTO, "_chunks")            # reuse the R0 chunk cache
CACHE_PATH = os.path.join(PROTO, "_embed_cache.npz")   # reuse the R0 embedding cache
CHUNKER = "C:/chunker/chunker.py"
EMBED_URL = os.environ.get("CONNECTOME_EMBED_URL", "http://127.0.0.1:8092/v1/embeddings")
CONCORDANCE = os.path.join(os.path.expanduser("~"), ".claude", "concordance", "shards")
VERSION = "0.1.0"
BUDGET = int(os.environ.get("CX_BUDGET", "700"))
MAX_FILE_BYTES = 320_000
SNIPPET_CHARS = 700
DUP_TH, BR_TH, TH_CHUNK, TH_DOC, TH_LEX = 0.97, 0.62, 0.60, 0.50, 0.22

ROOTS = [
    ("C:/NEW", "NEW"), ("C:/NEW/INTELLECT", "INTELLECT"), ("C:/NEW/eye-harness", "eye-harness"),
    ("C:/NEW/ANOMALY-LEDGER", "anomaly-ledger"), ("C:/Intercom/sandbox/CALIBRAN-4242/ROUNDTABLE-ISOMORPH", "roundtable"),
    ("C:/Intercom/sandbox", "meta-final"), ("C:/Cortex", "cortex"), ("C:/chunker", "one-pagers"),
    ("C:/hypercelld", "hypercelld"), ("C:/MEANDER", "meander"), ("C:/scriptorium", "scriptorium"),
    ("C:/Intercom", "intercom"), ("C:/hypercell_v5", "hypercell"), ("C:/ORRERY", "orrery"), ("C:/SURVEYOR", "surveyor"),
    ("C:/facet", "facet"), ("C:/everywhere", "everywhere"), ("C:/everywhen", "everywhen"), ("C:/Everything", "everything"),
    ("C:/connectome", "connectome"),
]
SKIP_NAME = re.compile(r"(REDACTION_LOG|_manifest|INDEX\.md$|^chunk-\d+\.md$|INTELLECT_FULL|_REDACTED|_lineage_|BUILD_LOG)")

PROVIDERS = {
    # gear two lanes: OpenAI-compatible chat completions. Prices USD per 1M tokens where pinned; TODO = unpriced -> refused for spend.
    "deepseek": dict(base="https://api.deepseek.com/chat/completions", model="deepseek-v4-flash",
                     vision="deepseek-v4-flash-vision-exp", env="DEEPSEEK_API_KEY",
                     price=dict(in_miss=0.14, in_hit=0.0028, out=0.28), verified="2026-07-31 (text) / 2026-08-21 (vision)",
                     extra=dict(thinking={"type": "disabled"})),
    "kimi": dict(base="https://api.moonshot.ai/v1/chat/completions", model="kimi-k2.6", vision="kimi-k2.6 (native, MoonViT)",
                 env="MOONSHOT_API_KEY", price=None, verified="model names 2026-09 (search); prices TODO"),
    "glm": dict(base="https://open.bigmodel.cn/api/paas/v4/chat/completions", model="glm-5-turbo", vision="glm-5v-turbo",
                env="ZHIPU_API_KEY", price=None, verified="GLM-5V-Turbo 2026-04-01 (search); prices TODO"),
    "openai": dict(base="https://api.openai.com/v1/chat/completions", model="TODO", vision="native", env="OPENAI_API_KEY",
                   price=None, verified="TODO"),
    "openrouter": dict(base="https://openrouter.ai/api/v1/chat/completions", model="TODO", vision="per model",
                       env="OPENROUTER_API_KEY", price=None, verified="TODO"),
    "gemini": dict(base="https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", model="TODO",
                   vision="native", env="GEMINI_API_KEY", price=None, verified="TODO"),
}


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# ----------------------------------------------------------------------------- intake (gear one, local)

def date_of(path):
    m = re.search(r"(20\d\d)-(\d\d)-(\d\d)", os.path.basename(path))
    if m:
        return "%s-%s-%s" % m.groups()
    return time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(path)))


def collect_files():
    seen, files = set(), []
    for root, label in ROOTS:
        for f in sorted(glob.glob(root + "/*.md")):
            key = os.path.normcase(os.path.abspath(f))
            if key in seen or SKIP_NAME.search(os.path.basename(f)):
                continue
            sz = os.path.getsize(f)
            if sz < 800 or sz > MAX_FILE_BYTES:
                continue
            seen.add(key)
            files.append((f, label))
    return files


def chunk_file(path, out_dir=None):
    """Run the chunker organ as a subprocess; return [(section, text)]. --overlap 0 hangs the chunker; 40 is the floor."""
    out = out_dir or os.path.join(CHUNK_DIR, re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.basename(path)) + ".chunks")
    if not os.path.isdir(out):
        r = subprocess.run([sys.executable, CHUNKER, "--budget", str(BUDGET), "--overlap", "40", "--out", out, path],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            log("chunker failed on", path, r.stderr[-300:])
            return []
    chunks = []
    for cf in sorted(glob.glob(os.path.join(out, "chunk-*.md"))):
        lines = open(cf, encoding="utf-8", errors="replace").read().split("\n")
        section, body_start, in_recap = "", 0, False
        for i, ln in enumerate(lines):
            if ln.startswith("<!--"):
                m = re.match(r"<!--\s*section:\s*(.*?)\s*-->", ln)
                if m:
                    section = m.group(1)
                if "recap:" in ln:
                    in_recap = True
                body_start = i + 1
                continue
            if in_recap and (ln.startswith(">") or ln.strip() == ""):
                body_start = i + 1
                if ln.strip() == "" and i > 0 and lines[i - 1].startswith(">"):
                    in_recap = False
                continue
            break
        text = "\n".join(lines[body_start:]).strip()
        if len(text) > 200:
            chunks.append((section, text))
    return chunks


def _key(t):
    return hashlib.blake2b(t.encode("utf-8"), digest_size=16).hexdigest()


def load_cache():
    if not os.path.exists(CACHE_PATH):
        return {}
    z = np.load(CACHE_PATH, allow_pickle=False)
    return dict(zip([k for k in z["keys"]], z["vecs"]))


def save_cache(cache):
    if not cache:
        return
    keys = np.array(list(cache.keys()))
    vecs = np.array([cache[k] for k in keys], dtype=np.float32)
    tmp = CACHE_PATH + ".tmp.npz"
    np.savez(tmp, keys=keys, vecs=vecs)
    os.replace(tmp, CACHE_PATH)


def embed_batch(texts):
    req = urllib.request.Request(EMBED_URL, data=json.dumps({"input": texts}).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
    return [e["embedding"] for e in sorted(d["data"], key=lambda e: e["index"])]


def embed_all(texts, batch=4, workers=3, use_cache=True):
    cache = load_cache() if use_cache else {}
    keys = [_key(t) for t in texts]
    vecs = [cache.get(k) for k in keys]
    todo = [i for i, v in enumerate(vecs) if v is None]
    if todo:
        log("embedding: %d cached, %d to do" % (len(texts) - len(todo), len(todo)))
    lock = __import__("threading").Lock()

    def work(start):
        ids = todo[start:start + batch]
        try:
            out = embed_batch([texts[i] for i in ids])
        except Exception:
            out = []
            for i in ids:
                try:
                    out.append(embed_batch([texts[i]])[0])
                except Exception as ex:
                    log("embed failed:", repr(ex)[:100])
                    out.append(None)
        with lock:
            for i, v in zip(ids, out):
                if v is not None:
                    vecs[i] = np.asarray(v, dtype=np.float32)
                    cache[keys[i]] = vecs[i]

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(work, range(0, len(todo), batch)))
    if todo and use_cache:
        save_cache(cache)
    X = np.array([np.zeros(1024, np.float32) if v is None else v for v in vecs], dtype=np.float32)
    X /= (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    return X, [v is not None for v in vecs]


def tokens_of(text):
    try:
        import tiktoken
        return len(tiktoken.get_encoding("o200k_base").encode(text))
    except Exception:
        return max(1, len(text) // 4)


# ----------------------------------------------------------------------------- transcripts (everywhen's shards)

def read_transcripts(days):
    """Spine messages from everywhen's shards that already carry vectors (int8 * scale). Never re-embedded."""
    since = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() - days * 86400))
    rows, vecs = [], []
    for shard in sorted(glob.glob(os.path.join(CONCORDANCE, "*.db")))[-3:]:
        try:
            c = sqlite3.connect("file:%s?mode=ro" % shard.replace("\\", "/"), uri=True)
            q = ("select m.uuid, m.ts, m.project, m.session_uuid, m.role, m.file, m.line, m.text, v.scale, v.q "
                 "from vec v join messages m on m.uuid = v.uuid where v.chunk = 0 and m.class = 0 and m.ts >= ? "
                 "and length(m.text) >= 120")
            for r in c.execute(q, (since,)):
                qv = np.frombuffer(r[9], dtype=np.int8).astype(np.float32) * float(r[8])
                if qv.shape[0] != 1024:
                    continue
                rows.append(dict(uuid=r[0], ts=r[1], project=r[2], session=r[3], role=r[4], file=r[5], line=r[6], text=r[7]))
                vecs.append(qv)
        except Exception as ex:
            log("transcript shard skipped:", os.path.basename(shard), repr(ex)[:80])
    if not rows:
        return [], np.zeros((0, 1024), np.float32)
    V = np.array(vecs, dtype=np.float32)
    V /= (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)
    return rows, V


# ----------------------------------------------------------------------------- the fold

def build(transcript_days=0):
    t0 = time.time()
    os.makedirs(STORE, exist_ok=True)
    os.makedirs(CHUNK_DIR, exist_ok=True)
    files = collect_files()
    docs, chunks = [], []
    for path, label in files:
        cs = chunk_file(path)
        if not cs:
            continue
        di = len(docs)
        full = open(path, encoding="utf-8", errors="replace").read()
        docs.append(dict(i=di, n=os.path.basename(path)[:-3], p=label, f=path, t=date_of(path), tk=tokens_of(full), text=full, chunks=[]))
        for section, text in cs:
            ci = len(chunks)
            chunks.append(dict(i=ci, d=di, s=section[:160], text=text, tk=tokens_of(text), t=docs[di]["t"], p=label))
            docs[di]["chunks"].append(ci)
    log("docs %d chunks %d (%.0fs)" % (len(docs), len(chunks), time.time() - t0))
    X, ok = embed_all([c["text"] for c in chunks])
    keep = [i for i, k in enumerate(ok) if k]
    X = X[keep]
    chunks = [chunks[i] for i in keep]
    for k, c in enumerate(chunks):
        c["i"] = k
    for d in docs:
        d["chunks"] = []
    for c in chunks:
        docs[c["d"]]["chunks"].append(c["i"])
    docs = [d for d in docs if d["chunks"]]
    remap = {d["i"]: k for k, d in enumerate(docs)}
    for k, d in enumerate(docs):
        d["i"] = k
    for c in chunks:
        c["d"] = remap[c["d"]]
    D = np.zeros((len(docs), X.shape[1]), np.float32)
    for d in docs:
        D[d["i"]] = X[d["chunks"]].mean(axis=0)
    D /= (np.linalg.norm(D, axis=1, keepdims=True) + 1e-9)

    links = []
    chunk_doc = np.array([c["d"] for c in chunks])
    S = X @ X.T
    np.fill_diagonal(S, -1)
    S_cross = np.where(chunk_doc[:, None] == chunk_doc[None, :], -1, S)
    seen, dups = set(), 0
    for i in range(len(chunks)):
        for j in np.argpartition(-S_cross[i], 3)[:3]:
            w = float(S_cross[i, j])
            if w < TH_CHUNK:
                continue
            key = (min(i, j), max(i, j))
            if key in seen:
                continue
            seen.add(key)
            if w >= DUP_TH:
                links.append(dict(a="c%d" % key[0], b="c%d" % key[1], l="dup", w=round(w, 3)))
                dups += 1
            else:
                links.append(dict(a="c%d" % key[0], b="c%d" % key[1], l="sem", w=round(w, 3)))
    SD = D @ D.T
    np.fill_diagonal(SD, -1)
    doc_edges, dseen = {}, set()
    for i in range(len(docs)):
        for j in np.argpartition(-SD[i], 4)[:4]:
            w = float(SD[i, j])
            if w < TH_DOC:
                continue
            key = (min(i, j), max(i, j))
            if key in dseen:
                continue
            dseen.add(key)
            links.append(dict(a="d%d" % key[0], b="d%d" % key[1], l="doc", w=round(w, 3)))
            doc_edges[key] = max(doc_edges.get(key, 0), w)
    from sklearn.feature_extraction.text import TfidfVectorizer
    tf = TfidfVectorizer(stop_words="english", max_df=0.85, min_df=2, ngram_range=(1, 2), sublinear_tf=True, max_features=60000)
    T = tf.fit_transform([d["text"] for d in docs])
    L = (T @ T.T).toarray()
    np.fill_diagonal(L, -1)
    lseen = set()
    for i in range(len(docs)):
        for j in np.argpartition(-L[i], 3)[:3]:
            w = float(L[i, j])
            if w < TH_LEX:
                continue
            key = (min(i, j), max(i, j))
            if key in lseen:
                continue
            lseen.add(key)
            links.append(dict(a="d%d" % key[0], b="d%d" % key[1], l="lex", w=round(w, 3)))
            doc_edges[key] = max(doc_edges.get(key, 0), 0.6 * w)
    for c in chunks:
        links.append(dict(a="d%d" % c["d"], b="c%d" % c["i"], l="con", w=1.0))
    by_proj = {}
    for d in docs:
        by_proj.setdefault(d["p"], []).append(d)
    for ds in by_proj.values():
        ds = sorted(ds, key=lambda d: (d["t"], d["n"]))
        for a, b in zip(ds, ds[1:]):
            links.append(dict(a="d%d" % a["i"], b="d%d" % b["i"], l="suc", w=0.5))

    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(range(len(docs)))
    for (i, j), w in doc_edges.items():
        G.add_edge(i, j, weight=w)
    comms = sorted(nx.community.louvain_communities(G, weight="weight", seed=7), key=lambda s: -len(s))
    comm_of = {m: ci for ci, members in enumerate(comms) for m in members}
    terms = np.array(tf.get_feature_names_out())
    comm_rows = []
    for ci, members in enumerate(comms):
        members = sorted(members)
        v = np.asarray(T[members].mean(axis=0)).ravel()
        comm_rows.append(dict(id=ci, label=" · ".join(terms[np.argsort(-v)[:4]]), n=len(members), members=members))
    for d in docs:
        d["c"] = comm_of[d["i"]]
    for c in chunks:
        c["c"] = docs[c["d"]]["c"]
    cand = np.argwhere((S_cross >= BR_TH) & (S_cross < DUP_TH))
    bridges, bseen = [], set()
    for i, j in cand:
        if i >= j or chunks[i]["c"] == chunks[j]["c"]:
            continue
        key = (int(i), int(j))
        if key in bseen:
            continue
        bseen.add(key)
        bridges.append((float(S_cross[i, j]), key[0], key[1]))
    bridges.sort(reverse=True)
    bridges = bridges[:160]
    existing = {(int(l["a"][1:]), int(l["b"][1:])): l for l in links if l["l"] == "sem"}
    for w, i, j in bridges:
        if (i, j) in existing:
            existing[(i, j)]["br"] = 1
        else:
            links.append(dict(a="c%d" % i, b="c%d" % j, l="sem", w=round(w, 3), br=1))
    log("links %d dup %d communities %d bridges %d (%.0fs)" % (len(links), dups, len(comms), len(bridges), time.time() - t0))

    import umap
    Y = umap.UMAP(n_components=3, n_neighbors=15, min_dist=0.12, metric="cosine", random_state=42).fit_transform(X)
    Y = (Y - Y.mean(axis=0)) / (np.abs(Y - Y.mean(axis=0)).max() + 1e-9) * 300.0
    H = umap.UMAP(n_components=3, n_neighbors=15, min_dist=0.12, metric="cosine", output_metric="hyperboloid",
                  random_state=42).fit_transform(X)
    h0 = np.sqrt(1 + (H ** 2).sum(axis=1))
    P = H / (1 + h0)[:, None]                       # Poincare ball, |p| < 1; rim = infinity
    # the slide rule: chunks sit at their manifold radius; a document sits one level inward (mean direction, 0.55 x radius)
    Pc = P * 300.0
    for c in chunks:
        c["x"], c["y"], c["z"] = [round(float(v), 1) for v in Y[c["i"]]]
        c["hx"], c["hy"], c["hz"] = [round(float(v), 1) for v in Pc[c["i"]]]
    for d in docs:
        d["x"], d["y"], d["z"] = [round(float(v), 1) for v in Y[d["chunks"]].mean(axis=0)]
        m = Pc[d["chunks"]].mean(axis=0)
        d["hx"], d["hy"], d["hz"] = [round(float(v), 1) for v in m * 0.55]
    log("layouts done (%.0fs)" % (time.time() - t0))

    trows, TV = ([], np.zeros((0, X.shape[1]), np.float32))
    if transcript_days:
        trows, TV = read_transcripts(transcript_days)
        log("transcripts with vectors from everywhen: %d (last %d days)" % (len(trows), transcript_days))

    nodes = [dict(id="d%d" % d["i"], k="d", n=d["n"], p=d["p"], c=d["c"], t=d["t"], tk=d["tk"], f=d["f"], nc=len(d["chunks"]),
                  x=d["x"], y=d["y"], z=d["z"], hx=d["hx"], hy=d["hy"], hz=d["hz"]) for d in docs]
    nodes += [dict(id="c%d" % c["i"], k="c", d="d%d" % c["d"], n=docs[c["d"]]["n"], s=c["s"], p=c["p"], c=c["c"], t=c["t"], tk=c["tk"],
                   x=c["x"], y=c["y"], z=c["z"], hx=c["hx"], hy=c["hy"], hz=c["hz"], sn=c["text"][:SNIPPET_CHARS]) for c in chunks]
    slice_counts = {}
    for l in links:
        slice_counts[l["l"]] = slice_counts.get(l["l"], 0) + 1
    meta = dict(built=time.strftime("%Y-%m-%d %H:%M"), version=VERSION, files=len(docs), chunks=len(chunks), links=len(links),
                slices=slice_counts, communities=len(comms), bridges=len(bridges), transcripts=len(trows),
                date_min=min(d["t"] for d in docs), date_max=max(d["t"] for d in docs), tokens=sum(d["tk"] for d in docs),
                embedder="qwen3-embedding-0.6b-q8_0 (llama.cpp :8092, 1024-d)",
                layout="UMAP-3 Euclidean and UMAP hyperboloid -> Poincare ball (cosine, n_neighbors=15, min_dist=0.12, seed 42)",
                thresholds=dict(sem=TH_CHUNK, doc=TH_DOC, lex=TH_LEX, bridge=BR_TH, dup=DUP_TH), elapsed_s=round(time.time() - t0))
    json.dump(dict(meta=meta, comms=[dict(id=c["id"], label=c["label"], n=c["n"]) for c in comm_rows], nodes=nodes, links=links),
              open(os.path.join(STORE, "scene.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    np.savez(os.path.join(STORE, "field.npz"), X=X.astype(np.float16), D=D.astype(np.float16), TV=TV.astype(np.float16))
    json.dump(dict(meta=meta, comms=comm_rows,
                   docs=[dict(i=d["i"], n=d["n"], p=d["p"], f=d["f"], t=d["t"], tk=d["tk"], c=d["c"], chunks=d["chunks"]) for d in docs],
                   chunks=[dict(i=c["i"], d=c["d"], s=c["s"], t=c["t"], tk=c["tk"], c=c["c"], text=c["text"]) for c in chunks],
                   transcripts=trows,
                   links=[l for l in links if l["l"] != "con"]),
              open(os.path.join(STORE, "index.json"), "w", encoding="utf-8"), ensure_ascii=False)
    lanes_path = os.path.join(STORE, "lanes.json")
    if not os.path.exists(lanes_path):
        json.dump({}, open(lanes_path, "w"))
    log("store written (%.0fs)" % (time.time() - t0))
    print(json.dumps(meta, indent=1))


# ----------------------------------------------------------------------------- the field, loaded

class Field:
    def __init__(self):
        if not os.path.exists(os.path.join(STORE, "index.json")):
            raise SystemExit("no store; run: connectome build")
        self.idx = json.load(open(os.path.join(STORE, "index.json"), encoding="utf-8"))
        z = np.load(os.path.join(STORE, "field.npz"))
        self.X = z["X"].astype(np.float32)
        self.D = z["D"].astype(np.float32)
        self.TV = z["TV"].astype(np.float32)
        self.chunks = self.idx["chunks"]
        self.docs = self.idx["docs"]
        self.comms = {c["id"]: c for c in self.idx["comms"]}
        self.trans = self.idx.get("transcripts", [])
        self.nbrs = {}
        for l in self.idx["links"]:
            if l["l"] in ("sem", "doc"):
                self.nbrs.setdefault(l["a"], []).append((l["b"], l["w"], l.get("br", 0)))
                self.nbrs.setdefault(l["b"], []).append((l["a"], l["w"], l.get("br", 0)))
        self._bm25 = None

    def bm25(self):
        if self._bm25 is None:
            from rank_bm25 import BM25Okapi
            tok = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
            self._tok = tok
            self._bm25 = BM25Okapi([tok(c["text"]) for c in self.chunks])
        return self._bm25

    def span(self, ci, n=SNIPPET_CHARS):
        c = self.chunks[ci]
        d = self.docs[c["d"]]
        return dict(chunk="c%d" % ci, doc=d["n"], path=d["f"], section=c["s"], date=c["t"], community=self.comms[c["c"]]["label"],
                    text=c["text"][:n])


def ask(q, k=8, as_json=False):
    F = Field()
    qv, ok = embed_all([q], use_cache=False)
    qv = qv[0]
    sims = F.X @ qv
    vec_rank = np.argsort(-sims)[:30]
    bm = F.bm25().get_scores(F._tok(q))
    lex_rank = np.argsort(-bm)[:30]
    rrf = {}
    for r, i in enumerate(vec_rank):
        rrf[int(i)] = rrf.get(int(i), 0) + 1.0 / (60 + r)
    for r, i in enumerate(lex_rank):
        if bm[i] > 0:
            rrf[int(i)] = rrf.get(int(i), 0) + 1.0 / (60 + r)
    # one hop of firing: neighbors of the top seeds, discounted
    for i in list(sorted(rrf, key=lambda i: -rrf[i])[:6]):
        for nb, w, br in F.nbrs.get("c%d" % i, []):
            if nb.startswith("c"):
                j = int(nb[1:])
                rrf[j] = rrf.get(j, 0) + 0.35 * rrf[i] * w
    top = sorted(rrf, key=lambda i: -rrf[i])[:k]
    plan = dict(query=q, kind="read_plan", note="spans, never an answer; cite path + section", spans=[])
    for i in top:
        s = F.span(i)
        s.update(score=round(rrf[i], 4), cosine=round(float(sims[i]), 3), bm25=round(float(bm[i]), 2))
        plan["spans"].append(s)
    if F.TV.shape[0]:
        ts = F.TV @ qv
        tr = np.argsort(-ts)[:4]
        plan["transcript_hits"] = [dict(uuid=F.trans[i]["uuid"], ts=F.trans[i]["ts"], project=F.trans[i]["project"], role=F.trans[i]["role"],
                                        file=F.trans[i]["file"], line=F.trans[i]["line"], cosine=round(float(ts[i]), 3),
                                        text=F.trans[i]["text"][:400]) for i in tr if ts[i] > 0.70]   # unrelated messages sit near 0.6 for this embedder
    absent = max(float(sims[top[0]]) if top else 0.0, 0.0)
    plan["absence_signal"] = "weak field match (best cosine %.2f); consider everywhere for an exact scan" % absent if absent < 0.5 else None
    if as_json:
        print(json.dumps(plan, ensure_ascii=False, indent=1))
    else:
        print("READ PLAN for: %s" % q)
        for s in plan["spans"]:
            print("- [%s] %s › %s  (cos %.2f, bm25 %.1f, score %.4f)\n    %s" % (s["chunk"], s["doc"], s["section"], s["cosine"], s["bm25"], s["score"], s["text"][:200].replace("\n", " ")))
        for h in plan.get("transcript_hits", []):
            print("- [transcript %s %s %s] cos %.2f: %s" % (h["ts"][:10], h["project"], h["role"], h["cosine"], h["text"][:160].replace("\n", " ")))
        if plan["absence_signal"]:
            print("!", plan["absence_signal"])
    return plan


def place(path, as_json=False, lane=None):
    """The residual gate: how badly does this document fit the field? Nothing is written to the field (place proposes)."""
    F = Field()
    lane = lane or os.path.dirname(os.path.abspath(path))
    tmp_out = os.path.join(STORE, "_place", re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.basename(path)) + "." + _key(path)[:8] + ".chunks")
    cs = chunk_file(path, out_dir=tmp_out)
    if not cs:
        raise SystemExit("no chunks from " + path)
    V, ok = embed_all([t for _, t in cs], use_cache=False)
    S = V @ F.X.T                                   # (m, N)
    top1 = S.max(axis=1)
    residual = 1.0 - top1                            # open residual against the field, per chunk
    lanes = json.load(open(os.path.join(STORE, "lanes.json")))
    lane_stat = lanes.get(lane, dict(ema_r2=None, n=0))
    v = math.sqrt(lane_stat["ema_r2"]) if lane_stat["ema_r2"] else None
    r_mean = float(residual.mean())
    priority = r_mean / v if v else None            # r / v: the eye harness's rule; v is the lane's volatility, belief-free
    # nearest communities and bridges per chunk
    chunk_comm = np.array([c["c"] for c in F.chunks])
    out_chunks = []
    bridges = []
    for m in range(V.shape[0]):
        nn = np.argsort(-S[m])[:5]
        comms_hit = [int(chunk_comm[j]) for j in nn]
        ent = 0.0
        for cid in set(comms_hit):
            p = comms_hit.count(cid) / len(comms_hit)
            ent -= p * math.log(p)
        near = [dict(chunk="c%d" % int(j), doc=F.docs[F.chunks[int(j)]["d"]]["n"], section=F.chunks[int(j)]["s"], cosine=round(float(S[m, j]), 3),
                     community=F.comms[int(chunk_comm[j])]["label"]) for j in nn[:3]]
        out_chunks.append(dict(section=cs[m][0][:120], residual=round(float(residual[m]), 3), community_entropy=round(ent, 3), nearest=near))
        # a bridge: this chunk is close to two chunks in different communities
        top_by_comm = {}
        for j in nn:
            cid = int(chunk_comm[j])
            if cid not in top_by_comm and S[m, j] >= BR_TH:
                top_by_comm[cid] = int(j)
        if len(top_by_comm) >= 2:
            ids = list(top_by_comm.values())[:2]
            bridges.append(dict(section=cs[m][0][:80], joins=[dict(doc=F.docs[F.chunks[j]["d"]]["n"], community=F.comms[int(chunk_comm[j])]["label"],
                                                                     cosine=round(float(S[m, j]), 3)) for j in ids]))
    if r_mean < 0.05:
        verdict = "RETELLING"          # already in the field, byte-for-byte or nearly; kept, never a bridge
    elif r_mean > 0.45:
        verdict = "NOVEL"
    elif bridges:
        verdict = "BRIDGING"
    else:
        verdict = "ROUTINE" if r_mean < 0.3 else "RELATED"
    # update the lane's volatility (an EMA of r^2 over what this lane has sent) -- the only state place writes, and it is not the field
    ema = lane_stat["ema_r2"]
    r2 = float((residual ** 2).mean())
    lane_stat["ema_r2"] = r2 if ema is None else 0.9 * ema + 0.1 * r2
    lane_stat["n"] = lane_stat["n"] + 1
    lanes[lane] = lane_stat
    json.dump(lanes, open(os.path.join(STORE, "lanes.json"), "w"), indent=1)
    rep = dict(file=path, lane=lane, chunks=V.shape[0], residual_mean=round(r_mean, 3), residual_max=round(float(residual.max()), 3),
               lane_volatility=round(v, 3) if v else None, priority=round(priority, 3) if priority else None, verdict=verdict,
               bridges=bridges[:8], chunks_detail=out_chunks, note="place proposes; nothing is folded into the field until build")
    if as_json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        print("PLACE %s  lane=%s  chunks=%d  residual mean %.3f max %.3f  v=%s  priority=%s  -> %s" % (
            os.path.basename(path), lane, rep["chunks"], r_mean, rep["residual_max"], rep["lane_volatility"], rep["priority"], verdict))
        for c in out_chunks[:6]:
            print("  r=%.3f H=%.2f  %s -> %s (%s, cos %.2f)" % (c["residual"], c["community_entropy"], c["section"][:50], c["nearest"][0]["doc"][:40],
                                                             c["nearest"][0]["community"][:30], c["nearest"][0]["cosine"]))
        for b in bridges[:5]:
            print("  BRIDGE %s: %s (%s) <-> %s (%s)" % (b["section"][:40], b["joins"][0]["doc"][:30], b["joins"][0]["community"][:20],
                                                     b["joins"][1]["doc"][:30], b["joins"][1]["community"][:20]))
    return rep


# ----------------------------------------------------------------------------- gear two: the provider seam

def provider_call(name, messages, max_tokens=800, temperature=0.0):
    P = PROVIDERS.get(name)
    if not P:
        raise SystemExit("REFUSED: unknown provider lane %r (see: connectome providers)" % name)
    key = os.environ.get(P["env"])
    if not key:
        raise SystemExit("REFUSED: %s not set for provider %s" % (P["env"], name))
    if not P.get("price"):
        raise SystemExit("REFUSED: provider %s has no pinned price; spend is refused until the row is priced" % name)
    body = dict(model=P["model"], messages=messages, temperature=temperature, max_tokens=max_tokens)
    body.update(P.get("extra", {}))
    req = urllib.request.Request(P["base"], data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    u = d.get("usage", {})
    hit = u.get("prompt_cache_hit_tokens", 0)
    miss = u.get("prompt_cache_miss_tokens", u.get("prompt_tokens", 0) - hit)
    out = u.get("completion_tokens", 0)
    usd = (miss * P["price"]["in_miss"] + hit * P["price"]["in_hit"] + out * P["price"]["out"]) / 1e6
    return d["choices"][0]["message"]["content"], dict(model=d.get("model", P["model"]), in_miss=miss, in_hit=hit, out=out, usd=round(usd, 6))


def codex(provider="deepseek", cap=0.25, dry_run=False, per_comm=6):
    """The unit map: what each community believes, from its own most central chunks; then the diff against the last generation."""
    F = Field()
    cdir = os.path.join(STORE, "codex")
    os.makedirs(cdir, exist_ok=True)
    gens = [g for g in sorted(glob.glob(os.path.join(cdir, "gen-*.md"))) if "-dry" not in g]   # dry runs never count
    gen_no = len(gens) + 1
    system = ("You write the unit map of a personal research estate: for one community of documents, state in at most 120 words "
              "what this community establishes, in plain declarative sentences, citing chunk ids in square brackets like [c412]. "
              "Say only what the excerpts support. If the excerpts disagree, say so in one sentence. No preamble.")
    spent, parts, usage_rows = 0.0, [], []
    for cid, c in sorted(F.comms.items()):
        members = c["members"]
        # central chunks: nearest to the community's mean vector
        idxs = [ci for m in members for ci in F.docs[m]["chunks"]]
        mv = F.X[idxs].mean(axis=0)
        mv /= (np.linalg.norm(mv) + 1e-9)
        order = sorted(idxs, key=lambda i: -float(F.X[i] @ mv))[:per_comm]
        excerpts = "\n\n".join("[c%d] %s › %s\n%s" % (i, F.docs[F.chunks[i]["d"]]["n"], F.chunks[i]["s"], F.chunks[i]["text"][:1400]) for i in order)
        user = "COMMUNITY %d (%d documents; label: %s)\n\nEXCERPTS:\n%s" % (cid, c["n"], c["label"], excerpts)
        if dry_run:
            parts.append("## %d · %s\n\n(dry run: %d excerpt tokens ≈)\n" % (cid, c["label"], tokens_of(user)))
            continue
        if spent >= cap:
            parts.append("## %d · %s\n\n(cap reached; not read this generation)\n" % (cid, c["label"]))
            continue
        text, u = provider_call(provider, [dict(role="system", content=system), dict(role="user", content=user)], max_tokens=320)
        spent += u["usd"]
        usage_rows.append(dict(community=cid, **u))
        parts.append("## %d · %s\n\n%s\n" % (cid, c["label"], text.strip()))
    bridges = [l for l in F.idx["links"] if l.get("br")]
    bridges = sorted(bridges, key=lambda l: -l["w"])[:12]
    blines = ["- [%s] %s ⟷ [%s] %s (cos %.2f)" % (l["a"], F.docs[F.chunks[int(l["a"][1:])]["d"]]["n"], l["b"], F.docs[F.chunks[int(l["b"][1:])]["d"]]["n"], l["w"]) for l in bridges]
    head = ("# UNIT MAP · generation %d · %s · provider %s · spent $%.4f (cap $%.2f)%s\n\n"
            "The map's own summary of the territory: narrative, never closes a claim; every sentence cites a chunk id that resolves to a span on the tape.\n\n"
            % (gen_no, time.strftime("%Y-%m-%d %H:%M"), provider, spent, cap, " · DRY RUN" if dry_run else ""))
    body = head + "\n".join(parts) + "\n## Bridges (similar meaning, different community)\n\n" + "\n".join(blines) + "\n"
    out_path = os.path.join(cdir, "gen-%03d%s.md" % (gen_no, "-dry" if dry_run else ""))
    open(out_path, "w", encoding="utf-8").write(body)
    diff_path = None
    if gens and not dry_run:
        import difflib
        prev = open(gens[-1], encoding="utf-8").read().splitlines()
        diff = list(difflib.unified_diff(prev, body.splitlines(), fromfile=os.path.basename(gens[-1]), tofile=os.path.basename(out_path), lineterm="", n=1))
        diff_path = os.path.join(cdir, "diff-%03d.md" % gen_no)
        open(diff_path, "w", encoding="utf-8").write("\n".join(diff))
    json.dump(dict(generation=gen_no, provider=provider, spent_usd=round(spent, 6), cap=cap, usage=usage_rows, dry_run=dry_run),
              open(os.path.join(cdir, "gen-%03d.receipt.json" % gen_no), "w"), indent=1)
    print(body)
    print("\nwrote", out_path, ("and " + diff_path) if diff_path else "", "spent $%.4f" % spent, file=sys.stderr)
    return out_path


def dossier(topic, as_json=False, hop=True, k_seed=40):
    """The skeleton of one topic: structure and pointers a new instrument reads first (v0.3 step 2, gear one only)."""
    F = Field()
    qv, _ = embed_all([topic], use_cache=False)
    qv = qv[0]
    sims = F.X @ qv
    lex = np.array([1 if re.search(r"\b" + re.escape(topic) + r"\b", c["text"], re.I) else 0 for c in F.chunks])
    seed = set(int(i) for i in np.argsort(-sims)[:k_seed] if sims[i] > 0.5) | set(int(i) for i in np.nonzero(lex)[0])
    members = set(seed)
    if hop:
        for i in list(seed):
            for nb, w, br in F.nbrs.get("c%d" % i, []):
                if nb.startswith("c") and w >= 0.65:
                    members.add(int(nb[1:]))
    # retellings collapse: drop members whose dup-partner is also a member (keep the earlier document)
    dup_pairs = [(int(l["a"][1:]), int(l["b"][1:])) for l in F.idx["links"] if l["l"] == "dup"]
    mult = {}
    for a, b in dup_pairs:
        if a in members and b in members:
            da, db = F.docs[F.chunks[a]["d"]], F.docs[F.chunks[b]["d"]]
            keep, drop = (a, b) if da["t"] <= db["t"] else (b, a)
            members.discard(drop)
            mult[keep] = mult.get(keep, 1) + 1
    by_doc = {}
    for i in members:
        by_doc.setdefault(F.chunks[i]["d"], []).append(i)
    timeline = []
    for d_i, cs in sorted(by_doc.items(), key=lambda kv: (F.docs[kv[0]]["t"], F.docs[kv[0]]["n"])):
        d = F.docs[d_i]
        timeline.append(dict(doc=d["n"], path=d["f"], date=d["t"], project=d["p"], community=F.comms[d["c"]]["label"],
                             chunks=["c%d" % i for i in sorted(cs)], sections=[F.chunks[i]["s"][:80] for i in sorted(cs)][:6],
                             share_of_doc=round(len(cs) / max(1, len(d["chunks"])), 2)))
    comm_counts = {}
    for i in members:
        cid = F.chunks[i]["c"]
        comm_counts[cid] = comm_counts.get(cid, 0) + 1
    bridges = []
    for l in F.idx["links"]:
        if l.get("br"):
            a, b = int(l["a"][1:]), int(l["b"][1:])
            if (a in members) != (b in members):
                inside, outside = (a, b) if a in members else (b, a)
                bridges.append(dict(inside="c%d" % inside, inside_doc=F.docs[F.chunks[inside]["d"]]["n"], outside="c%d" % outside,
                                    outside_doc=F.docs[F.chunks[outside]["d"]]["n"], outside_community=F.comms[F.chunks[outside]["c"]]["label"], w=l["w"]))
    bridges.sort(key=lambda b: -b["w"])
    degree = {}
    for l in F.idx["links"]:
        if l["l"] in ("sem", "doc"):
            for key in (l["a"], l["b"]):
                degree[key] = degree.get(key, 0) + 1
    dark = ["c%d" % i for i in sorted(members) if degree.get("c%d" % i, 0) == 0]
    eras = []
    if timeline:
        months = {}
        for row in timeline:
            months.setdefault(row["date"][:7], 0)
            months[row["date"][:7]] += len(row["chunks"])
        eras = [dict(month=m, chunks=n) for m, n in sorted(months.items())]
    tokens_in_topic = sum(F.chunks[i]["tk"] for i in members)
    skel = dict(topic=topic, kind="dossier_skeleton", version=VERSION,
                census=dict(chunks=len(members), documents=len(by_doc), tokens=tokens_in_topic, retellings_collapsed=sum(v - 1 for v in mult.values()),
                            date_min=timeline[0]["date"] if timeline else None, date_max=timeline[-1]["date"] if timeline else None),
                communities=[dict(id=cid, label=F.comms[cid]["label"], chunks=n) for cid, n in sorted(comm_counts.items(), key=lambda kv: -kv[1])],
                eras=eras, timeline=timeline, bridges_out=bridges[:20], dark_matter=dark[:40],
                read_plan_first=[F.span(i, 240) for i in sorted(members, key=lambda i: -float(sims[i]))[:8]],
                note="structure and pointers, not text: read the timeline oldest-first and newest-first, then request spans by chunk id (recall); "
                     "claims, supersession and the forgotten list arrive with cards (v0.3 R4)")
    if as_json:
        print(json.dumps(skel, ensure_ascii=False, indent=1))
    else:
        c = skel["census"]
        print("DOSSIER %s: %d chunks in %d documents (%dk tokens), %s -> %s, %d retellings collapsed" % (
            topic, c["chunks"], c["documents"], c["tokens"] // 1000, c["date_min"], c["date_max"], c["retellings_collapsed"]))
        print("communities:", "; ".join("%s (%d)" % (x["label"][:28], x["chunks"]) for x in skel["communities"][:6]))
        print("eras:", ", ".join("%s:%d" % (e["month"], e["chunks"]) for e in eras))
        for row in timeline[:12]:
            print("  %s  %-58s %2d chunks  %s" % (row["date"], row["doc"][:58], len(row["chunks"]), row["community"][:24]))
        if len(timeline) > 12:
            print("  ... %d more documents" % (len(timeline) - 12))
        for b in bridges[:5]:
            print("  BRIDGE out: %s -> %s (%s, %.2f)" % (b["inside_doc"][:34], b["outside_doc"][:34], b["outside_community"][:22], b["w"]))
        print("  dark matter (never related to anything): %d chunks" % len(dark))
    return skel


def what_changed():
    cdir = os.path.join(STORE, "codex")
    diffs = sorted(glob.glob(os.path.join(cdir, "diff-*.md")))
    if not diffs:
        gens = sorted(glob.glob(os.path.join(cdir, "gen-*.md")))
        return "no diff yet (%d generation(s)); run: connectome codex" % len(gens)
    return open(diffs[-1], encoding="utf-8").read()


def unit_map():
    cdir = os.path.join(STORE, "codex")
    gens = [g for g in sorted(glob.glob(os.path.join(cdir, "gen-*.md"))) if "-dry" not in g]
    if not gens:
        return "no unit map yet; run: connectome codex"
    return open(gens[-1], encoding="utf-8").read()


# ----------------------------------------------------------------------------- surfaces

def about():
    meta = {}
    p = os.path.join(STORE, "index.json")
    if os.path.exists(p):
        meta = json.load(open(p, encoding="utf-8"))["meta"]
    print(json.dumps(dict(organ="connectome", version=VERSION, path=os.path.abspath(__file__),
                          family="everything/facet · everywhere · everywhen · chunker · scriptorium · connectome",
                          purpose="the field over the estate: chunks placed by meaning, related in slices, folded into communities and a unit map; "
                                  "recall returns a read plan (spans), place returns a residual verdict, codex returns what the map believes and what changed",
                          verbs=[dict(verb="connectome build [--transcripts N]", what="fold the corpus into store/ (local embeddings, cached)"),
                                 dict(verb="connectome ask Q [--json]", what="read plan: BM25 || vector || 1-hop firing -> RRF -> spans"),
                                 dict(verb="connectome place FILE [--json]", what="residual gate: residual, nearest, bridges, priority = r / lane volatility"),
                                 dict(verb="connectome codex [--dry-run] [--cap USD]", what="gear two: the unit map per community + diff vs last generation"),
                                 dict(verb="connectome render", what="store/scene.json -> scene.html"),
                                 dict(verb="connectome mcp", what="MCP stdio: recall, place, what_changed, unit_map"),
                                 dict(verb="connectome providers", what="the gear-two lanes")],
                          store=meta, health=dict(store_present=bool(meta), embed_url=EMBED_URL,
                                                  deepseek_key=bool(os.environ.get("DEEPSEEK_API_KEY"))),
                          docs=["C:/NEW/CONNECTOME_THE-SECOND-BRAIN-RENDERED_DESIGN_CALIBRAN_2026-09-01.md",
                                "C:/NEW/CONNECTOME_THE-SLIDE-RULE-CONNECTOME_DESIGN-v0.2_CALIBRAN_2026-09-01.md"]), indent=1))


def render():
    sys.path.insert(0, PROTO)
    src = os.path.join(STORE, "scene.json")
    dst = os.path.join(HERE, "scene.html")
    data = open(src, encoding="utf-8").read().replace("</", "<\\/")
    tpl = open(os.path.join(PROTO, "template.html"), encoding="utf-8").read()
    assert tpl.count("/*__SCENE_JSON__*/") == 1
    open(dst, "w", encoding="utf-8").write(tpl.replace("/*__SCENE_JSON__*/", data))
    print("wrote", dst, "%.2f MB" % (os.path.getsize(dst) / 1e6))


def mcp_serve():
    from mcp.server.fastmcp import FastMCP
    srv = FastMCP("connectome")

    @srv.tool(structured_output=False)
    def recall(query: str, k: int = 8) -> dict:
        """A read plan over the estate: spans (path, section, text) ranked by BM25, vector similarity and one hop of graph firing. Never an answer; cite the spans."""
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            return ask(query, k=k, as_json=True)

    @srv.tool(structured_output=False)
    def place_file(path: str) -> dict:
        """The residual gate: how badly a document fits the field (residual per chunk, nearest communities, bridges, priority = residual / lane volatility). Proposes only."""
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            return place(path, as_json=True)

    @srv.tool(structured_output=False)
    def dossier_tool(topic: str) -> dict:
        """The skeleton of one topic (structure and pointers, not text): documents in time, communities, eras, retellings collapsed, bridges out, dark matter, and a first read plan. Read this before requesting spans with recall."""
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            return dossier(topic, as_json=True)

    @srv.tool(structured_output=False)
    def what_changed_tool() -> str:
        """The diff between the last two unit-map generations: what changed in the map's understanding."""
        return what_changed()

    @srv.tool(structured_output=False)
    def unit_map_tool() -> str:
        """The current unit map: what each community of the estate believes, with chunk citations."""
        return unit_map()

    srv.run()


def main():
    # Windows consoles default to cp1252; the estate's documents are UTF-8 (the chunker's own fix)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(prog="connectome")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("about")
    b = sub.add_parser("build")
    b.add_argument("--transcripts", type=int, default=0)
    a = sub.add_parser("ask")
    a.add_argument("query")
    a.add_argument("--k", type=int, default=8)
    a.add_argument("--json", action="store_true")
    p = sub.add_parser("place")
    p.add_argument("file")
    p.add_argument("--json", action="store_true")
    p.add_argument("--lane", default=None)
    c = sub.add_parser("codex")
    c.add_argument("--provider", default="deepseek")
    c.add_argument("--cap", type=float, default=0.25)
    c.add_argument("--dry-run", action="store_true")
    d = sub.add_parser("dossier")
    d.add_argument("--topic", required=True)
    d.add_argument("--json", action="store_true")
    sub.add_parser("render")
    sub.add_parser("mcp")
    sub.add_parser("providers")
    sub.add_parser("--about")
    args = ap.parse_args()
    if args.cmd == "dossier":
        dossier(args.topic, as_json=args.json)
        return
    if args.cmd in ("about", "--about"):
        about()
    elif args.cmd == "build":
        build(args.transcripts)
    elif args.cmd == "ask":
        ask(args.query, k=args.k, as_json=args.json)
    elif args.cmd == "place":
        place(args.file, as_json=args.json, lane=args.lane)
    elif args.cmd == "codex":
        codex(args.provider, args.cap, args.dry_run)
    elif args.cmd == "render":
        render()
    elif args.cmd == "mcp":
        mcp_serve()
    elif args.cmd == "providers":
        print(json.dumps(PROVIDERS, indent=1))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
