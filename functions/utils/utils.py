import json
import os


def get_invocation_id() -> str:
    try:
        overwritten = json.loads(os.environ["OVERWRITTEN"])
        if (
            not isinstance(overwritten, dict)
            or "InvocationID" not in overwritten
            or not isinstance(overwritten["InvocationID"], str)
            or overwritten["InvocationID"].strip() == ""
        ):
            raise EnvironmentError("InvocationID is not set")
        return overwritten["InvocationID"]
    except KeyError as e:
        raise EnvironmentError("OVERWRITTEN is not set") from e
    except json.JSONDecodeError as e:
        raise EnvironmentError("OVERWRITTEN is not valid JSON") from e
    except EnvironmentError:
        raise
