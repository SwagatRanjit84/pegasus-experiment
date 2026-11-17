import os
from Pegasus.api import *

wf = Workflow("conditional-branch-pipeline")

# Ensure input_data.txt exists (sum = 45.0)
with open("input_data.txt", "w") as f:
    f.write("1.0,2.0,3.0\n4.0,5.0,6.0\n7.0,8.0,9.0\n")

file_in       = File("input_data.txt")
high_in       = File("high_branch_input.txt")
low_in        = File("low_branch_input.txt")
high_result   = File("high_branch_output.txt")
low_result    = File("low_branch_output.txt")

rc = ReplicaCatalog().add_replica(
    site="local",
    lfn=file_in,
    pfn=os.path.abspath("input_data.txt")
)
rc.write("replicas.yml")

tc = TransformationCatalog().add_transformations(
    Transformation(
        "router_task",
        site="local",
        pfn=os.path.abspath("router.py"),
        is_stageable=True,
        arch=Arch.AARCH64,
        os_type=OS.LINUX
    ),
    Transformation(
        "branch_task",
        site="local",
        pfn=os.path.abspath("branch_worker.py"),
        is_stageable=True,
        arch=Arch.AARCH64,
        os_type=OS.LINUX
    )
)
tc.write("transformations.yml")

# Job 1: Router evaluates condition and routes data
job_router = Job("router_task") \
    .add_args(file_in, high_in, low_in) \
    .add_inputs(file_in) \
    .add_outputs(high_in, low_in)

# Job 2: High branch (runs in parallel with Job 3, executes only if not SKIP)
job_high = Job("branch_task") \
    .add_args("HIGH", high_in, high_result) \
    .add_inputs(high_in) \
    .add_outputs(high_result)

# Job 3: Low branch (executes only if not SKIP)
job_low = Job("branch_task") \
    .add_args("LOW", low_in, low_result) \
    .add_inputs(low_in) \
    .add_outputs(low_result)

wf.add_jobs(job_router, job_high, job_low)
wf.write("conditional_workflow.yml")
print("Conditional workflow generated.")
