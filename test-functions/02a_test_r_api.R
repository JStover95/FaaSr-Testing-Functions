source("utils/utils.R")
source("utils/enums.R")
library(arrow)

test_r_api <- function(folder, input4, input2, input3, output1, output2) {
  cat("Current working directory:", getwd(), "\n")
  invocation_id = get_invocation_id()
  msg = paste0("Using invocation ID: ", invocation_id)
  faasr_log(msg)

  # Test deleting input4
  remote_filename1 <- paste0(invocation_id, '/', input4)
  faasr_delete_file(remote_filename)
  msg = paste0("Deleted input4: ", input4)
  faasr_log(msg)
  
  # Test getting input2
  remote_filename2 <- paste0(invocation_id, '/', input2)
  faasr_get_file(remote_folder=folder, remote_file=remote_filename2, local_file=input2)
  msg = paste0("Saved remote file: ", input2, " to ", input2)
  faasr_log(msg)
  
  # Test getting input3 using arrow API
  mys3 <- faasr_arrow_s3_bucket(faasr_prefix=folder)
  remote_path3 <- mys3$path(file.path(folder, invocation_id, input3))
  arrow_input3 <- arrow::read_csv_arrow(remote_path3)
  
  # Test putting output1
  writeLines(unlist(TestRApi)[1], output1)
  faasr_put_file(local_file=output1, remote_folder_folder, remote_output=output1)
  
  # Test putting output2
  writeLines(unlist(TestRApi)[2], output2)
  faasr_put_file(local_file=output2, remote_folder_folder, remote_output=output2)
  
}