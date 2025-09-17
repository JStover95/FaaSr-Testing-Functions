source("utils/utils.R")
source("utils/enums.R")

test_R_api <- function(folder, input1, input2, input3, output1, output2) {
  invocation_id = get_invocation_id()
  
  #Test deleting input1
  remote_filename1 <- paste0(invocation_id, '/', input1)
  faasr_delete_file(remote_filename)
  
  #Test getting input2
  remote_filename2 <- paste0(invocation_id, '/', input2)
  faasr_get_file(remote_folder=folder, remote_file=remote_filename2, local_file=input2)
  
  #Test getting input3
  remote_filename3 <- paste0(invocation_id, '/', input3)
  faasr_get_file(remote_folder=folder, remote_file=remote_filename3, local_file=input3)
  
  #Test putting output1
  writeLines(unlist(TestRApi)[1], output1)
  faasr_put_file(local_file=output1, remote_folder_folder, remote_output=output1)
  
  #Test putting output2
  writeLines(unlist(TestRApi)[2], output2)
  faasr_put_file(local_file=output2, remote_folder_folder, remote_output=output2)
  
  
  
  
  
  
}