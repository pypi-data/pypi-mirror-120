from typing import Any

import pytest

from wilddog.models import validators


@pytest.mark.parametrize("value", ["123", 12, "sdff"])
def test_string_validator(value: Any) -> None:
    str_type = validators.StringType()
    str_type.validate(value)
    assert str(value) == str_type.value_of(value)


@pytest.mark.parametrize(
    "value, expectation", [("false", False), ("true", True), ("1", True), ("0", False)]
)
def test_boolean_validator(value: Any, expectation: bool) -> None:
    _type = validators.BooleanType()
    _type.validate(value)
    assert _type.value_of(value) == expectation


@pytest.mark.parametrize("value, expectation", [(12, 12.0), ("11", 11.0), ("1.1", 1.1), ("0", 0)])
def test_numeric_validator(value: Any, expectation: float) -> None:
    _type = validators.NumericType()
    _type.validate(value)
    assert _type.value_of(value) == expectation


@pytest.mark.parametrize("value", ["12s3", "a.s", "sdff"])
def test_numeric_validator__invalid(value: Any) -> None:
    str_type = validators.NumericType()
    with pytest.raises(ValueError):
        str_type.validate(value)
