from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class UserNameIsEmptyException(ApplicationException):

    @property
    def message(self):
        return 'User name cannot be empty'


@dataclass(eq=False)
class UserNameIsTooShortException(ApplicationException):
    user_name: str

    @property
    def message(self):
        return f'User name must be at least 3 characters long "{self.user_name}"'


@dataclass(eq=False)
class UserNameIsTooLongException(ApplicationException):
    user_name: str

    @property
    def message(self):
        return f'User name must be at most 50 characters long "{self.user_name[:50]}..."'


@dataclass(eq=False)
class UserNameIsNotAlphanumericException(ApplicationException):
    user_name: str

    @property
    def message(self):
        return f'User name must only contain letters and numbers "{self.user_name}"'


@dataclass(eq=False)
class EmailIsEmptyException(ApplicationException):

    @property
    def message(self):
        return 'Email cannot be empty'


@dataclass(eq=False)
class EmailIsTooLongException(ApplicationException):
    email: str

    @property
    def message(self):
        return f'Email must be at most 50 characters long "{self.email[:50]}..."'


@dataclass(eq=False)
class EmailIsNotValidException(ApplicationException):
    email: str

    @property
    def message(self):
        return f'Email is not valid "{self.email}"'


@dataclass(eq=False)
class PasswordIsEmptyException(ApplicationException):

    @property
    def message(self):
        return 'Password cannot be empty'


@dataclass(eq=False)
class TypeIsNotValidException(ApplicationException):
    gotten_type: str
    expected_type: str

    @property
    def message(self):
        return f'Type is not valid. Was gotten "{self.gotten_type}" expected "{self.expected_type}"'
