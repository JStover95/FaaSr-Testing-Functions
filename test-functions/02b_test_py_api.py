from FaaSr_py.client.py_client_stubs import (
    faasr_delete_file,
    faasr_get_file,
    faasr_invocation_id,
    faasr_log,
    faasr_put_file,
)

from .utils.enums import TestPyApi


def test_py_api(
    folder: str,
    input1: str,
    input2: str,
    input3: str,
    output1: str,
    output2: str,
) -> None:
    invocation_id = faasr_invocation_id()
    faasr_log(f"Using invocation ID: {invocation_id}")

    # Test deleting input1
    faasr_delete_file(remote_folder=folder, remote_file=f"{invocation_id}/{input1}")
    faasr_log(f"Deleted input1: {input1}")

    # Test getting input2
    remote_file = f"{invocation_id}/{input2}"
    faasr_get_file(
        local_file=input2,
        remote_file=remote_file,
        remote_folder=folder,
    )
    faasr_log(f"Saved remote file: {remote_file} to {input2}")

    # Test getting input3
    remote_file = f"{invocation_id}/{input3}"
    faasr_get_file(
        local_file=input3,
        remote_file=remote_file,
        remote_folder=folder,
    )
    faasr_log(f"Saved remote file: {remote_file} to {input3}")

    # Test putting output1
    with open(output1, "w") as f:
        f.write(TestPyApi.OUTPUT_1_CONTENT.value)
    remote_file = f"{invocation_id}/{output1}"
    faasr_put_file(local_file=output1, remote_file=remote_file, remote_folder=folder)
    faasr_log(
        f"Created output file: {remote_file} with content: {TestPyApi.OUTPUT_1_CONTENT.value}"
    )

    # Test putting output2
    with open(output2, "w") as f:
        f.write(TestPyApi.OUTPUT_2_CONTENT.value)
    remote_file = f"{invocation_id}/{output2}"
    faasr_put_file(local_file=output2, remote_file=remote_file, remote_folder=folder)
    faasr_log(
        f"Created output file: {remote_file} with content: {TestPyApi.OUTPUT_2_CONTENT.value}"
    )
