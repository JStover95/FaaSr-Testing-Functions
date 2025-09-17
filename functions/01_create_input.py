from uuid import uuid4

from FaaSr_py.client.py_client_stubs import faasr_put_file

from functions.utils import get_invocation_id


def create_input(
    folder: str,
    input1: str,
    input2: str,
    input3: str,
) -> None:
    invocation_id = get_invocation_id()
    print("Invocation ID:", invocation_id)
    prefix = str(uuid4())

    # Create input1
    with open(input1, "w") as f:
        f.write("Test input1")

    # Create input2
    with open(input2, "w") as f:
        f.write("Test input2")

    # Create input3
    with open(input3, "w") as f:
        f.write("Test input3")

    faasr_put_file(
        local_file=input1,
        remote_file=f"{prefix}/{input1}",
        remote_folder=folder,
    )
    faasr_put_file(
        local_file=input2,
        remote_file=f"{prefix}/{input2}",
        remote_folder=folder,
    )
    faasr_put_file(
        local_file=input3,
        remote_file=f"{prefix}/{input3}",
        remote_folder=folder,
    )
