from FaaSr_py.client.py_client_stubs import faasr_log, faasr_put_file


def create_input(
    folder: str,
    input1: str,
    input2: str,
    input3: str,
    input4: str,
) -> None:
    # Create input1 (input to be deleted using test_py_api)
    with open(input1, "w") as f:
        f.write("Test input1")
    
    faasr_put_file(
        local_file=input1,
        remote_file=input1,
        remote_folder=folder,
    )
    
    faasr_log(
        f"Created input1: {input1} with content: Test input1"
    )

    # Create input2
    with open(input2, "w") as f:
        f.write("Test input2")
    
    faasr_put_file(
        local_file=input2,
        remote_file=input2,
        remote_folder=folder,
    )
    
    faasr_log(
        f"Created input2: {input2} with content: Test input2"
    )


    # Create input3 (csv format, for arrow api)
    with open(input3, "w") as f:
        f.write("id,fruit,price\n1,apple,1.99\n2,banana,0.16\n3,strawberry,3.77\n")
    
    faasr_put_file(
        local_file=input3,
        remote_file=input3,
        remote_folder=folder,
    )
    
    faasr_log(
        f"Created input3: {input3} with content: id,fruit,price\n1,apple,1.99\n2,banana,0.16\n3,strawberry,3.77\n"
    )

        
    # Create input4 (input to be deleted using R API)
    with open(input4, "w") as f:
        f.write("Test input4")
    
    faasr_put_file(
        local_file=input4,
        remote_file=input4,
        remote_folder=folder,
    )
    
    faasr_log(
        f"Created input4: {input4} with content: Test input4"
    )
