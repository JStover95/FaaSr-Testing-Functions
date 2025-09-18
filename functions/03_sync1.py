from FaaSr_py.client.py_client_stubs import (
    faasr_get_file,
    faasr_get_folder_list,
)

from .utils.enums import TestPyApi

#Check if input1 and input 4 is deleted, input2 & input 3 remained
#Validate content of output1 and output2 for R and Python

def sync1(folder: str,
         input1: str,
         input2: str,
         input3: str,
         input4: str,
         output1_py: str,
         output2_py: str,
         output1_R: str,
         output2_R: str,
         ):
    
    folder_list = faasr_get_folder_list(prefix=folder)
    
    try:
        #Test if input1 is deleted
        if input1 in folder_list:
            raise AssertionError(f"{input1} should be deleted. Still found in {folder} folder.")
        
        #Test if input4 is deleted
        if input4 in folder_list:
            raise AssertionError(f"{input4} should be deleted. Still found in {folder} folder.")
        
        #Test if input2 and input2 are still in the folder
        if input2 not in folder_list:
            raise AssertionError(f"{input2} not in {folder} folder.")
        
        if input3 not in folder_list:
            raise AssertionError(f"{input3} not in {folder} folder.")
        
        #Check if any output files are missing
        if (output1_py not in folder_list or output2_py not in folder_list
            or output1_R not in folder_list or output2_R not in folder_list):
            raise AssertionError(f"Output file(s) missing in {folder} folder")
            
        #Validate content of output files
        faasr_get_file(local_file=output1_py, remote_file=output1_py, remote_folder=folder)
        with open(output1_py, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_1_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output1_py}")
            
        faasr_get_file(local_file=output2_py, remote_file=output2_py, remote_folder=folder)
        with open(output2_py, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_2_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output2_py}")
            
        #Note: Content of output1 and output2 for both R and Python are identical. 
        faasr_get_file(local_file=output1_R, remote_file=output1_R, remote_folder=folder)
        with open(output1_R, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_1_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output1_R}")
        
        faasr_get_file(local_file=output2_R, remote_file=output2_R, remote_folder=folder)
        with open(output2_R, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_2_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output2_R}")
    
    #Return false if any of the tests failed
    except AssertionError as e:
        print(e)
        return False
    
    #Return true if all tests passed
    return True