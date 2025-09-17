from FaaSr_py.client.py_client_stubs import (
    faasr_delete_file,
    faasr_get_file,
    faasr_get_folder_list,
    faasr_get_s3_creds,
    faasr_log,
    faasr_put_file,
    faasr_rank,
)

from .utils import get_invocation_id
from .utils.enums import TestPyApi


def test_py_api(
    folder: str,
    input1: str,
    input2: str,
    input3: str,
    output1: str,
    output2: str,
) -> None:
    invocation_id = get_invocation_id()

    # Test deleting input1
    faasr_delete_file(f"{invocation_id}/{input1}")

    # Test getting input2
    faasr_get_file(
        local_file=input2,
        remote_file=f"{invocation_id}/{input2}",
        remote_folder=folder,
    )

    # Test getting input3
    faasr_get_file(
        local_file=input3,
        remote_file=f"{invocation_id}/{input3}",
        remote_folder=folder,
    )

    # Test listing folder
    print("Getting folder list", faasr_get_folder_list(folder))

    # Test getting s3 creds
    print("Getting s3 creds", faasr_get_s3_creds())

    # Test logging
    faasr_log("Test log")

    # Test putting output1
    with open(output1, "w") as f:
        f.write(TestPyApi.OUTPUT_1_CONTENT.value)
    faasr_put_file(local_file=output1, remote_file=output1, remote_folder=folder)

    # Test putting output2
    with open(output2, "w") as f:
        f.write(TestPyApi.OUTPUT_2_CONTENT.value)
    faasr_put_file(local_file=output2, remote_file=output2, remote_folder=folder)

    # Test rank
    print("Getting rank", faasr_rank())
