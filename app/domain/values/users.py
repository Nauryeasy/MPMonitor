from abc import ABC
from dataclasses import dataclass, field
import re
import bcrypt

from domain.values.base import BaseValueObject
from domain.exceptions.users import (
    UserNameIsEmptyException,
    UserNameIsTooLongException,
    UserNameIsTooShortException,
    UserNameIsNotAlphanumericException,
    EmailIsEmptyException,
    EmailIsNotValidException,
    EmailIsTooLongException,
    PasswordIsEmptyException,
)


@dataclass(frozen=True)
class BaseUserValueObject(BaseValueObject, ABC):
    ...


@dataclass(frozen=True)
class UserName(BaseUserValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise UserNameIsEmptyException()

        if len(self.value) < 3:
            raise UserNameIsTooShortException(self.value)

        if len(self.value) > 50:
            raise UserNameIsTooLongException(self.value)

        if not self.value.isalnum():

            # TODO: Change the validation to check the content of special characters

            raise UserNameIsNotAlphanumericException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseUserValueObject):
    __email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmailIsEmptyException()

        if len(self.value) > 50:
            raise EmailIsTooLongException(self.value)

        if not self.__email_pattern.match(self.value):
            raise EmailIsNotValidException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Password(BaseUserValueObject):
    value: str = field(repr=False)

    def __post_init__(self):
        super().__post_init__()
        hashed_password = self.__hash_password()

        object.__setattr__(self, 'value', hashed_password)

    def __hash_password(self) -> str:
        return bcrypt.hashpw(self.value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def validate(self) -> None:
        if not self.value:
            raise PasswordIsEmptyException()

    def as_generic_type(self) -> str:
        return str(self.value)
