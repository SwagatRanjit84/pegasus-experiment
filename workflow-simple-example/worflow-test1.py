from Pegasus.api import *

# 1. Initialize the workflow
wf = Workflow("hello-pegasus")

# 2. Define the transformation programmatically using correct API parameters
tc = TransformationCatalog().add_transformations(
    Transformation(
        "echo",
        site="local",
        pfn="/bin/echo",
        is_stageable=False,
        arch=Arch.AARCH64,
        os_type=OS.LINUX
    )
)
tc.write("transformations.yml")

# 3. Create the job referencing the transformation name
job = Job("echo").add_args("Hello from local HTCondor!")

# 4. Add the job to the workflow and write out the abstract workflow YAML
wf.add_jobs(job)
wf.write("workflow.yml")

print("Workflow and Transformation Catalogs generated successfully.")
