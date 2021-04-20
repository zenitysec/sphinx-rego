import pytest

from deepdiff import DeepDiff

# noinspection PyProtectedMember
from sphinxrego.opa import _rego_json_to_obj, flatten


@pytest.mark.parametrize("inp, exp", (
    ({"type": "object", "value": [[{"type": "string", "value": "key"}, {"type": "string", "value": "val"}]]}, {"key": "val"}),
    ({"type": "array", "value": [{"type": "string", "value": "val1"}, {"type": "string", "value": "val2"}]}, ["val1", "val2"]),
    ({"type": "string", "value": "val"}, "val"),
    ({"type": "number", "value": 1}, 1),
    ({"type": "boolean", "value": True}, True),
    ({"type": "null", "value": {}}, None)
))
def test_rego_json_to_obj(inp, exp):
    got = _rego_json_to_obj(inp, validate_structure=False)
    assert not DeepDiff(exp, got)


@pytest.mark.parametrize("inp, exp", (
    ({"a": 1}, {"a": 1}),
    ({"a": {"a": 1}}, {"a.a": 1}),
    ({"a": [1, 2]}, {"a.0": 1, "a.1": 2}),
    ({"a": (1, 2)}, {"a.0": 1, "a.1": 2}),
    ({"a": [1, {"a": 2}]}, {"a.0": 1, "a.1.a": 2})
))
def test_flatten(inp, exp):
    got = flatten(inp)
    assert not DeepDiff(exp, got)
