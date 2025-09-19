from FaaSr_py.client.py_client_stubs import faasr_log, faasr_put_file

from utils import get_invocation_id
from utils.enums import CreateInput


def create_input(
    folder: str,
    input1: str,
    input2: str,
    input3: str,
) -> None:
    invocation_id = get_invocation_id()
    faasr_log(f"Using invocation ID: {invocation_id}")

    # Create input1
    with open(input1, "w") as f:
        f.write(CreateInput.INPUT_1_CONTENT.value)

    remote_file = f"{invocation_id}/{input1}"
    faasr_put_file(
        local_file=input1,
        remote_file=remote_file,
        remote_folder=folder,
    )
    faasr_log(
        f"Created input1: {remote_file} with content: {CreateInput.INPUT_1_CONTENT.value}"
    )

    # Create input2
    with open(input2, "w") as f:
        f.write(CreateInput.INPUT_2_CONTENT.value)

    remote_file = f"{invocation_id}/{input2}"
    faasr_put_file(
        local_file=input2,
        remote_file=remote_file,
        remote_folder=folder,
    )
    faasr_log(
        f"Created input2: {remote_file} with content: {CreateInput.INPUT_2_CONTENT.value}"
    )

    # Create input3
    with open(input3, "w") as f:
        f.write(CreateInput.INPUT_3_CONTENT.value)

    remote_file = f"{invocation_id}/{input3}"
    faasr_put_file(
        local_file=input3,
        remote_file=remote_file,
        remote_folder=folder,
    )
    faasr_log(
        f"Created input3: {remote_file} with content: {CreateInput.INPUT_3_CONTENT.value}"
    )
