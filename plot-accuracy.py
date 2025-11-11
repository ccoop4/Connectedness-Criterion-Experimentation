#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser(description="Plot accuracy bars from accuracy_stats/* for one dataset/base/control.")
    p.add_argument("--dataset", required=True)
    p.add_argument("--base", required=True)
    p.add_argument("--control-method", required=True)
    p.add_argument("--local", action="store_true")
    p.add_argument("--output", default=None)
    args = p.parse_args()

    root = Path(".").resolve()
    acc_dir = root / "accuracy_stats" / f"{args.dataset}_{args.base}_{args.control_method}"

    metrics = {
        "ARI": {},
        "AMI": {},
        "NMI": {},
        "Precision": {},
        "Recall": {},
    }
    suffixes = {
        "ARI": ".ari",
        "AMI": ".ami",
        "NMI": ".nmi",
        "Precision": ".precision",
        "Recall": ".recall",
    }

    for metric, ext in suffixes.items():
        for fp in acc_dir.glob(f"*{ext}"):
            crit = fp.name[:-len(ext)]
            try:
                val = float(fp.read_text().strip())
                metrics[metric][crit] = val
            except Exception:
                continue

    common = set(metrics["ARI"]) & set(metrics["AMI"]) & set(metrics["NMI"]) & set(metrics["Precision"]) & set(metrics["Recall"])

    if args.local:
        crits = [c for c in common if c.endswith("_local")]
        display = [c[:-6] for c in crits]
    else:
        crits = [c for c in common if not c.endswith("_local")]
        display = crits

    crits = sorted(crits, key=lambda c: (c != "control", c))
    if args.local:
        display = [c[:-6] for c in crits]
    else:
        display = crits

    data = {
        "ARI":       [metrics["ARI"][c] for c in crits],
        "AMI":       [metrics["AMI"][c] for c in crits],
        "NMI":       [metrics["NMI"][c] for c in crits],
        "Precision": [metrics["Precision"][c] for c in crits],
        "Recall":    [metrics["Recall"][c] for c in crits],
    }

    if args.output:
        out_path = Path(args.output).resolve()
    else:
        out_path = root / "plots" / f"{args.dataset}_{args.base}_{args.control_method}"
        if args.local:
            out_path = out_path.with_name(out_path.name + "_local")
        out_path = out_path.with_suffix(".png")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(5, 1, figsize=(10, 12), sharex=True)
    x = range(len(crits))

    def draw(ax, vals, label):
        bars = ax.bar(x, vals, color='lightblue', edgecolor="black")
        ax.set_ylabel(label)
        ax.set_ylim(0, 1)
        for rect, val in zip(bars, vals):
            ax.text(rect.get_x() + rect.get_width()/2, val, f"{val:.3f}",
                    ha="center", va="bottom", fontsize=7)
        ax.grid(axis="y", linestyle="--", alpha=0.3)

    draw(axes[0], data["ARI"], "ARI")
    draw(axes[1], data["AMI"], "AMI")
    draw(axes[2], data["NMI"], "NMI")
    draw(axes[3], data["Precision"], "Precision")
    draw(axes[4], data["Recall"], "Recall")

    axes[4].set_xticks(list(x))
    axes[4].set_xticklabels(display, rotation=30, ha="right")

    mode = "local" if args.local else "global"
    fig.suptitle(f"{args.dataset} | base={args.base} | control={args.control_method} | {mode}", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    fig.savefig(out_path, dpi=200)
    print(f"Figure saved at {out_path}")

if __name__ == "__main__":
    main()