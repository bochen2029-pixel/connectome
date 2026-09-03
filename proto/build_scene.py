#!/usr/bin/env python
"""
build_scene.py -- CONNECTOME R0: a first render of the estate's markdown corpus as a 3-D scene.

Pipeline (all local, nothing leaves the box):
  walk roots -> chunk (C:/chunker as a subprocess) -> embed (llama.cpp :8092, qwen3-embedding-0.6b, 1024-d)
  -> slices: semantic chunk-kNN (cross-doc) | semantic doc-kNN | lexical (TF-IDF doc-doc) | containment | succession
  -> Louvain communities on the doc graph -> UMAP-3 positions on chunk vectors (docs = mean of their chunks)
  -> bridges = high similarity x different community  ->  scene.json

R0 is static: no live lane, no residual gate, no sleep. Its only job is to be looked at.
"""
import glob
import json
import math
import os
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "scene.json")
CHUNK_DIR = os.path.join(HERE, "_chunks")
CHUNKER = "C:/chunker/chunker.py"
EMBED_URL = "http://127.0.0.1:8092/v1/embeddings"
BUDGET = int(os.environ.get("CX_BUDGET", "700"))
MAX_FILE_BYTES = 320_000
SNIPPET_CHARS = 700

ROOTS = [
    ("C:/NEW", "NEW"),
    ("C:/NEW/INTELLECT", "INTELLECT"),
    ("C:/NEW/eye-harness", "eye-harness"),
    ("C:/NEW/ANOMALY-LEDGER", "anomaly-ledger"),
    ("C:/Intercom/sandbox/CALIBRAN-4242/ROUNDTABLE-ISOMORPH", "roundtable"),
    ("C:/Intercom/sandbox", "meta-final"),
    ("C:/Cortex", "cortex"),
    ("C:/chunker", "one-pagers"),
    ("C:/hypercelld", "hypercelld"),
    ("C:/MEANDER", "meander"),
    ("C:/scriptorium", "scriptorium"),
    ("C:/Intercom", "intercom"),
    ("C:/hypercell_v5", "hypercell"),
    ("C:/ORRERY", "orrery"),
    ("C:/SURVEYOR", "surveyor"),
]
# stitched concatenations and redacted twins duplicate their sources byte-for-byte; a retelling is not a bridge
SKIP_NAME = re.compile(r"(REDACTION_LOG|_manifest|INDEX\.md$|^chunk-\d+\.md$|INTELLECT_FULL|_REDACTED|_lineage_)")
DUP_TH = 0.97   # cross-document chunk pairs at or above this cosine are retellings: kept as their own slice, never bridges


def log(*a):
    print(*a, flush=True)


def date_of(path):
    m = re.search(r"(20\d\d)-(\d\d)-(\d\d)", os.path.basename(path))
    if m:
        return "%s-%s-%s" % m.groups()
    return time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(path)))


def collect_files():
    seen = set()
    files = []
    for root, label in ROOTS:
        for f in sorted(glob.glob(root + "/*.md")):
            key = os.path.normcase(os.path.abspath(f))
            if key in seen:
                continue
            base = os.path.basename(f)
            if SKIP_NAME.search(base):
                continue
            sz = os.path.getsize(f)
            if sz < 800 or sz > MAX_FILE_BYTES:
                continue
            seen.add(key)
            files.append((f, label))
    return files


