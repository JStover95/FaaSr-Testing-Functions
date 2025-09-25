# Note: This will be run if 04a_test_run_true fails and return True
# End Workflow

from FaaSr_py.client.py_client_stubs import faasr_log

def test_dontrun_true() -> None:
    
    faasr_log("Ending Workflow...")