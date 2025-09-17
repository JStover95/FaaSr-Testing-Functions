import argparse
import json
import logging
import os
import sys
import time
import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any

import boto3
from FaaSr_py.engine.faasr_payload import FaaSrPayload
from FaaSr_py.helpers.s3_helper_functions import get_invocation_folder
from pydantic import BaseModel, Field

from integration_test_framework.utils import LOGGER_NAME
from workflow.scripts.invoke_workflow import WorkflowMigrationAdapter  # noqa: F401

DEFAULT_TIMEOUT_SECONDS = 1800
DEFAULT_CHECK_INTERVAL = 5

REQUIRED_ENV_VARS = [
    "MY_S3_BUCKET_ACCESSKEY",
    "MY_S3_BUCKET_SECRETKEY",
    "GITHUB_TOKEN",
]

EPILOGUE = f"""Example usage:
python integration_test_framework.py --workflow-file workflow/workflows/main.json

Required environment variables:
{"\n- ".join(REQUIRED_ENV_VARS)}

Note: Currently, this framework only supports GitHub Actions.
"""


class FunctionStatus(Enum):
    """Test execution status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class TestResult(BaseModel):
    """Function test result"""

    expected_output: str
    actual_output: str
    passed: bool


class FunctionResult(BaseModel):
    """Function test result"""

    function_name: str
    status: FunctionStatus
    start_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_time: datetime | None = Field(None)
    duration: float | None = Field(None)
    error_message: str | None = Field(None)
    test_results: list[TestResult]


class InitializationError(Exception):
    """Exception raised for initialization errors"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error initializing integration tester: {self.message}"


class WorkflowConfigurationError(Exception):
    """Exception raised for workflow configuration errors"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error configuring workflow: {self.message}"


class WorkflowExecutionError(Exception):
    """Exception raised for workflow execution errors"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error executing workflow: {self.message}"


