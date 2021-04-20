import pytest

from deepdiff import DeepDiff

# noinspection PyProtectedMember
from sphinxrego.opa import _rego_json_to_obj


@pytest.mark.parametrize("inp, exp", (
    ({"type": "object", "value": [[{"type": "string", "value": "key"}, {"type": "string", "value": "val"}]]}, {"key": "val"}),
    ({"type": "array", "value": [{"type": "string", "value": "val1"}, {"type": "string", "value": "val2"}]}, ["val1", "val2"]),
    ({"type": "string", "value": "val"}, "val"),
    ({"type": "number", "value": 1}, 1),
    ({"type": "boolean", "value": True}, True),
    ({"type": "null", "value": {}}, None)
))
def test_rego_json_to_obj(inp, exp):
    got = _rego_json_to_obj(inp)
    assert not DeepDiff(exp, got)
