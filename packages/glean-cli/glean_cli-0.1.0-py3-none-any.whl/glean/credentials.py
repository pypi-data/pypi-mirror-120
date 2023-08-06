from dataclasses import dataclass
import json
import os.path


@dataclass
class CliCredentials:
    access_key_id: str
    access_key_token: str
    project_id: str


def parse_credentials(credentials_filepath) -> CliCredentials:
    """Parses the provided credentials file."""
    if not os.path.isfile(credentials_filepath):
        raise RuntimeError(f"Credentials file does not exist ({credentials_filepath})")

    with open(credentials_filepath, "r") as f:
        credentials_json = f.read()

    try:
        credentials = json.loads(credentials_json)
        return CliCredentials(**credentials)
    except Exception as e:
        raise RuntimeError("Invalid credentials file.") from e
