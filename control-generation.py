#!/usr/bin/env python3
import argparse, os, random, subprocess, sys
from pathlib import Path

def run_leiden(edge_path, leiden_py, out_file, model, seed = 0, resolution = None):
    cmd = [sys.executable, leiden_py, "-e", str(edge_path), "-o", str(out_file), "-m", model, "-s", str(seed)]
    if model == "cpm":
        cmd.append("-r")
        cmd.append(str(resolution))
    subprocess.run(cmd, check=True)

def run_dcsbm(edge_path: Path, sbm_py: Path, prefix: Path, out_file: Path, num_procs: int):
    cmd = [sys.executable, str(sbm_py), "--input-network", str(edge_path), "--inner-sbm-model", "DC-SBM", "--output-prefix", str(prefix), "--output-clustering", str(out_file), "--num-processors", str(num_procs)]
    subprocess.run(cmd, check=True)

def main():
    p = argparse.ArgumentParser(description="Generate a control clustering for one EC-SBM dataset.")
    p.add_argument("--dataset", required=True)
    p.add_argument("--base", required=True)
    p.add_argument("--method", required=True, choices=["leiden-mod", "leiden-cpm", "dcsbm-flat"])
    p.add_argument("--resolution", type=float, default=None, required=False)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--random-seed", action="store_true")
    p.add_argument("--num-processors", type=int, default=1)
    p.add_argument("--overwrite", action="store_true")
    args = p.parse_args()

    parent = Path('.').resolve()
    ec_root = parent / "EC-SBM-Networks"
    wcc_root = parent / "wcc-networks"

    edge_path = ec_root / args.base / args.dataset / "0" / "edge.tsv"
    
    if args.method == "leiden-mod":
        method_label = "leiden-mod"
    elif args.method == "leiden-cpm":
        method_label = f"leiden-cpm-{args.resolution:.15g}"
    else:
        method_label = "dcsbm-flat"

    method_dir = wcc_root / method_label
    dataset_dir = method_dir / args.dataset
    dataset_dir.mkdir(parents=True, exist_ok=True)

    out_file = dataset_dir / f"{args.dataset}_{args.base}_control.tsv"

    if out_file.exists() and not args.overwrite:
        print(f"Test already ran for {out_file}")
        return

    seed = args.seed
    if args.random_seed:
        seed = random.randint(0, 2**31 - 1)
    print(f"Seed: {seed}")

    if args.method == "leiden-mod":
        tmp = dataset_dir / f".{out_file.name}"
        run_leiden(edge_path, parent / "run-leiden.py", tmp, "mod", seed, None)
        os.replace(tmp, out_file)
    elif args.method == "leiden-cpm":
        tmp = dataset_dir / f".{out_file.name}"
        run_leiden(edge_path, parent / args.leiden_script, tmp, "cpm", seed, args.resolution)
        os.replace(tmp, out_file)
    else:
        # dcsbm-flat
        sbm_script = str(Path("outside_repos") / "network-analysis-code" / "run_sbm" / "run_flat_sbm.py")
        run_dcsbm(edge_path, parent / sbm_script, dataset_dir / f"{args.dataset}_{args.base}", out_file, args.num_processors)

if __name__ == "__main__":
    main()
