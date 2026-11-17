
import os
import platform
from Pegasus.api import *

# ==========================================
# 1. USER CONFIGURATION
# ==========================================

HPC_USERNAME = "sranjit42"
HPC_LOGIN = "login.hpc.tntech.edu"

HPC_HOME = "/home/tntech.edu/sranjit42"
HPC_PARTITION = "hugemem"
HPC_SCRATCH = HPC_HOME + "/pegasus/scratch"
HPC_STORAGE = HPC_HOME + "/pegasus/storage"
HPC_QOS = "normal"

HPC_ACCOUNT = "csc6740-001-2026f"


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ==========================================
# 2. INITIALIZE SITE CATALOG
# ==========================================

sc = SiteCatalog()

# ==========================================
# 3. LOCAL SITE: MAC
# ==========================================

local_arch = (
    Arch.AARCH64
    if platform.machine() in ("arm64", "aarch64")
    else Arch.X86_64
)

local_scratch = os.path.join(BASE_DIR, "scratch")
local_storage = os.path.join(BASE_DIR, "storage")

os.makedirs(local_scratch, exist_ok=True)
os.makedirs(local_storage, exist_ok=True)

local = Site(
    "local",
    arch=local_arch,
    os_type=OS.MACOSX
)

local.add_directories(
    Directory(
        Directory.SHARED_SCRATCH,
        local_scratch,
        shared_file_system=True
    ).add_file_servers(
        FileServer(
            "file://" + local_scratch,
            Operation.ALL
        )
    ),

    Directory(
        Directory.LOCAL_STORAGE,
        local_storage,
        shared_file_system=True
    ).add_file_servers(
        FileServer(
            "file://" + local_storage,
            Operation.ALL
        )
    )
)

# ==========================================
# 4. REMOTE SITE: SLURM CLUSTER
# ==========================================

cluster = Site(
    "cluster",
    arch=Arch.X86_64,
    os_type=OS.LINUX
)

# Scratch and storage must exist on HPC.
# Create them before running the workflow.

cluster.add_directories(
    Directory(
        Directory.SHARED_SCRATCH,
        HPC_SCRATCH,
        shared_file_system=True
    ).add_file_servers(
        FileServer(
            f"scp://{HPC_USERNAME}@{HPC_LOGIN}{HPC_SCRATCH}",
            Operation.ALL
        )
    ),

    Directory(
        Directory.LOCAL_STORAGE,
        HPC_STORAGE,
        shared_file_system=True
    ).add_file_servers(
        FileServer(
            f"scp://{HPC_USERNAME}@{HPC_LOGIN}{HPC_STORAGE}",
            Operation.ALL
        )
    )
)

# ==========================================
# 5. SLURM EXECUTION CONFIGURATION
# ==========================================

cluster.add_pegasus_profile(
    style="glite",
    queue=HPC_PARTITION,
    project=HPC_ACCOUNT,
    nodes="1",
    ppn="8",
    runtime="7200",
    data_configuration="sharedfs"
)

# ==========================================
# 6. ADD SITES
# ==========================================

sc.add_sites(local, cluster)

# ==========================================
# 7. WRITE SITE CATALOG
# ==========================================

sc.write("sites.yml")

print("========================================")
print("PEGASUS SITE CATALOG GENERATED")
print("========================================")
print("Local execution: Mac")
print("Remote execution: SLURM")
print("HPC account:", HPC_ACCOUNT)
print("HPC partition:", HPC_PARTITION)
print("HPC CPUs: 8")
print("HPC runtime: 7200 seconds")
print("========================================")
