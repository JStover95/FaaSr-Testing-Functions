from FaaSr_py.client.py_client_stubs import (
    faasr_get_file,
    faasr_get_folder_list,
    faasr_invocation_id,
    faasr_log,
)

from .utils.enums import TestPyApi

# Check for required files and validate content of the files


def sync1(
    folder: str,
    input1: str,
    input2: str,
    input3: str,
    input4: str,
    output1_py: str,
    output2_py: str,
    output1_R: str,
    output2_R: str,
) -> None:
    faasr_log("Starting Sync1...")

    invocation_id = faasr_invocation_id()
    remote_prefix = f"{folder}/{invocation_id}"
    folder_list = faasr_get_folder_list(prefix=remote_prefix)

    try:
        # Test if input1 is deleted by 02b_test_py_api
        remote_input1 = f"{remote_prefix}/{input1}"
        if remote_input1 in folder_list:
            raise AssertionError(
                f"{input1} should be deleted. Still found in {folder} folder."
            )

        faasr_log(f"Pass: {input1} is deleted.")

        # Test if input4 is deleted by 02a_test_r_api
        remote_input4 = f"{remote_prefix}/{input4}"
        if remote_input4 in folder_list:
            raise AssertionError(
                f"{input4} should be deleted. Still found in {folder} folder."
            )

        faasr_log(f"Pass: {input4} is deleted.")

        # Test if input2 and input3 are still in the folder
        remote_input2 = f"{remote_prefix}/{input2}"
        if remote_input2 not in folder_list:
            raise AssertionError(f"{input2} not in {folder} folder.")

        remote_input3 = f"{remote_prefix}/{input3}"
        if remote_input3 not in folder_list:
            raise AssertionError(f"{input3} not in {folder} folder.")

        faasr_log(f"Pass: {input2} and {input3} are in the folder.")

        # Check if any output files are missing (using full path)
        remote_output1_py = f"{remote_prefix}/{output1_py}"
        remote_output2_py = f"{remote_prefix}/{output2_py}"
        remote_output1_R = f"{remote_prefix}/{output1_R}"
        remote_output2_R = f"{remote_prefix}/{output2_R}"
        if (
            remote_output1_py not in folder_list
            or remote_output2_py not in folder_list
            or remote_output1_R not in folder_list
            or remote_output2_R not in folder_list
        ):
            raise AssertionError(f"Output file(s) missing in {folder} folder")

        faasr_log("Pass: all output files are in the folder.")

        # Validate content of output files
        remote_file = f"{invocation_id}/{output1_py}"
        faasr_get_file(
            local_file=output1_py, remote_file=remote_file, remote_folder=folder
        )
        with open(output1_py, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_1_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output1_py}")

        faasr_log(f"Pass: {output1_py} has the correct content: {content}")

        remote_file = f"{invocation_id}/{output2_py}"
        faasr_get_file(
            local_file=output2_py, remote_file=remote_file, remote_folder=folder
        )
        with open(output2_py, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_2_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output2_py}")

        faasr_log(f"Pass: {output2_py} has the correct content: {content}")

        # Note: Content of output1 and output2 for both R and Python are identical.
        remote_file = f"{invocation_id}/{output1_R}"
        faasr_get_file(
            local_file=output1_R, remote_file=remote_file, remote_folder=folder
        )
        with open(output1_R, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_1_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output1_R}")

        faasr_log(f"Pass: {output1_R} has the correct content: {content}")

        remote_file = f"{invocation_id}/{output2_R}"
        faasr_get_file(
            local_file=output2_R, remote_file=remote_file, remote_folder=folder
        )
        with open(output2_R, "r") as f:
            content = f.read()
            content = content.strip()
            if content != TestPyApi.OUTPUT_2_CONTENT.value:
                raise AssertionError(f"Incorrect content in {output2_R}")

        faasr_log(f"Pass: {output2_R} has the correct content: {content}")

    # Return false if any of the tests failed -> 04b_test_dontrun_false.py will be invoked
    except AssertionError as e:
        faasr_log(str(e))
        return False

    # Return true if all tests passed -> 04a_test_run_true.py will be invoked
    faasr_log("Sync1 Completed: Returning True to invoke test_run_true")
    return True
