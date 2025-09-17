from FaaSr_py.client.py_client_stubs import faasr_put_file

from .utils import get_invocation_id
from .utils.enums import CreateInput


def create_input(
    folder: str,
    input1: str,
    input2: str,
    input3: str,
) -> None:
    invocation_id = get_invocation_id()

    # Create input1
    with open(input1, "w") as f:
        f.write(CreateInput.INPUT_1_CONTENT.value)

    # Create input2
    with open(input2, "w") as f:
        f.write(CreateInput.INPUT_2_CONTENT.value)

    # Create input3
    with open(input3, "w") as f:
        f.write(CreateInput.INPUT_3_CONTENT.value)

    faasr_put_file(
        local_file=input1,
        remote_file=f"{invocation_id}/{input1}",
        remote_folder=folder,
    )
    faasr_put_file(
        local_file=input2,
        remote_file=f"{invocation_id}/{input2}",
        remote_folder=folder,
    )
    faasr_put_file(
        local_file=input3,
        remote_file=f"{invocation_id}/{input3}",
        remote_folder=folder,
    )