class WorkflowTriggerError(Exception):
    """Exception raised for workflow trigger errors"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error triggering workflow: {self.message}"


class FaaSrPayloadAdapter(FaaSrPayload):
    """Adapter for FaaSrPayload to work with local workflow files"""

    def __init__(
        self,
        url: str,
        overwritten: dict[str, Any],
        local_workflow_data: dict[str, Any],
    ):
        self.url = url
        self._overwritten = overwritten or {}
        self._base_workflow = local_workflow_data

        # Set up log file name
        if self.get("FunctionRank"):
            self.log_file = f"{self['FunctionInvoke']}({self['FunctionRank']}).txt"
        else:
            self.log_file = f"{self['FunctionInvoke']}.txt"


class FaaSrIntegrationTester:
    """Class for running integration tests"""

    logfile_fstr = "logs/integration_test_{timestamp}.log"

    def __init__(self, workflow_file: str, timeout: int, check_interval: int):
        """
        Initialize the integration tester.

        Args:
            workflow_file: Path to the FaaSr workflow JSON file
        """
        self._validate_environment()

        self.workflow_file = workflow_file
        self.workflow_data = self._load_workflow()
        self.function_statuses: dict[str, FunctionStatus] = {
            function_name: FunctionStatus.PENDING
            for function_name in self.workflow_data["ActionList"].keys()
        }
        self.faasr_payload = None
        self.test_result = None
        self.timeout = timeout
        self.check_interval = check_interval

        # Setup logging
        self.log_timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
        self._setup_logging()

        # Initialize S3 client for monitoring
        self.s3_client = None
        self._init_s3_client()

    def _validate_environment(self):
        """Validate environment variables"""
        missing_env_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_env_vars:
            raise InitializationError(
                f"Missing required environment variables: {', '.join(missing_env_vars)}"
            )

    def _setup_logging(self):
        """Setup logging configuration"""
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(
                    self.logfile_fstr.format(timestamp=self.log_timestamp)
                ),
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.logger = logging.getLogger(LOGGER_NAME)

    def _load_workflow(self) -> dict[str, Any]:
        """Load and validate workflow configuration"""
        self.logger.info("Loading workflow configuration")

        try:
            with open(self.workflow_file, "r") as f:
                workflow = json.load(f)
            self.logger.info(
                f"Loaded workflow: {workflow.get('WorkflowName', 'Unknown')}"
            )
            return workflow
        except Exception as e:
            self.logger.error(f"Failed to load workflow file: {e}")
            raise InitializationError(f"Failed to load workflow file: {e}")

    def _init_s3_client(self):
        """Initialize S3 client for monitoring"""
        self.logger.info("Initializing S3 client for monitoring")

        try:
            # Create a mock FaaSrPayload to get S3 credentials
            # In a real scenario, you'd get these from your test config
            default_datastore = self.workflow_data.get(
                "DefaultDataStore",
                "My_S3_Bucket",
            )
            datastore_config = self.workflow_data["DataStores"][default_datastore]

            if datastore_config.get("Endpoint"):
                self.s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=os.getenv("MY_S3_BUCKET_ACCESSKEY"),
                    aws_secret_access_key=os.getenv("MY_S3_BUCKET_SECRETKEY"),
                    region_name=datastore_config["Region"],
                    endpoint_url=datastore_config["Endpoint"],
                )
            else:
                self.s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=os.getenv("MY_S3_BUCKET_ACCESSKEY"),
                    aws_secret_access_key=os.getenv("MY_S3_BUCKET_SECRETKEY"),
                    region_name=datastore_config["Region"],
                )

            self.bucket_name = datastore_config["Bucket"]
            self.logger.info(f"Initialized S3 client for bucket: {self.bucket_name}")

        except Exception as e:
            self.logger.error(f"Failed to initialize S3 client: {e}")
            raise InitializationError(f"Failed to initialize S3 client: {e}")

    def _create_faasr_payload(self) -> FaaSrPayload:
        """Create FaaSrPayload for workflow execution"""
        self.logger.info("Creating FaaSrPayload for workflow execution")

        try:
            workflow = self.workflow_data.copy()

            # Create a mock GitHub URL for local testing
            github_url = (
                f"local/{self.workflow_data.get('WorkflowName', 'test')}/workflow.json"
            )

            # Create FaaSrPayload with local data
            payload = FaaSrPayloadAdapter(github_url, workflow, workflow)

            # Generate InvocationID if not present
            if not payload.get("InvocationID"):
                payload["InvocationID"] = str(uuid.uuid4())

            return payload

        except Exception as e:
            self.logger.error(f"Failed to create FaaSrPayload: {e}")
            raise WorkflowConfigurationError(f"Failed to create FaaSrPayload: {e}")

    def _trigger_workflow(self):
        """Trigger the workflow execution"""
        self.logger.info("Triggering workflow execution")

        try:
            adapter = WorkflowMigrationAdapter(self.workflow_file)
            adapter.trigger_workflow()
            self.logger.info("Workflow triggered successfully")
        except Exception as e:
            self.logger.error(f"Failed to trigger workflow: {e}")
            raise WorkflowTriggerError(f"Failed to trigger workflow: {e}")

    def _monitor_workflow_execution(self):
        """Monitor the workflow execution"""
        self.logger.info(
            f"Monitoring workflow execution for functions: {', '.join(self.function_statuses.keys())}"
        )

        start_time = datetime.now(UTC)

        while time.time() - start_time < self.timeout:
            for function_name, status in self.function_statuses.items():
                if status == FunctionStatus.PENDING or status == FunctionStatus.RUNNING:
                    if self._check_function_completion(function_name):
                        self._set_function_status(
                            function_name,
                            FunctionStatus.COMPLETED,
                        )
                        self.logger.info(f"Function {function_name} completed")
                    elif self._check_function_running(function_name):
                        self._set_function_status(
                            function_name,
                            FunctionStatus.RUNNING,
                        )
                        all_completed = False

            if all_completed:
                self.logger.info("All functions completed")
                break

            time.sleep(self.check_interval)

        # Check for timeouts
        for function_name, status in self.function_statuses.items():
            if status == FunctionStatus.PENDING or status == FunctionStatus.RUNNING:
                self._set_function_status(
                    function_name,
                    FunctionStatus.TIMEOUT,
                )
                self.logger.warning(f"Function {function_name} timed out")

    def _check_function_completion(self, function_name: str) -> bool:
        """Check if a function has completed by looking for .done file in S3"""
        try:
            # Get the invocation folder path
            invocation_folder = get_invocation_folder(self.faasr_payload)

            # Check for .done file
            done_file_path = (
                f"{invocation_folder}/function_completions/{function_name}.done"
            )

            # List objects with this prefix
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=str(done_file_path),
            )

            return "Contents" in response and len(response["Contents"]) > 0

        except Exception as e:
            self.logger.error(f"Error checking completion for {function_name}: {e}")
            return False

    def _check_function_running(self, function_name: str) -> bool:
        """Check if a function is running by looking for log files in S3"""
        try:
            # Get the invocation folder path
            invocation_folder = get_invocation_folder(self.faasr_payload)

            # Check for log files
            log_prefix = f"{invocation_folder}/{function_name}"

            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=str(log_prefix),
            )

            return "Contents" in response and len(response["Contents"]) > 0

        except Exception as e:
            self.logger.error(f"Error checking running status for {function_name}: {e}")
            return False

    def _set_function_status(self, function_name: str, status: FunctionStatus):
        """Set the status of a function"""
        self.function_statuses[function_name] = status


def main() -> int:
    """Main entry point for the integration testing framework"""
    parser = argparse.ArgumentParser(description="FaaSr Integration Testing Framework")
    parser.add_argument(
        "--workflow-file",
        required=True,
        help="Path to the FaaSr workflow JSON file",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Timeout in seconds for workflow execution",
    )
    parser.add_argument(
        "--check-interval",
        type=int,
        default=DEFAULT_CHECK_INTERVAL,
        help="Interval in seconds for checking workflow execution",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Run integration test
    try:
        tester = FaaSrIntegrationTester(
            args.workflow_file, args.timeout, args.check_interval
        )
    except InitializationError as e:
        import traceback

        print(f"‼️ Error initializing integration tester: {e}")
        print("=" * 60)
        print("Traceback:")
        print("=" * 60)
        traceback.print_exc()
        return 1

    try:
        if tester.run_integration_test():
            print("✅ Integration test completed successfully")
            return 0
        else:
            print("❌ Integration test failed")
            return 1
    except Exception as e:
        import traceback

        print(f"‼️ Error running integration test: {e}")
        print("=" * 60)
        print("Traceback:")
        print("=" * 60)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
