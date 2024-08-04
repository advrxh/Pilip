import json
from types import NoneType
from typing import List, Dict


def load_from_str(input: str):

    if isinstance(input, NoneType) or input is None:
        return None

    return json.loads(input)


def dump_to_str(input: List | Dict):

    return json.dumps(input, indent=None)
