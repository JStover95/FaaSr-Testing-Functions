# Note: This will be run if 03_sync1 runs successfully and return True
# Create a run_true_output.txt
# Save it into s3 bucket using faasr_put_file
# Arguments: folder, output
# Return False -> invoke 05a_test_run_false.py

from FaaSr_py.client.py_client_stubs import (
    faasr_invocation_id,
    faasr_log,
    faasr_put_file,
)

from .utils.enums import TestConditional


def test_run_true(folder: str, output: str) -> None:
    invocation_id = faasr_invocation_id()
    faasr_log(f"Using invocation ID: {invocation_id}")

    try:
        # Create run_true_output.txt
        with open(output, "w") as f:
            f.write(TestConditional.RUN_TRUE_CONTENT.value)
        remote_file = f"{invocation_id}/{output}"
        faasr_put_file(local_file=output, remote_file=remote_file, remote_folder=folder)
        faasr_log(
            f"Created output file: {remote_file} with content: {TestConditional.RUN_TRUE_CONTENT.value}"
        )

    except Exception as e:
        faasr_log(e)
        return True

    faasr_log("Returning False to invoke test_run_false.")
    return False
