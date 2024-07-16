import bcrypt
import pytest

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
from domain.values.users import Email, Password, UserName


# TODO: User Faker


def test_user_name_validate_success():
    user_name = 'test'

    user_name_obj = UserName(user_name)

    assert user_name_obj.value == user_name


def test_user_name_validate_is_empty():
    user_name = ''

    with pytest.raises(UserNameIsEmptyException):
        user_name_obj = UserName(user_name)


def test_user_name_validate_is_too_long():
    user_name = 'test' * 100

    with pytest.raises(UserNameIsTooLongException):
        user_name_obj = UserName(user_name)


def test_user_name_validate_is_too_short():
    user_name = 't'

    with pytest.raises(UserNameIsTooShortException):
        user_name_obj = UserName(user_name)


def test_user_name_validate_is_not_alphanumeric():
    user_name = 'test*&!@'

    with pytest.raises(UserNameIsNotAlphanumericException):
        user_name_obj = UserName(user_name)


def test_user_email_validate_success():
    email = 'fkgjd@example.com'

    email_obj = Email(email)

    assert email_obj.value == email


def test_user_email_validate_is_empty():
    email = ''

    with pytest.raises(EmailIsEmptyException):
        email_obj = Email(email)


def test_user_email_validate_is_too_long():
    email = 'test' * 100 + '@test.com'

    with pytest.raises(EmailIsTooLongException):
        email_obj = Email(email)


def test_user_email_validate_is_not_valid():
    email = 'test'

    with pytest.raises(EmailIsNotValidException):
        email_obj = Email(email)


def test_user_password_validate_success():
    password = 'test'

    password_obj = Password(password)

    assert bcrypt.checkpw(password.encode('utf-8'), password_obj.value.encode('utf-8'))
