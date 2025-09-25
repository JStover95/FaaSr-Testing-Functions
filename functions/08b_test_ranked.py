import os.path

from FaaSr_py.client.py_client_stubs import faasr_log, faasr_put_file, faasr_rank
from utils import get_invocation_id


def test_ranked(folder: str) -> None:
    rank_info = faasr_rank()
    invocation_id = get_invocation_id()

    local_file = "test_ranked.txt"
    remote_file = os.path.join(invocation_id, local_file)

    with open(local_file, "w") as f:
        f.write(f"Rank: {rank_info.get('rank')}")
        f.write(f"Max rank: {rank_info.get('max_rank')}")

    faasr_put_file(
        local_file=local_file,
        remote_folder=folder,
        remote_file=remote_file,
    )

    faasr_log(f"Saved remote file: {os.path.join(folder, remote_file)}")
