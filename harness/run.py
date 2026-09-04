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
    args = p.parse_args(argv)
    return {"converge": cmd_converge, "fronts": cmd_fronts, "report": cmd_report}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
