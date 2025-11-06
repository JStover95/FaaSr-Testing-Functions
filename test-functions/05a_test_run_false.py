# Note: This will be run if 04a_test_run_true runs successfully and return False
# Create a run_false_output.txt
# Save it into s3 bucket using faasr_put_file
# Arguments: folder, output

from FaaSr_py.client.py_client_stubs import (
    faasr_invocation_id,
    faasr_log,
    faasr_put_file,
)

from .utils.enums import TestConditional


def test_run_false(folder: str, output: str) -> None:
    invocation_id = faasr_invocation_id()
    faasr_log(f"Using invocation ID: {invocation_id}")

    # Create run_false_output.txt
    with open(output, "w") as f:
        f.write(TestConditional.RUN_FALSE_CONTENT.value)

    remote_file = f"{invocation_id}/{output}"
    faasr_put_file(local_file=output, remote_file=remote_file, remote_folder=folder)
    faasr_log(
        f"Created output file: {remote_file} with content: {TestConditional.RUN_FALSE_CONTENT.value}"
    )
