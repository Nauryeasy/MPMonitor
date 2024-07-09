from dataclasses import dataclass, field
import re
import bcrypt

from domain.values.base import BaseValueObject

# TODO: Add tests

@dataclass(frozen=True)
class UserName(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise ValueError('Name cannot be empty')

        if len(self.value) < 3:
            raise ValueError('Name must be at least 3 characters long')

        if len(self.value) > 50:
            raise ValueError('Name must be at most 50 characters long')

        if not self.value.isalnum():

            # TODO: Change the validation to check the content of special characters

            raise ValueError('Name must only contain letters')

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseValueObject):
    __email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    value: str

    def validate(self):
        if not self.value:
            raise ValueError('Email cannot be empty')

        if len(self.value) > 50:
            raise ValueError('Email must be at most 50 characters long')

        if not self.__email_pattern.match(self.value):
            raise ValueError('Email is not valid')

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Password(BaseValueObject):
    value: str = field(repr=False)

    def __post_init__(self):
        super().__post_init__()
        hashed_password = self.__hash_password()

        object.__setattr__(self, 'value', hashed_password)

    def __hash_password(self):
        return bcrypt.hashpw(self.value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def validate(self):
        if not self.value:
            raise ValueError('Password cannot be empty')

    def as_generic_type(self):
        return str(self.value)
