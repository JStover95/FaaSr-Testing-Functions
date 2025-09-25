# Note: This will be run if 04a_test_run_true runs successfully and return False
# Create a run_false_output.txt 
# Save it into s3 bucket using faasr_put_file
# Arguments: folder, output

from FaaSr_py.client.py_client_stubs import (
    faasr_log,
    faasr_put_file,
)

from .utils import get_invocation_id
from .utils.enums import TestConditional

def test_run_false(folder: str,
                  output: str
                  ) -> None:
    
    invocation_id = get_invocation_id()
    faasr_log(f"Using invocation ID: {invocation_id}")
    
    try:
        with open(output, "w") as f:
            f.write(TestConditional.RUN_FALSE_CONTENT.value)
        remote_file = f"{invocation_id}/{output}"
        faasr_put_file(local_file=output, remote_file=remote_file, remote_folder=folder)
        faasr_log(
            f"Created output file: {remote_file} with content: {TestConditional.RUN_FALSE_CONTENT.value}"
        )
        
    except Exception as e:
        faasr_log(e)
        return False
    
    # Create files to test faasr_rank
    
    for i in range(1, 11):
        filename = f"rank{i}.txt"
        with open(filename, 'w') as f:
            f.write(f"This is file {filename}\n")
            
        remote_file = f"{invocation_id}/rank_files/{filename}"
        faasr_put_file(local_file=filename, remote_file=remote_file, remote_folder=folder)
        faasr_log(
            f"Created file: {remote_file} with content: This is file {filename}"
        )