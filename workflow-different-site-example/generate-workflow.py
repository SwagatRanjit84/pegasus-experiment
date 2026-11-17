
import os
import platform
from Pegasus.api import *

# ==========================================
# 1. Initialize workflow
# ==========================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

wf = Workflow("three-step-pipeline")

# ==========================================
# 2. Define workflow files
# ==========================================

file_in = File("input_data.txt")
file_mid1 = File("stage1_output.txt")
file_mid2 = File("stage2_output.txt")
file_out = File("final_output.txt")

# ==========================================
# 3. Replica Catalog
# ==========================================

rc = ReplicaCatalog()

rc.add_replica(
    site="local",
    lfn=file_in,
    pfn=os.path.join(BASE_DIR, "input_data.txt")
)

rc.write("replicas.yml")

# ==========================================
# 4. Transformation Catalog
# ==========================================

tc = TransformationCatalog()

# Local processor: Mac
tc.add_transformations(
    Transformation(
        "data_processor_local",
        site="local",
        pfn=os.path.join(BASE_DIR, "processor.py"),
        is_stageable=False,
        arch=(
            Arch.AARCH64
            if platform.machine() in ("arm64", "aarch64")
            else Arch.X86_64
        ),
        os_type=OS.MACOSX
    )
)

# Remote processor: SLURM cluster
tc.add_transformations(
    Transformation(
        "data_processor_cluster",
        site="cluster",
        pfn="/home/YOUR_USERNAME/three-step-pipeline/processor.py",
        is_stageable=False,
        arch=Arch.X86_64,
        os_type=OS.LINUX
    )
)

tc.write("transformations.yml")

# ==========================================
# 5. Define Job 1: LOCAL
# ==========================================

job1 = Job("data_processor_local")

job1.add_args(
    "Stage-A",
    file_in,
    file_mid1
)

job1.add_inputs(file_in)
job1.add_outputs(file_mid1)

# ==========================================
# 6. Define Job 2: SLURM CLUSTER
# ==========================================

job2 = Job("data_processor_cluster")

job2.add_args(
    "Stage-B",
    file_mid1,
    file_mid2
)

job2.add_inputs(file_mid1)
job2.add_outputs(file_mid2)

# Request 8 CPUs and 2-hour runtime on the cluster
job2.add_profiles(
    Namespace.PEGASUS,
    key="runtime",
    value=7200
)

# ==========================================
# 7. Define Job 3: LOCAL
# ==========================================

job3 = Job("data_processor_local")

job3.add_args(
    "Stage-C",
    file_mid2,
    file_out
)

job3.add_inputs(file_mid2)
job3.add_outputs(file_out)

# ==========================================
# 8. Add jobs to workflow
# ==========================================

wf.add_jobs(job1, job2, job3)

# ==========================================
# 9. Register catalogs
# ==========================================

wf.add_replica_catalog(rc)
wf.add_transformation_catalog(tc)

# ==========================================
# 10. Write workflow
# ==========================================

wf.write("workflow.yml")

print("======================================")
print("PEGASUS WORKFLOW GENERATED")
print("======================================")
print("Job 1: Mac local")
print("Job 2: SLURM cluster")
print("Job 3: Mac local")
print("======================================")
