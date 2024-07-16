import asyncio
from dataclasses import dataclass, field

from domain.entities.users import User
from infra.repositories.users.base import BaseUserRepository


@dataclass
class MemoryUserRepository(BaseUserRepository):

    _users: list[User] = field(default_factory=list, kw_only=True)

    async def update_user(self, user: User) -> None:
        self._users = [u if u.oid != user.oid else user for u in self._users]

    async def delete_user(self, user_oid: str) -> None:
        self._users = [user for user in self._users if user.oid != user_oid]

    async def get_user_by_oid(self, user_oid: str) -> User:
        return next((user for user in self._users if user.oid == user_oid), None)

    async def register_user(self, user: User) -> None:
        self._users.append(user)

    async def _check_exists_by_username(self, username: str) -> bool:
        try:
            return bool(next(
                user for user in self._users if user.username.as_generic_type() == username
            ))
        except StopIteration:
            return False

    async def _check_exists_by_email(self, email: str) -> bool:
        try:
            return bool(next(
                user for user in self._users if user.email.as_generic_type() == email
            ))
        except StopIteration:
            return False
