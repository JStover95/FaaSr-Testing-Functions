import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any

import boto3

from integration_test_framework.utils import LOGGER_NAME
from workflow.scripts.invoke_workflow import WorkflowMigrationAdapter  # noqa: F401


class InitializationError(Exception):
    """Exception raised for initialization errors"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error initializing integration tester: {self.message}"


class FaaSrIntegrationTester:
    """Class for running integration tests"""

    logfile_fstr = "logs/integration_test_{timestamp}.log"

    def __init__(self, workflow_file: str):
        """
        Initialize the integration tester.

        Args:
            workflow_file: Path to the FaaSr workflow JSON file
        """
        self._validate_environment()

        self.workflow_file = workflow_file
        self.workflow_data = self._load_workflow()
        self.faasr_payload = None
        self.test_result = None

        # Setup logging
        self.log_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._setup_logging()

        # Initialize S3 client for monitoring
        self.s3_client = None
        self._init_s3_client()

    def _validate_environment(self):
        """Validate environment variables"""
        if not os.getenv("MY_S3_BUCKET_ACCESSKEY"):
            raise InitializationError("MY_S3_BUCKET_ACCESSKEY is not set")
        if not os.getenv("MY_S3_BUCKET_SECRETKEY"):
            raise InitializationError("MY_S3_BUCKET_SECRETKEY is not set")

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


def main() -> int:
    """Main entry point for the integration testing framework"""
    parser = argparse.ArgumentParser(description="FaaSr Integration Testing Framework")
    parser.add_argument(
        "--workflow-file",
        required=True,
        help="Path to the FaaSr workflow JSON file",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Run integration test
    tester = FaaSrIntegrationTester(args.workflow_file)
    if tester.run_integration_test():
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
