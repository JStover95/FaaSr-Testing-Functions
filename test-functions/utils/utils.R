library(jsonlite)

get_invocation_id <- function() {
  overwritten <- Sys.getenv("OVERWRITTEN", unset = NA)
  if (is.na(overwritten)) {
    stop("OVERWRITTEN is not set")
  }
  
  parsed <- tryCatch(fromJSON(overwritten), error = function(e) {
    stop("OVERWRITTEN is not valid JSON")
  })
  
  if (!is.list(parsed) ||
      is.null(parsed$InvocationID) ||
      !is.character(parsed$InvocationID) ||
      nchar(trimws(parsed$InvocationID)) == 0) {
    stop("InvocationID is not set")
  }
  
  return(parsed$InvocationID)
}
