import os
from Pegasus.api import *

# 1. Initialize workflow
wf = Workflow("three-step-pipeline")

# 2. Define data files flowing through the 3-job pipeline
file_in   = File("input_data.txt")
file_mid1 = File("stage1_output.txt")
file_mid2 = File("stage2_output.txt")
file_out  = File("final_output.txt")

# 3. Register input file in Replica Catalog
rc = ReplicaCatalog().add_replica(
    site="local",
    lfn=file_in,
    pfn=os.path.abspath("input_data.txt")
)
rc.write("replicas.yml")

# 4. Define Transformation Catalog pointing directly to processor.py
script_path = os.path.abspath("processor.py")
tc = TransformationCatalog().add_transformations(
    Transformation(
        "data_processor",
        site="local",
        pfn=script_path,
        is_stageable=False,
        arch=Arch.AARCH64,
        os_type=OS.LINUX
    )
)
tc.write("transformations.yml")

# 5. Define 3 sequential Jobs passing stage name, input, and output
job1 = Job("data_processor") \
    .add_args("Stage-A", file_in, file_mid1) \
    .add_inputs(file_in) \
    .add_outputs(file_mid1)

job2 = Job("data_processor") \
    .add_args("Stage-B", file_mid1, file_mid2) \
    .add_inputs(file_mid1) \
    .add_outputs(file_mid2)

job3 = Job("data_processor") \
    .add_args("Stage-C", file_mid2, file_out) \
    .add_inputs(file_mid2) \
    .add_outputs(file_out)

# 6. Add jobs to workflow
wf.add_jobs(job1, job2, job3)

# Write out abstract workflow YAML
wf.write("workflow.yml")
print("Workflow generator updated successfully.")
