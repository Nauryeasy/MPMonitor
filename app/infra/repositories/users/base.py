from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from domain.entities.users import User


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def get_user_by_oid(self, user_oid: str) -> User:
        ...

    @abstractmethod
    async def register_user(self, user: User) -> None:
        ...

    @abstractmethod
    async def update_user(self, user: User) -> None:
        ...

    @abstractmethod
    async def delete_user(self, user: User) -> None:
        ...

    @abstractmethod
    async def _check_exists_by_username(self, username: str) -> bool:
        ...

    @abstractmethod
    async def _check_exists_by_email(self, email: str) -> bool:
        ...

    async def check_unique(self, username: str, email: str) -> bool:
        return not await self._check_exists_by_username(username) and not await self._check_exists_by_email(email)
