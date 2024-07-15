from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Self
from uuid import uuid4

from domain.events.base import BaseEvent


@dataclass
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    _events: list[BaseEvent] = field(
        default_factory=list,
        kw_only=True,
    )

    # Злые датаклассы :(
    # Там не передаются дефолт значения, когда-нибудь разберусь почему, но не сейчас

    #TODO: Understand why after overriding annotations the default values do not get into the child class

    # def __init_subclass__(cls, **kwargs):
    #     super().__init_subclass__(**kwargs)
    #     cls_annotations = getattr(cls, '__annotations__', {})
    #     base_annotations = {}
    #
    #     for base in cls.__bases__:
    #         base_annotations.update(getattr(base, '__annotations__', {}))
    #
    #     cls_annotations.update(base_annotations)
    #     print(cls_annotations)
    #     cls.__annotations__ = cls_annotations

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: Self) -> bool:
        if not isinstance(__value, type(self)):
            return False
        return self.oid == __value.oid

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        events = copy(self._events)
        self._events.clear()

        return events
