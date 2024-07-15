from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self):
        return 'An application error has occurred'

    def __str__(self):
        return self.message
