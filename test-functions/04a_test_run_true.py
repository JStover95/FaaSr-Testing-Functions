# Note: This will be run if 03_sync1 runs successfully and return True
# Get csv file (input 3) using faasr_get_file
# Find the fruit with highest price
# Save it into s3 bucket using faasr_put_file
# Arguments: folder, input, output
# Return False -> invoke 05a_test_run_false

from FaaSr_py.client.py_client_stubs import (
    faasr_get_file,
    faasr_log,
    faasr_put_file,
)

import pandas as pd
from .utils import get_invocation_id

def test_run_true(folder: str,
                  input3: str,
                  output: str
                  ) -> None:
    
    invocation_id = get_invocation_id()
    
    remote_file = f"{invocation_id}/{input3}"
    faasr_get_file(
        local_file=input3,
        remote_file=remote_file,
        remote_folder=folder,
    )
    
    faasr_log(f"Saved remote file: {remote_file} to {input3}")
    
    df = pd.read_csv(input3, delimiter=",")
    max_df = df[df['price'] == df['price'].max()]
    max_df.to_csv(output, index=False)
    
    remote_file = f"{invocation_id}/{output}"
    faasr_put_file(local_file=output, remote_file=remote_file, remote_folder=folder)
    faasr_log(
        f"Created output file: {remote_file} with content: {max_df}"
    )
    
    