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
        
        # Test if input4 is deleted
        remote_input4 = f"{folder}/{invocation_id}/{input4}"
        if remote_input4 in folder_list:
            raise AssertionError(f"{input4} should be deleted. Still found in {folder} folder.")
        
        faasr_log(f"Pass: {input4} is deleted.")
        
        # Test if input2 and input3 are still in the folder
        remote_input2 = f"{folder}/{invocation_id}/{input2}"
        if remote_input2 not in folder_list:
            raise AssertionError(f"{input2} not in {folder} folder.")
        
        remote_input3 = f"{folder}/{invocation_id}/{input3}"
        if remote_input3 not in folder_list:
            raise AssertionError(f"{input3} not in {folder} folder.")
        
        faasr_log(f"Pass: {input2} and {input3} are still in the folder.")
        
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