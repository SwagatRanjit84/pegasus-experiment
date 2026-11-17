#!/usr/bin/env python3
import sys

def run_branch(mode, input_path, output_path):
    with open(input_path, "r") as f:
        content = f.read().strip()

    if content == "SKIP":
        print(f"[{mode}] Received SKIP signal. Bypassing computation.")
        with open(output_path, "w") as f:
            f.write(f"{mode}: SKIPPED\n")
        sys.exit(0)

    print(f"[{mode}] Active branch! Processing data...")
    lines = content.splitlines()
    results = []
    for line in lines:
        vals = [float(x) for x in line.split(",")]
        if mode == "HIGH":
            new_vals = [v * 10.0 for v in vals]
        else:
            new_vals = [v + 100.0 for v in vals]
        results.append(",".join(map(str, new_vals)))

    with open(output_path, "w") as f:
        f.write("\n".join(results) + "\n")

if __name__ == "__main__":
    run_branch(sys.argv[1], sys.argv[2], sys.argv[3])
