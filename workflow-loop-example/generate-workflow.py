
import os
from Pegasus.api import *

# 1. Initialize the workflow
wf = Workflow("cyclic-loop-workflow")

# 2. Define files
file_in = File("input_data.txt")
file_a  = File("stage_a_out.txt")
file_b  = File("stage_b_out.txt")
file_c  = File("stage_c_out.txt")
file_d  = File("stage_d_out.txt")

# 3. Define Replica Catalog
rc = ReplicaCatalog().add_replica(
    site="local",
    lfn=file_in,
    pfn=os.path.abspath("input_data.txt")
)
rc.write("replicas.yml")

# 4. Define Transformation Catalog
script_path = os.path.abspath("processor.py")
tc = TransformationCatalog().add_transformations(
    Transformation(
        "data_processor",
        site="local",
        pfn=script_path,
        is_stageable=True,
        arch=Arch.AARCH64,
        os_type=OS.LINUX
    )
)
tc.write("transformations.yml")

# 5. Create Jobs for A -> (B || C) -> D topology
job_a = Job("data_processor") \
    .add_args("Stage-A", file_in, file_a) \
    .add_inputs(file_in) \
    .add_outputs(file_a)

job_b = Job("data_processor") \
    .add_args("Stage-B", file_a, file_b) \
    .add_inputs(file_a) \
    .add_outputs(file_b)

job_c = Job("data_processor") \
    .add_args("Stage-C", file_a, file_c) \
    .add_inputs(file_a) \
    .add_outputs(file_c)

job_d = Job("data_processor") \
    .add_args("Stage-D", file_b, file_d) \
    .add_inputs(file_b, file_c) \
    .add_outputs(file_d)

# 6. Add jobs to workflow and write abstract YAML
wf.add_jobs(job_a, job_b, job_c, job_d)
wf.write("workflow.yml")

print("Workflow and Catalogs generated successfully.")

