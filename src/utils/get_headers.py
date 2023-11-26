from typing import Optional, Union, Dict, List
import json


def get_headers(path: str, key: str):
    """Get header from a file.

    Args:
        path: Path to the file.
        key: Key of the header.

    Returns:
        Value of the header.
    """

    with open(path, "r", encoding="UTF-8") as file:
        headers: Dict[str, Dict[str, str]] = json.loads(file.read())

    try:
        return headers[key]
    except:
        raise EnvironmentError(f"Set the {key}")
