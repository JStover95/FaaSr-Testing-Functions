from FaaSr_py.client.py_client_stubs import (
    faasr_log,
    faasr_put_file,
    faasr_rank
)

from .utils import get_invocation_id
from .utils.enums import TestRank

def test_rank(folder: str,
              rank_folder: str
              )-> None:
    invocation_id = get_invocation_id()
    faasr_log(f"Using invocation ID: {invocation_id}")
    
    rank_list = faasr_rank()
    rank_number = rank_list.get("rank")
    rank_max = rank_list.get("max_rank")
    
    faasr_log(f"Currently on {rank_number} out of {rank_max}.")
    
    filename = f"rank{rank_number}.txt"
    with open(filename, 'w') as f:
        f.write(f"{TestRank}{rank_number}")
        
    remote_file = f"{invocation_id}/{rank_folder}/{filename}"
    faasr_put_file(local_file=filename, remote_file=remote_file, remote_folder=folder)
    faasr_log(
        f"Created file: {remote_file} with content: {TestRank}{rank_number}"
    )
    