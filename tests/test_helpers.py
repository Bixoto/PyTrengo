import pytest

from trengo import make_params


@pytest.mark.parametrize("raw,expected", [
    ({}, {}),
    # arrays
    ({"foo[]": None}, {}),
    ({"foo[]": range(2)}, {"foo[]": [0, 1]}),
])
def test_make_params(raw, expected):
    assert make_params(raw) == expected
