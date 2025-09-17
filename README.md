# FaaSr-Testing

This repo contains functions that can be used for FaaSr integration testing.

**Functions:**

- **`01_create_input.py`**: An entrypoint for FaaSr integration testing that creates test data on S3.
- **`02b_test_py_api.py`**: A Python function for testing Python API functionality.

## Getting Started

1. Set up the Python virtual environment. Python 3.13 is recommended.

   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Utils

**`get_invocation_id`**:

This function attempts to retrieve the FaaSr workflow invocation ID from the environment. This allows for test isolation on S3. For example:

```py
from .utils import get_invocation_id


def function(folder: str, input: str) -> None:
    invocation_id = get_invocation_id()

    with open(input1, "w") as f:
        f.write("...")

    faasr_put_file(
        local_file=input1,
        remote_file=f"{invocation_id}/{input1}",  # Test isolation using the InvocationID
        remote_folder=folder,
    )
```

**`enums.py`**:

This file contains Enums that will act as a single source of truth across all integration tests.