def chunk_file(path):
    """Run the chunker organ as a subprocess; return [(section, text)]."""
    out = os.path.join(CHUNK_DIR, re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.basename(path)) + ".chunks")
    if not os.path.isdir(out):
        # --overlap 0 hangs the chunker (infinite loop in its recap logic, found 2026-09-01); 40 is the smallest safe value.
        r = subprocess.run([sys.executable, CHUNKER, "--budget", str(BUDGET), "--overlap", "40", "--out", out, path],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            log("chunker failed on", path, r.stderr[-300:])
            return []
    chunks = []
    for cf in sorted(glob.glob(os.path.join(out, "chunk-*.md"))):
        raw = open(cf, encoding="utf-8", errors="replace").read()
        section = ""
        lines = raw.split("\n")
        body_start = 0
        in_recap = False
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


def embed_batch(texts):
    req = urllib.request.Request(EMBED_URL, data=json.dumps({"input": texts}).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
    rows = sorted(d["data"], key=lambda e: e["index"])
    return [e["embedding"] for e in rows]


CACHE_PATH = os.path.join(HERE, "_embed_cache.npz")


def _text_key(t):
    import hashlib
    return hashlib.blake2b(t.encode("utf-8"), digest_size=16).hexdigest()


def load_cache():
    if not os.path.exists(CACHE_PATH):
        return {}
    z = np.load(CACHE_PATH, allow_pickle=False)
    keys = [k for k in z["keys"]]
    return dict(zip(keys, z["vecs"]))


def save_cache(cache):
    if not cache:
        return
    keys = np.array(list(cache.keys()))
    vecs = np.array([cache[k] for k in keys], dtype=np.float32)
    tmp = CACHE_PATH + ".tmp.npz"
    np.savez(tmp, keys=keys, vecs=vecs)
    os.replace(tmp, CACHE_PATH)


def embed_all(texts, batch=4, workers=3):
    """Embed with an on-disk cache keyed by text hash, so a rerun never re-embeds."""
    cache = load_cache()
    keys = [_text_key(t) for t in texts]
    vecs = [cache.get(k) for k in keys]
    todo = [i for i, v in enumerate(vecs) if v is None]
    log("embedding: %d cached, %d to do" % (len(texts) - len(todo), len(todo)))
    idx = list(range(0, len(todo), batch))
    t0 = time.time()
    done = [0]
    lock = __import__("threading").Lock()

    def work(start):
        ids = todo[start:start + batch]
        chunk = [texts[i] for i in ids]
        try:
            out = embed_batch(chunk)
        except Exception:
            out = []
            for t in chunk:
                try:
                    out.append(embed_batch([t])[0])
                except Exception as ex:
                    log("embed failed (len %d): %s" % (len(t), repr(ex)[:120]))
                    out.append(None)
        with lock:
            for i, v in zip(ids, out):
                if v is not None:
                    vecs[i] = np.asarray(v, dtype=np.float32)
                    cache[keys[i]] = vecs[i]
            done[0] += len(chunk)
            if done[0] % 200 < batch:
                log("  embedded %d/%d (%.0fs)" % (done[0], len(todo), time.time() - t0))
                save_cache(cache)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(work, idx))
    save_cache(cache)
    return [None if v is None else (v.tolist() if hasattr(v, "tolist") else v) for v in vecs]


def tokens_of(text):
    try:
        import tiktoken
        enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return max(1, len(text) // 4)


def main():
    t0 = time.time()
    os.makedirs(CHUNK_DIR, exist_ok=True)
    files = collect_files()
    log("files:", len(files))
    # preflight: can the embedder take a chunk of BUDGET tokens?
    probe = "word " * (BUDGET + 60)
    try:
        embed_batch([probe])
        log("embedder accepts %d-token inputs" % (BUDGET + 60))
    except Exception as ex:
        log("embedder refused a %d-token input (%s); falling back to budget 400" % (BUDGET + 60, repr(ex)[:80]))
        globals()["BUDGET"] = 400

    docs = []
    chunks = []
    for path, label in files:
        cs = chunk_file(path)
        if not cs:
            continue
        di = len(docs)
        full = open(path, encoding="utf-8", errors="replace").read()
        title = os.path.basename(path)[:-3]
        docs.append(dict(i=di, k="d", n=title, p=label, f=path, t=date_of(path), tk=tokens_of(full), text=full, chunks=[]))
        for section, text in cs:
            ci = len(chunks)
            chunks.append(dict(i=ci, k="c", d=di, s=section[:160], text=text, tk=tokens_of(text), t=docs[di]["t"], p=label))
            docs[di]["chunks"].append(ci)
    log("docs: %d  chunks: %d  (%.0fs)" % (len(docs), len(chunks), time.time() - t0))

    # ---- embeddings ----
    vecs = embed_all([c["text"] for c in chunks])
    keep = [i for i, v in enumerate(vecs) if v is not None]
    if len(keep) < len(chunks):
        log("dropping %d unembedded chunks" % (len(chunks) - len(keep)))
    X = np.array([vecs[i] for i in keep], dtype=np.float32)
    X /= (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    chunks = [chunks[i] for i in keep]
    for new_i, c in enumerate(chunks):
        c["i"] = new_i
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
    log("embedded: %d chunks x %d dims (%.0fs)" % (X.shape[0], X.shape[1], time.time() - t0))

    D = np.zeros((len(docs), X.shape[1]), dtype=np.float32)
    for d in docs:
        D[d["i"]] = X[d["chunks"]].mean(axis=0)
    D /= (np.linalg.norm(D, axis=1, keepdims=True) + 1e-9)

    # ---- slices ----
    links = []
    chunk_doc = np.array([c["d"] for c in chunks])
    # semantic chunk kNN, cross-document only
    S = X @ X.T
    np.fill_diagonal(S, -1)
    same_doc = chunk_doc[:, None] == chunk_doc[None, :]
    S_cross = np.where(same_doc, -1, S)
    K_CHUNK, TH_CHUNK = 3, 0.60
    seen = set()
    dups = 0
    for i in range(len(chunks)):
        nn = np.argpartition(-S_cross[i], K_CHUNK)[:K_CHUNK]
        for j in nn:
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
    log("retellings (cos >= %.2f, cross-document): %d" % (DUP_TH, dups))
    # semantic doc kNN
    SD = D @ D.T
    np.fill_diagonal(SD, -1)
    K_DOC, TH_DOC = 4, 0.50
    dseen = set()
    doc_edges = {}
    for i in range(len(docs)):
        nn = np.argpartition(-SD[i], K_DOC)[:K_DOC]
        for j in nn:
            w = float(SD[i, j])
            if w < TH_DOC:
                continue
            key = (min(i, j), max(i, j))
            if key in dseen:
                continue
            dseen.add(key)
            links.append(dict(a="d%d" % key[0], b="d%d" % key[1], l="doc", w=round(w, 3)))
            doc_edges[key] = max(doc_edges.get(key, 0), w)
    # lexical: TF-IDF doc-doc
    from sklearn.feature_extraction.text import TfidfVectorizer
    tf = TfidfVectorizer(stop_words="english", max_df=0.85, min_df=2, ngram_range=(1, 2), sublinear_tf=True, max_features=60000)
    T = tf.fit_transform([d["text"] for d in docs])
    L = (T @ T.T).toarray()
    np.fill_diagonal(L, -1)
    K_LEX, TH_LEX = 3, 0.22
    lseen = set()
    for i in range(len(docs)):
        nn = np.argpartition(-L[i], K_LEX)[:K_LEX]
        for j in nn:
            w = float(L[i, j])
            if w < TH_LEX:
                continue
            key = (min(i, j), max(i, j))
            if key in lseen:
                continue
            lseen.add(key)
            links.append(dict(a="d%d" % key[0], b="d%d" % key[1], l="lex", w=round(w, 3)))
            doc_edges[key] = max(doc_edges.get(key, 0), 0.6 * w)
    # containment
    for c in chunks:
        links.append(dict(a="d%d" % c["d"], b="c%d" % c["i"], l="con", w=1.0))
    # succession: consecutive docs by date within a project
    by_proj = {}
    for d in docs:
        by_proj.setdefault(d["p"], []).append(d)
    for p, ds in by_proj.items():
        ds = sorted(ds, key=lambda d: (d["t"], d["n"]))
        for a, b in zip(ds, ds[1:]):
            links.append(dict(a="d%d" % a["i"], b="d%d" % b["i"], l="suc", w=0.5))

    # ---- communities (Louvain on the doc graph) ----
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(range(len(docs)))
    for (i, j), w in doc_edges.items():
        G.add_edge(i, j, weight=w)
    comms = nx.community.louvain_communities(G, weight="weight", seed=7, resolution=1.0)
    comms = sorted(comms, key=lambda s: -len(s))
    comm_of = {}
    for ci, members in enumerate(comms):
        for m in members:
            comm_of[m] = ci
    terms = np.array(tf.get_feature_names_out())
    comm_rows = []
    for ci, members in enumerate(comms):
        members = sorted(members)
        v = np.asarray(T[members].mean(axis=0)).ravel()
        top = terms[np.argsort(-v)[:4]]
        comm_rows.append(dict(id=ci, label=" · ".join(top), n=len(members),
                              docs=sum(docs[m]["tk"] for m in members)))
    for d in docs:
        d["c"] = comm_of[d["i"]]
    for c in chunks:
        c["c"] = docs[c["d"]]["c"]
    log("communities: %d  links: %d  (%.0fs)" % (len(comms), len(links), time.time() - t0))

    # ---- bridges: high similarity across communities, docs not already doc-neighbors ----
    BR_TH = 0.62
    cand = np.argwhere((S_cross >= BR_TH) & (S_cross < DUP_TH))
    bridges = []
    bseen = set()
    for i, j in cand:
        if i >= j:
            continue
        ci, cj = chunks[i]["c"], chunks[j]["c"]
        if ci == cj:
            continue
        di, dj = chunks[i]["d"], chunks[j]["d"]
        key = (min(i, j), max(i, j))
        if key in bseen:
            continue
        bseen.add(key)
        bridges.append((float(S_cross[i, j]), int(i), int(j)))
    bridges.sort(reverse=True)
    bridges = bridges[:160]
    bridge_keys = {(i, j) for _, i, j in bridges}
    existing = {(int(l["a"][1:]), int(l["b"][1:])) for l in links if l["l"] == "sem"}
    for w, i, j in bridges:
        if (i, j) in existing:
            for l in links:
                if l["l"] == "sem" and l["a"] == "c%d" % i and l["b"] == "c%d" % j:
                    l["br"] = 1
        else:
            links.append(dict(a="c%d" % i, b="c%d" % j, l="sem", w=round(w, 3), br=1))
    log("bridges: %d" % len(bridges))

    # ---- layout: UMAP-3 on chunk vectors ----
    import umap
    reducer = umap.UMAP(n_components=3, n_neighbors=15, min_dist=0.12, metric="cosine", random_state=42)
    Y = reducer.fit_transform(X)
    Y = Y - Y.mean(axis=0)
    Y = Y / (np.abs(Y).max() + 1e-9) * 300.0
    for c in chunks:
        c["x"], c["y"], c["z"] = [round(float(v), 1) for v in Y[c["i"]]]
    for d in docs:
        P = Y[d["chunks"]].mean(axis=0)
        d["x"], d["y"], d["z"] = [round(float(v), 1) for v in P]
    log("layout done (%.0fs)" % (time.time() - t0))

    # ---- export ----
    nodes = []
    for d in docs:
        nodes.append(dict(id="d%d" % d["i"], k="d", n=d["n"], p=d["p"], c=d["c"], t=d["t"], tk=d["tk"], f=d["f"],
                          x=d["x"], y=d["y"], z=d["z"], nc=len(d["chunks"])))
    for c in chunks:
        nodes.append(dict(id="c%d" % c["i"], k="c", d="d%d" % c["d"], n=docs[c["d"]]["n"], s=c["s"], p=c["p"], c=c["c"],
                          t=c["t"], tk=c["tk"], x=c["x"], y=c["y"], z=c["z"], sn=c["text"][:SNIPPET_CHARS]))
    slice_counts = {}
    for l in links:
        slice_counts[l["l"]] = slice_counts.get(l["l"], 0) + 1
    meta = dict(built=time.strftime("%Y-%m-%d %H:%M"), files=len(docs), chunks=len(chunks), links=len(links),
                slices=slice_counts, communities=len(comms), bridges=len(bridges),
                date_min=min(d["t"] for d in docs), date_max=max(d["t"] for d in docs),
                tokens=sum(d["tk"] for d in docs), embedder="qwen3-embedding-0.6b-q8_0 (llama.cpp :8092, 1024-d)",
                layout="UMAP-3 (cosine, n_neighbors=15, min_dist=0.12, seed 42) on chunk vectors; docs at the mean of their chunks",
                budget=BUDGET, thresholds=dict(sem=TH_CHUNK, doc=TH_DOC, lex=TH_LEX, bridge=BR_TH),
                elapsed_s=round(time.time() - t0))
    json.dump(dict(meta=meta, comms=comm_rows, nodes=nodes, links=links), open(OUT, "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    log("wrote", OUT, "%.1f MB" % (os.path.getsize(OUT) / 1e6))
    log(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
