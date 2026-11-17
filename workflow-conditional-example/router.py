#!/usr/bin/env python3
import sys

def route_data(input_path, high_out, low_out, threshold=30.0):
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    total_sum = 0.0
    for line in lines:
        total_sum += sum(float(x) for x in line.split(","))

    print(f"[Router] Computed total sum = {total_sum} (Threshold = {threshold})")

    if total_sum > threshold:
        print("[Router] Condition TRUE (sum > threshold) -> Activating HIGH branch, skipping LOW branch.")
        with open(high_out, "w") as f:
            f.write("\n".join(lines) + "\n")
        with open(low_out, "w") as f:
            f.write("SKIP\n")
    else:
        print("[Router] Condition FALSE (sum <= threshold) -> Activating LOW branch, skipping HIGH branch.")
        with open(high_out, "w") as f:
            f.write("SKIP\n")
        with open(low_out, "w") as f:
            f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    route_data(sys.argv[1], sys.argv[2], sys.argv[3])
