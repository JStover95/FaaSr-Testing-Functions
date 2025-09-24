# Note: This will be run if 03_sync1 fails and return True
# End Workflow

from FaaSr_py.client.py_client_stubs import faasr_log

def test_dontrun_false() -> None:
    
    faasr_log("Ending Workflow...")