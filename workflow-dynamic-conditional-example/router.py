#!/usr/bin/env python3
import sys

def route_data(input_path, high_out, low_out, threshold=30.0):
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    total_sum = sum(
        sum(float(x) for x in line.split(","))
        for line in lines
    )

    print(f"[Router] Computed total sum = {total_sum} (Threshold = {threshold})")

    if total_sum > threshold:
        print("[Router] Condition TRUE -> Writing ONLY high_branch_input.txt (omitting low_branch_input.txt).")
        with open(high_out, "w") as f:
            f.write("\n".join(lines) + "\n")
    else:
        print("[Router] Condition FALSE -> Writing ONLY low_branch_input.txt (omitting high_branch_input.txt).")
        with open(low_out, "w") as f:
            f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    route_data(sys.argv[1], sys.argv[2], sys.argv[3])
