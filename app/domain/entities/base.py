from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

from domain.values.base import Id


@dataclass
class BaseEntity(ABC):
    id: Id
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: Self) -> bool:
        if not isinstance(__value, type(self)):
            return False
        return self.id == __value.id


if __name__ == '__main__':
    base_id = Id(1)
    print(BaseEntity(base_id))
