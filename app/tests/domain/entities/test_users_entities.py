from datetime import datetime
import pytest

from domain.entities.users import User
from domain.events.users import NewUserRegisteredEvent, UserUpdatedEvent
from domain.exceptions.users import TypeIsNotValidException
from domain.values.users import Email, Password, UserName, BaseUserValueObject


def test_user_create_success():
    user_name = UserName('test')
    first_name = UserName('test')
    last_name = UserName('test')
    email = Email('fkgjd@example.com')
    password = Password('test')

    user = User(
        username=user_name,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    assert user.username == user_name
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == email
    assert user.created_at.date() == datetime.today().date()


def test_user_check_password_success():
    user = User(
        username=UserName('test'),
        first_name=UserName('test'),
        last_name=UserName('test'),
        email=Email('fkgjd@example.com'),
        password=Password('test'),
    )

    assert user.check_password('test')


def test_user_check_password_fail():
    user = User(
        username=UserName('test'),
        first_name=UserName('test'),
        last_name=UserName('test'),
        email=Email('fkgjd@example.com'),
        password=Password('test'),
    )
    assert not user.check_password('test2')


def test_new_user_register_success():
    user = User(
        username=UserName('test'),
        first_name=UserName('test'),
        last_name=UserName('test'),
        email=Email('fkgjd@example.com'),
        password=Password('test'),
    )

    user.register_new_user()

    events = user.pull_events()
    pulled_events = user.pull_events()

    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewUserRegisteredEvent)
    assert new_event.user_oid == user.oid
    assert new_event.user_username == user.username.as_generic_type()
    assert new_event.user_first_name == user.first_name.as_generic_type()
    assert new_event.user_last_name == user.last_name.as_generic_type()
    assert new_event.user_email == user.email.as_generic_type()
    assert new_event.user_password == user.password.as_generic_type()


def test_user_update_success():
    user = User(
        username=UserName('test'),
        first_name=UserName('test'),
        last_name=UserName('test'),
        email=Email('fkgjd@example.com'),
        password=Password('test'),
    )

    new_user_name = UserName('test2')
    new_first_name = UserName('test2')
    new_last_name = UserName('test2')
    new_email = Email('fkgjd@example.com')
    new_password = Password('test2')

    user.username = new_user_name
    user.first_name = new_first_name
    user.last_name = new_last_name
    user.email = new_email
    user.password = new_password

    assert user.username.as_generic_type() == new_user_name.as_generic_type()
    assert user.first_name.as_generic_type() == new_first_name.as_generic_type()
    assert user.last_name.as_generic_type() == new_last_name.as_generic_type()
    assert user.email.as_generic_type() == new_email.as_generic_type()
    assert user.password.as_generic_type() == new_password.as_generic_type()

    events = user.pull_events()
    pulled_events = user.pull_events()

    assert not pulled_events, pulled_events
    for event in events:
        assert isinstance(event, UserUpdatedEvent), type(event)
        assert issubclass(event.change_type, BaseUserValueObject), event.change_type


def test_user_update_with_primitives_success():
    user = User(
        username=UserName('test'),
        first_name=UserName('test'),
        last_name=UserName('test'),
        email=Email('fkgjd@example.com'),
        password=Password('test'),
    )

    new_user_name = 'test2'
    new_first_name = 'test2'
    new_last_name = 'test2'
    new_email = 'fkgjd@example.com'
    new_password = 'test2'

    user.username = new_user_name
    user.first_name = new_first_name
    user.last_name = new_last_name
    user.email = new_email
    user.password = new_password

    assert user.username.as_generic_type() == new_user_name
    assert user.first_name.as_generic_type() == new_first_name
    assert user.last_name.as_generic_type() == new_last_name
    assert user.email.as_generic_type() == new_email
    assert user.check_password(new_password)

    events = user.pull_events()
    pulled_events = user.pull_events()

    assert not pulled_events, pulled_events
    for event in events:
        assert isinstance(event, UserUpdatedEvent), type(event)
        assert issubclass(event.change_type, BaseUserValueObject), event.change_type


def test_user_update_type_is_invalid_fail():
    user = User(
        username=UserName('test'),
        first_name=UserName('test'),
        last_name=UserName('test'),
        email=Email('fkgjd@example.com'),
        password=Password('test'),
    )

    new_user_name = 1

    with pytest.raises(TypeIsNotValidException):
        user.username = new_user_name
