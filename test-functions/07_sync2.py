from FaaSr_py.client.py_client_stubs import (
    faasr_get_file,
    faasr_log,
    faasr_get_folder_list,
)

from .utils.enums import TestConditional, TestRank
from .utils import get_invocation_id

def sync2(folder: str,
         run_true_output: str,
         run_false_output: str
         )->None:
    invocation_id = get_invocation_id()
    remote_prefix = f"{folder}/{invocation_id}"
    folder_list = faasr_get_folder_list(prefix=remote_prefix)
    faasr_log(f"List of objects in {remote_prefix}: {folder_list}")
    
    try:
        # Test if run_true_output and run_false_output are still in the folder
        remote_run_true_output = f"{remote_prefix}/{run_true_output}"
        if remote_run_true_output not in folder_list:
            raise AssertionError(f"{remote_run_true_output} not in {folder} folder.")
        
        remote_run_false_output = f"{remote_prefix}/{run_false_output}"
        if remote_run_false_output not in folder_list:
            raise AssertionError(f"{remote_run_false_output} not in {folder} folder.")
        
        faasr_log(f"Pass: {run_true_output} and {run_false_output} are still in the folder.")
        
        remote_rank_output = f"{remote_prefix}/rank_files/rank"
        
        for i in range(1, 6):
            remote_rank_file = f"{remote_rank_output}{i}"
            
        
        # Check if any output files are missing
        remote_output1_py = f"{folder}/{invocation_id}/{output1_py}"
        remote_output2_py = f"{folder}/{invocation_id}/{output2_py}"
        remote_output1_R = f"{folder}/{invocation_id}/{output1_R}"
        remote_output2_R = f"{folder}/{invocation_id}/{output2_R}"
        if (remote_output1_py not in folder_list or remote_output2_py not in folder_list
            or remote_output1_R not in folder_list or remote_output2_R not in folder_list):
            raise AssertionError(f"Output file(s) missing in {folder} folder")
        
        faasr_log("Pass: all output files are in the folder.")
        
        # Validate content of output files
        faasr_get_file(local_file=output1_py, remote_file=output1_py, remote_folder=folder)
        with open(output1_py, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_1_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output1_py}")
            
        faasr_log(f"Pass: {output1_py} has the correct content: {TestPyApi.OUTPUT_1_CONTENT.value}")
            
        faasr_get_file(local_file=output2_py, remote_file=output2_py, remote_folder=folder)
        with open(output2_py, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_2_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output2_py}")
            
        faasr_log(f"Pass: {output2_py} has the correct content: {TestPyApi.OUTPUT_2_CONTENT.value}")
            
        # Note: Content of output1 and output2 for both R and Python are identical. 
        faasr_get_file(local_file=output1_R, remote_file=output1_R, remote_folder=folder)
        with open(output1_R, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_1_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output1_R}")
            
        faasr_log(f"Pass: {output1_R} has the correct content: {TestPyApi.OUTPUT_1_CONTENT.value}")
        
        faasr_get_file(local_file=output2_R, remote_file=output2_R, remote_folder=folder)
        with open(output2_R, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_2_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output2_R}")
            
        faasr_log(f"Pass: {output2_R} has the correct content: {TestPyApi.OUTPUT_2_CONTENT.value}")
    
    # Return false if any of the tests failed -> 04b_test_dontrun_false.py will be invoked
    except AssertionError as e:
        faasr_log(str(e))
        return False
    
    # Return true if all tests passed -> 04a_test_run_true.py will be invoked
    faasr_log("Sync1 Completed: Returning True to invoke test_run_true")
    return True