"""Run the harness and print a receipt.

    python -m harness.run converge [--shuffles N]
    python -m harness.run fronts   [--window W] [--trailing T]
    python -m harness.run report

Every number printed here is computed from the corpus in arrival order with no label
and no human judgement anywhere in the path.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

import numpy as np

from .corpus import load_store
from .embed import server_model
from .fronts import detect
from .loss import converge, residual_curve
from . import partition as P
from . import stability as S
from . import provenance as PV


def _corpus(args):
    c = load_store(args.store)
    lo, hi = c.span()
    print(
        f"corpus: {len(c.documents)} documents, {c.n_chunks} chunks, dim {c.dim}, "
        f"{lo} to {hi}"
    )
    if getattr(c, "undated", 0):
        print(f"  ({c.undated} document(s) skipped: no date could be established)")
    return c


def cmd_converge(args) -> int:
    c = _corpus(args)
    r = converge(c, shuffles=args.shuffles, seed=args.seed)
    print(f"\nF-CONVERGE: arrival order vs {r.n_shuffles} shuffles at matched size\n")
    print("  decile   time   shuffled   advantage   retelling")
    for i, (t, s, a) in enumerate(zip(r.time_deciles, r.shuffled_deciles, r.advantage()), 1):
        print(f"    {i:2d}     {t[0]:.3f}    {s[0]:.3f}     {a:+6.1%}      {t[1]:.2f}")
    print(
        f"\n  head->tail ratio: time {r.ratio(r.time_deciles):.2f}, "
        f"shuffled {r.ratio(r.shuffled_deciles):.2f}"
    )
    print(
        "  reading: the field learns its corpus where the subject holds, and loses to an\n"
        "  arbitrary order where the author opened new subjects.  A corpus is a stream of\n"
        "  fronts, not a stationary distribution."
    )
    return 0


def cmd_fronts(args) -> int:
    c = _corpus(args)
    s = residual_curve(c)
    d = detect(s, window=args.window, trailing=args.trailing)
    print(f"\n{d.summary()}\n")
    for f in d.fronts:
        first = c.documents_by_id[f.documents[0]]
        when = dt.datetime.fromtimestamp(first.when).date()
        tail = "open" if f.closed_at is None else str(f.closed_at)
        print(
            f"  pos {f.opened_at:3d}->{tail:>4}  {f.length:3d} docs  peak z {f.peak_z:+.2f}  "
            f"{when}  {first.name[:44]}"
        )
        for did in f.documents[1:6]:
            print(f"        {c.documents_by_id[did].name[:60]}")
        if len(f.documents) > 6:
            print(f"        ... and {len(f.documents) - 6} more")
    return 0


def cmd_report(args) -> int:
    c = _corpus(args)
    model = server_model()
    print(f"embedding server: {model or 'down'}")
    s = residual_curve(c)
    res = np.asarray([x.residual for x in s])
    d = detect(s)
    r = converge(c, shuffles=args.shuffles, seed=args.seed)
    receipt = {
        "documents": len(c.documents),
        "chunks": c.n_chunks,
        "dim": c.dim,
        "embedding_server": model,
        "residual_quantiles": {q: round(float(np.quantile(res, q / 100)), 4) for q in (10, 50, 90)},
        "fronts": [
            {
                "opened_at": f.opened_at,
                "closed_at": f.closed_at,
                "length": f.length,
                "peak_z": round(f.peak_z, 3),
                "first": c.documents_by_id[f.documents[0]].name,
            }
            for f in d.fronts
        ],
        "advantage_by_decile": [round(a, 4) for a in r.advantage()],
    }
    print(json.dumps(receipt, indent=2))
    return 0


def cmd_partition(args) -> int:
    c = _corpus(args)
    part = P.build(c.vectors, n_seeds=args.seeds, seed=args.seed)
    print("")
    print(f"partition/v{part.version}: {part.centroids.shape[0]} communities")
    print(f"  modularity        {part.modularity:.3f}")
    print(f"  co-classification {part.co_classification:.3f} over {part.n_seeds} runs")
    print(f"  drift on its own corpus {P.drift(part, c.vectors):.3f}")
    print(f"  largest communities {np.sort(part.sizes)[::-1][:8].tolist()}")
    return 0


def cmd_stability(args) -> int:
    """F-LAYOUT-STABLE: does freezing beat re-clustering as the corpus grows?"""
    c = _corpus(args)
    mean, worst = S.seed_stability(c.vectors, seeds=3, n_seeds=args.seeds)
    print("")
    print(f"consensus partitioning across 3 base seeds: ARI mean {mean:.3f}, worst {worst:.3f}")
    print("")
    print("  growth   frozen ARI   re-fit ARI   frozen moved   re-fit moved   drift")
    for frac in (0.9, 0.8, 0.6):
        r = S.grow(c, base_fraction=frac, n_seeds=args.seeds, seed=args.seed)
        print(
            f"   {r.grown_fraction:4.0%}      {r.frozen_ari:.3f}        {r.refit_ari:.3f}"
            f"         {r.frozen_moved:5.1%}         {r.refit_moved:5.1%}      "
            f"{r.frozen_drift:.3f}"
        )
    print("")
    print("  reading: assignment to a frozen partition moves nothing, while re-clustering")
    print("  the grown corpus moves a fifth of it.  Drift is the price, and it is reported")
    print("  rather than hidden: it is what a version event fires on.")
    return 0


def cmd_provenance(args) -> int:
    """The slice that states causation rather than similarity, and costs nothing."""
    import json as _json

    c = _corpus(args)
    with open(f"{args.store}/index.json", encoding="utf-8") as fh:
        index = _json.load(fh)

    messages = index.get("transcripts") or []
    if not messages:
        print("no transcripts in this store; the provenance slice needs sessions")
        return 0

    edges = PV.link(
        [ch["text"] for ch in index["chunks"]],
        [m.get("text", "") for m in messages],
        [str(m.get("session", "?")) for m in messages],
    )
    linked = {int(c.doc_of_chunk[e.chunk]) for e in edges}
    print("")
    print(f"{len(edges)} provenance edges over {len(messages)} messages")
    print(f"{len(linked)} of {len(c.documents)} documents trace to a session")
    strongest = sorted(edges, key=lambda e: -e.shared)[:5]
    for e in strongest:
        doc = c.documents_by_id[int(c.doc_of_chunk[e.chunk])]
        print(f"  {e.shared:4d} shared 12-grams  {doc.name[:44]}  <- {e.session[:12]}")
    return 0


def main(argv: list[str] | None = None) -> int:
    # Common flags are attached to every subparser as well as the parent, so
    # `run converge --shuffles 3` and `run --shuffles 3 converge` both work.  A CLI
    # that accepts a flag in only one position is a trap for the next caller.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--store", default="store")
    common.add_argument("--shuffles", type=int, default=5)
    common.add_argument("--seed", type=int, default=0)

    p = argparse.ArgumentParser(prog="harness", parents=[common])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("converge", parents=[common])
    f = sub.add_parser("fronts", parents=[common])
    f.add_argument("--window", type=int, default=8)
    f.add_argument("--trailing", type=int, default=40)
    sub.add_parser("report", parents=[common])
    pp = sub.add_parser("partition", parents=[common])
    pp.add_argument("--seeds", type=int, default=10)
    st = sub.add_parser("stability", parents=[common])
    st.add_argument("--seeds", type=int, default=6)
    sub.add_parser("provenance", parents=[common])
    args = p.parse_args(argv)
    table = {
        "converge": cmd_converge,
        "fronts": cmd_fronts,
        "report": cmd_report,
        "partition": cmd_partition,
        "stability": cmd_stability,
        "provenance": cmd_provenance,
    }
    return table[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
