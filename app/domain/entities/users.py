import datetime
from abc import ABCMeta
from dataclasses import dataclass
from typing import Any

import bcrypt

from domain.entities.base import BaseEntity
from domain.events.users import NewUserRegisteredEvent, UserUpdatedEvent
from domain.exceptions.users import TypeIsNotValidException
from domain.values.users import UserName, Email, Password, BaseUserValueObject


# TODO: Understand why after overriding annotations the default values do not get into the child class
# class UserInheritsAnnotationsMeta(ABCMeta):
#     def __new__(cls, name, bases, namespace, **kwargs):
#         annotations = namespace.get('__annotations__', {})
#         print(namespace)
#         for base in bases:
#             annotations.update(getattr(base, '__annotations__', {}))
#         namespace['__annotations__'] = annotations
#         return super().__new__(cls, name, bases, namespace, **kwargs)


# TODO: Add User logic methods


@dataclass(eq=False)
class User(BaseEntity):  # metaclass=UserInheritsAnnotationsMeta):

    _is_initialised = False

    username: UserName
    first_name: UserName
    last_name: UserName
    email: Email
    password: Password

    def __post_init__(self) -> None:
        self._is_initialised = True

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.value.encode('utf-8'))

    def register_new_user(self) -> None:
        self.register_event(
            NewUserRegisteredEvent(
                user_oid=self.oid,
                user_username=self.username.as_generic_type(),
                user_first_name=self.first_name.as_generic_type(),
                user_last_name=self.last_name.as_generic_type(),
                user_email=self.email.as_generic_type(),
                user_password=self.password.as_generic_type(),
            )
        )

    def __setattr__(self, key: str, value: Any) -> None:
        if not issubclass(type(value), BaseUserValueObject):
            if key not in self.__annotations__:
                super().__setattr__(key, value)
                return
            if self.__annotations__[key].__annotations__['value'] != type(value):
                raise TypeIsNotValidException(
                    gotten_type=type(value),
                    expected_type=str(self.__annotations__[key])
                )
            value = self.__annotations__[key](value)

        if self._is_initialised:
            self.register_event(
                UserUpdatedEvent(
                    user_oid=self.oid,
                    change_type=self.__annotations__[key],
                    old_value=getattr(self, key).as_generic_type(),
                    new_value=value.as_generic_type(),
                )
            )

        super().__setattr__(key, value)


if __name__ == '__main__':
    user = User(
        username=UserName('test'),
        first_name=UserName('test'),
        last_name=UserName('test'),
        email=Email('fkgjd@example.com'),
        password=Password('test'),
    )
