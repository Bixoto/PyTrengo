from datetime import datetime

import pytest

from trengo import make_params


@pytest.mark.parametrize("raw,expected", [
    ({}, {}),
    # arrays
    ({"foo[]": None}, {}),
    ({"foo[]": range(2)}, {"foo[]": [0, 1]}),
    ({"foo": datetime(2024, 1, 1, 12, 0, 0)}, {"foo": "2024-01-01T12:00:00"}),
])
def test_make_params(raw, expected):
    assert make_params(raw) == expected
