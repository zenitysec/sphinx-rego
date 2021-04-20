from typing import Union

import os
import subprocess

import json

try:
    subprocess.check_call(["opa"], stdout=subprocess.PIPE)
except subprocess.CalledProcessError:
    raise AssertionError("Could not find `opa`, please install from https://www.openpolicyagent.org/docs/latest/")


def get_metadoc(path: str) -> dict:
    """
    Load and parse __rego_metadoc__ from path
    :param path: location of .rego file
    :return: Python object representing metadoc
    """
    if not os.path.isfile(path):
        raise OSError(f"Couldn't find file at {path}")

    _, ext = os.path.splitext(path)
    if ext != ".rego":
        raise ValueError(f"File extension must be .rego, not {ext}")

    parsed = subprocess.check_output(f"opa parse --format json {path}".split(" "))
    jsn = json.loads(parsed)

    for r in jsn.get("rules", []):
        h = r.get("head", {})
        v = h.get("value", {})
        if h.get("name") == "__rego__metadoc__" and v.get("type") == "object":
            raw_metadoc = v
            break
    else:
        raise ValueError(f"Couldn't find __rego__metadoc__ rule in {path}")

    return _rego_json_to_obj(raw_metadoc)


def _rego_json_to_obj(r: dict) -> Union[dict, list, str, bool, int, None]:
    """
    Recursively transform the JSON output of `OPA parse --format json` to a Python object
    :param r: raw JSON object
    :return: transformed object
    """
    if r["type"] in ("string", "number", "boolean"):
        return r["value"]
    if r["type"] == "null":
        return None
    if r["type"] == "object":
        return {_rego_json_to_obj(v1): _rego_json_to_obj(v2) for v1, v2 in r["value"]}
    if r["type"] == "array":
        return [_rego_json_to_obj(v) for v in r["value"]]
    raise ValueError(f"Unable to parse object {r}")
