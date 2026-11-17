#!/usr/bin/env python3

import sys

stage = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

print("Executing:", stage)

with open(input_file, "r") as f:
    data = f.read()

result = f"{stage}: {data}"

with open(output_file, "w") as f:
    f.write(result)

print("Output generated:", output_file)