from FaaSr_py.client.py_client_stubs import (
    faasr_delete_file,
    faasr_get_file,
    faasr_get_folder_list,
    faasr_get_s3_creds,
    faasr_log,
    faasr_put_file,
    faasr_rank,
    faasr_return,
)


def test_py_api(
    folder: str,
    input1: str,
    input2: str,
    input3: str,
    output1: str,
    output2: str,
) -> None:
    # Test deleting input1
    faasr_delete_file(input1)

    # Test getting input2
    faasr_get_file(local_file="local2.txt", remote_file=input2, remote_folder=folder)

    # Test getting input3
    faasr_get_file(local_file="local3.txt", remote_file=input3, remote_folder=folder)

    # Test listing folder
    print("Getting folder list", faasr_get_folder_list(folder))

    # Test getting s3 creds
    print("Getting s3 creds", faasr_get_s3_creds())

    # Test logging
    faasr_log("Test log")

    # Test putting output1
    with open("local1.txt", "w") as f:
        f.write("Test output1")
    faasr_put_file(local_file="local1.txt", remote_file=output1, remote_folder=folder)

    # Test putting output2
    with open("local2.txt", "w") as f:
        f.write("Test output2")
    faasr_put_file(local_file="local2.txt", remote_file=output2, remote_folder=folder)

    # Test rank
    print("Getting rank", faasr_rank())

    # Return
    faasr_return("Test return")
