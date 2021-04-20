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


def _rego_json_to_obj(r: dict) -> dict:
    """
    Recursively transform the JSON output of `OPA parse --format json` to a Python object
    :param r: raw JSON object
    :return: transformed object
    """

    def _recu_rego_json_to_obj(_r: dict) -> Union[dict, list, str, bool, int, None]:
        if _r["type"] in ("string", "number", "boolean"):
            return _r["value"]
        if _r["type"] == "null":
            return None
        if _r["type"] == "object":
            return {_rego_json_to_obj(v1): _rego_json_to_obj(v2) for v1, v2 in _r["value"]}
        if _r["type"] == "array":
            return [_rego_json_to_obj(v) for v in _r["value"]]
        raise ValueError(f"Unable to parse object {_r}")

    # if `r` is a dict then `_recu_rego_json_to_obj(r)` is also a dict
    return _recu_rego_json_to_obj(r)


def flatten(r: dict) -> dict:
    """
    Recursively transform Python nested object to one-layer dict
    :param r: raw object
    :return: one-layer dict
    """

    def _recu_flatten(_r: Union[dict, list, tuple], _new: dict, prefix: str = "") -> None:
        if isinstance(_r, dict):
            idx = _r.keys()
        elif isinstance(_r, (list, tuple)):
            idx = range(len(_r))
        else:
            raise ValueError(f"Got unexpected value type {type(_r)}")

        for i in idx:
            v = _r[i]
            if isinstance(v, (str, int, bool, type(None))):
                _new[prefix + str(i)] = v
            else:
                _recu_flatten(v, _new, prefix + str(i) + ".")

    new = {}
    _recu_flatten(r, new)

    return new