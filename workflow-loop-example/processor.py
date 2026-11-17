#!/usr/bin/env python3
import sys
import os

def process_data(input_path, output_path, stage_name):
    print(f"[{stage_name}] Reading input from {input_path}")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} not found!")
        
    with open(input_path, "r") as f:
        lines = f.readlines()
        
    processed_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        vals = [float(x) for x in line.split(",")]
        # Fixed syntax error: multiplied values correctly
        new_vals = [v * 2.0 for v in vals]
        processed_lines.append(",".join(map(str, new_vals)))
        
    print(f"[{stage_name}] Writing output to {output_path}")
    with open(output_path, "w") as f:
        f.write("\n".join(processed_lines) + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: processor.py <stage_name> <input_file> <output_file>")
        sys.exit(1)
    
    stage = sys.argv[1]
    infile = sys.argv[2]
    outfile = sys.argv[3]
    process_data(infile, outfile, stage)