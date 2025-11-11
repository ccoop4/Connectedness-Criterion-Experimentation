#!/usr/bin/env python3
import argparse, subprocess, sys, os
from pathlib import Path

def run_wcc(wcc_bin, wcc_cwd, edgelist, control_tsv, out_tsv, log_file, crit, procs, log_level):
    cmd = [str(wcc_bin), "MincutOnly", "--edgelist", str(edgelist), "--existing-clustering", str(control_tsv), "--num-processors", str(procs), "--output-file", str(out_tsv), "--log-file", str(log_file), "--log-level", str(log_level), "--connectedness-criterion", crit]
    subprocess.run(cmd, check=True, cwd=str(wcc_cwd))

def main():
    p = argparse.ArgumentParser(description="Run WCC with specified criteria on a control clustering.")
    p.add_argument("--dataset", required=True)
    p.add_argument("--base", required=True)
    p.add_argument("--control-method", required=True, choices=["leiden-mod", "leiden-cpm", "dcsbm-flat"])
    p.add_argument("--control-resolution", type=float, default=None)
    p.add_argument("--criteria", nargs="+", required=True)
    p.add_argument("--num-processors", type=int, default=1)
    p.add_argument("--log-level", type=int, default=1)
    p.add_argument("--overwrite", action="store_true")
    args = p.parse_args()

    parent = Path('.').resolve()

    if args.control_method == "leiden-mod":
        ctrl_label = "leiden-mod"
    elif args.control_method == "leiden-cpm":
        ctrl_label = f"leiden-cpm-{args.control_resolution:.15g}"
    else:  # dcsbm-flat
        ctrl_label = "dcsbm-flat"

    ec_root = parent / "EC-SBM-Networks"
    wcc_root = parent / "wcc-networks"
    wcc_repo = parent / "outside_repos" / "constrained-clustering"
    wcc_bin = wcc_repo / "build" / "bin" / "constrained_clustering"

    edgelist = ec_root / args.base / args.dataset / "0" / "edge.tsv"
    control_tsv = wcc_root / ctrl_label / args.dataset / f"{args.dataset}_{args.base}_control.tsv"
    out_dir = wcc_root / ctrl_label / args.dataset
    out_dir.mkdir(parents=True, exist_ok=True)

    for crit in args.criteria:
        out_tsv = out_dir / f"{args.dataset}_{args.base}_{crit}.tsv"
        log_file = out_dir / f"{args.dataset}_{args.base}_{crit}.log"

        if out_tsv.exists() and not args.overwrite:
            print(f"Skipping {crit}")
            continue

        print(f"Running {crit} -> {out_tsv}")
        run_wcc(wcc_bin=wcc_bin, wcc_cwd=wcc_repo, edgelist=edgelist, control_tsv=control_tsv, out_tsv=out_tsv, log_file=log_file, crit=crit, procs=args.num_processors, log_level=args.log_level)
        print(f"Wrote {out_tsv}")

if __name__ == "__main__":
    main()
