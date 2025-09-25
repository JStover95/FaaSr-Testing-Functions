library(arrow)

test_arrow <- function(folder, input4, input2, input3, output1, output2) {

  # Test deleting input4
  faasr_delete_file(remote_folder=folder, remote_file=input4)
  msg = paste0("Deleted input4: ", input4)
  faasr_log(msg)
  
  # Test getting input2
  faasr_get_file(remote_folder=folder, remote_file=input2, local_file=input2)
  msg = paste0("Saved remote file: ", input2, " to ", input2)
  faasr_log(msg)
  
  # Test getting input3 using arrow API
  mys3 <- faasr_arrow_s3_bucket()
  remote_path <- mys3$path(file.path(folder, input3))
  arrow_input <- arrow::read_csv_arrow(remote_path)
  
  # Test putting output1
#   writeLines("Test output1", output1)
#   remote_file <- paste0(invocation_id, '/', output1)
#   faasr_put_file(local_file=output1, remote_folder=folder, remote_file=remote_file)
#   msg = paste0("Created output file: ", remote_file, " with content: Test output1")
#   faasr_log(msg)
  
  # Test putting output2
#   writeLines("Test output2", output2)
#   remote_file <- paste0(invocation_id, '/', output2)
#   faasr_put_file(local_file=output2, remote_folder=folder, remote_file=remote_file)
#   msg = paste0("Created output file: ", remote_file, " with content: Test output2")
#   faasr_log(msg)

}