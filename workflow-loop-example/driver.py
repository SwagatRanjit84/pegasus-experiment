#!/usr/bin/env python3
import os
import subprocess
from workflow_generator import generate_iteration_workflow

def check_convergence(status_file):
    if not os.path.exists(status_file):
        return False
    with open(status_file, "r") as f:
        content = f.read().strip()
        # Returns True if convergence condition is met, False to loop again
        return "CONVERGED" in content

def main():
    iteration = 0
    max_iterations = 3
    converged = False
    
    current_input = "input_data.txt"

    while not converged and iteration < max_iterations:
        print(f"\n==============================")
        print(f" Starting Pegasus Iteration {iteration}")
        print(f"==============================")

        # 1. Generate the static DAG for this iteration
        wf_file, output_c = generate_iteration_workflow(iteration, current_input)

        # 2. Plan and submit the workflow via Pegasus
        subprocess.run([
            "pegasus-plan",
            "--conf", "pegasus.properties",
            "--dax", wf_file,
            "--site", "condorpool",
            "--output", "local",
            "--submit"
        ], check=True)

        # 3. Check status from Stage D output
        status_file = f"stage_d_out_iter_{iteration}.txt"
        
        # Feed output of Stage-C as the input for the next iteration cycle
        current_input = f"stage_c_out_iter_{iteration}.txt"
        
        converged = check_convergence(status_file)
        iteration += 1

    print("\nPegasus iterative workflow sequence completed.")

if __name__ == "__main__":
    main()