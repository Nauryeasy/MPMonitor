from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


VT = TypeVar('VT', bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[VT]):
    value: VT

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        ...

    @abstractmethod
    def as_generic_type(self) -> VT:
        ...


@dataclass(frozen=True)
class Id(BaseValueObject[int]):

    def validate(self) -> None:
        if not self.value:
            raise ValueError('Id cannot be empty')

        if not isinstance(self.value, int):
            raise ValueError('Id must be an integer')

        if self.value < 0:
            raise ValueError('Id cannot be negative')

    def as_generic_type(self) -> int:
        return int(self.value)
