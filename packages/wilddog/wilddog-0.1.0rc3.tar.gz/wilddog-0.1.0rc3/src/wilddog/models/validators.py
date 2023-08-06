import abc
from typing import Any, Generic, Literal, Type, TypedDict, TypeVar, Union

ValueTypeLiteral = Literal["String", "Numeric", "Boolean"]
T = Union[bool, float, str]


__all__ = ["BooleanType", "NumericType", "StringType", "validate"]


class ValueType(abc.ABC):
    @property
    @abc.abstractmethod
    def type(self) -> Type[T]:
        ...

    def value_of(self, value: str) -> T:
        return self.type(value)

    def validate(self, value: Any) -> None:
        if isinstance(value, self.type):
            return
        self.type(value)


class StringType(ValueType):
    @property
    def type(self) -> Type[str]:
        return str


class BooleanType(ValueType):
    @property
    def type(self) -> Type[bool]:
        return bool

    def value_of(self, value: str) -> bool:
        return value in ["true", "t", "1", "y", "yes"]


class NumericType(ValueType):
    @property
    def type(self) -> Type[float]:
        return float


class ValueTypes(TypedDict):
    String: StringType
    Numeric: NumericType
    Boolean: BooleanType


VALUE_TYPES: ValueTypes = {
    "String": StringType(),
    "Numeric": NumericType(),
    "Boolean": BooleanType(),
}


def get_type(name: ValueTypeLiteral) -> ValueType:
    return VALUE_TYPES[name]


def validate(value_type: ValueTypeLiteral, value: str) -> None:
    ty = VALUE_TYPES[value_type]
    ty.validate(value)
