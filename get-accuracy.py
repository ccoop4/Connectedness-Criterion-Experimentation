#!/usr/bin/env python3
import argparse, sys, subprocess
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Get accuracy metrics for all WCC clusterings for one dataset.")
    p.add_argument("--dataset", required=True)
    p.add_argument("--base", required=True)
    p.add_argument("--control-method", required=True, choices=["leiden-mod", "leiden-cpm", "dcsbm-flat"])
    p.add_argument("--control-resolution", type=float, default=None)
    p.add_argument("--num-processors", type=int, default=1)
    p.add_argument("--local", action="store_true")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--accuracy-script", default="outside_repos/network_evaluation/commdet_acc/compute_cd_accuracy.py")
    args = p.parse_args()

    root = Path(".").resolve()
    ecsbm_root = root / "EC-SBM-Networks"
    wcc_root = root / "wcc-networks"
    acc_root = root / "accuracy_stats"

    if args.control_method == "leiden-mod":
        ctrl_label = "leiden-mod"
    elif args.control_method == "leiden-cpm":
        ctrl_label = f"leiden-cpm-{args.control_resolution:.15g}"
    else:  # dcsbm-flat
        ctrl_label = "dcsbm-flat"

    edge_path = ecsbm_root / args.base / args.dataset / "0" / "edge.tsv"
    gt_path   = ecsbm_root / args.base / args.dataset / "0" / "com.tsv"

    cluster_dir = wcc_root / ctrl_label / args.dataset

    out_dir = acc_root / f"{args.dataset}_{args.base}_{ctrl_label}"
    out_dir.mkdir(parents=True, exist_ok=True)

    acc_script = root / args.accuracy_script

    count_ran = 0
    count_skipped = 0

    prefix = f"{args.dataset}_{args.base}_"

    for tsv in sorted(cluster_dir.glob("*.tsv")):
        name = tsv.name
        if not name.startswith(prefix):
            print(f"Already in folder: {name}")
            count_skipped += 1
            continue

        crit = name[len(prefix):-4]

        if args.local:
            out_prefix = out_dir / f"{crit}_local"
        else:
            out_prefix = out_dir / crit

        cmd = [sys.executable, str(acc_script), "--input-network", str(edge_path), "--gt-clustering", str(gt_path), "--est-clustering", str(tsv), "--output-prefix", str(out_prefix), "--num_processors", str(args.num_processors)]
        if args.local:
            cmd.append("--local")
        if args.overwrite:
            cmd.append("--overwrite")

        subprocess.run(cmd, check=True, cwd=str(root))
        count_ran += 1

    print(f"Ran {count_ran} criteria successfully, skipped {count_skipped}. Wrote results to out_dir={out_dir}")

if __name__ == "__main__":
    main()
