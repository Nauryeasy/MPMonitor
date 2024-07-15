from dataclasses import dataclass
from typing import Type

from domain.events.base import BaseEvent
from domain.values.users import BaseUserValueObject


@dataclass
class NewUserRegisteredEvent(BaseEvent):
    user_oid: str
    user_username: str
    user_first_name: str
    user_last_name: str
    user_email: str
    user_password: str


@dataclass
class UserUpdatedEvent(BaseEvent):
    user_oid: str
    change_type: Type[BaseUserValueObject]
    old_value: str
    new_value: str
