from FaaSr_py.client.py_client_stubs import (
    faasr_get_file,
    faasr_get_folder_list,
    faasr_invocation_id,
    faasr_log,
)

from .utils.enums import TestRank


def sync2(
    folder: str,
    rank_folder: str,
    run_true_output: str,
    run_false_output: str,
) -> None:
    faasr_log("Starting Sync2...")

    invocation_id = faasr_invocation_id()
    remote_prefix = f"{folder}/{invocation_id}"
    folder_list = faasr_get_folder_list(prefix=remote_prefix)
    faasr_log(f"List of objects in {remote_prefix}: {folder_list}")

    try:
        # Test if run_true_output.txt and run_false_output.txt are still in the folder
        remote_run_true_output = f"{remote_prefix}/{run_true_output}"
        if remote_run_true_output not in folder_list:
            raise AssertionError(f"{remote_run_true_output} not in {folder} folder.")

        remote_run_false_output = f"{remote_prefix}/{run_false_output}"
        if remote_run_false_output not in folder_list:
            raise AssertionError(f"{remote_run_false_output} not in {folder} folder.")

        faasr_log(f"Pass: {run_true_output} and {run_false_output} are in the folder.")

        remote_rank_output = f"{remote_prefix}/{rank_folder}/rank"

        for i in range(1, 6):
            remote_rank_file = f"{remote_rank_output}{i}.txt"
            if remote_rank_file not in folder_list:
                raise AssertionError(f"{remote_rank_file} not in {folder} folder.")

            faasr_log(f"Pass: {remote_rank_file} is in the folder.")

            remote_file = f"{invocation_id}/{rank_folder}/rank{i}.txt"
            local_file = f"rank{i}.txt"
            faasr_get_file(
                local_file=local_file, remote_file=remote_file, remote_folder=folder
            )
            with open(local_file, "r") as f:
                content = f.read()
                content = content.strip()
                if content != f"{TestRank}{i}":
                    raise AssertionError(f"Incorrect content in {local_file}")

                faasr_log(f"Pass: {local_file} has the correct content: {content}")

    except AssertionError as e:
        faasr_log(str(e))
        return False

    return True
