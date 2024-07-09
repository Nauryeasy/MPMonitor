from dataclasses import dataclass
import bcrypt

from domain.entities.base import BaseEntity
from domain.values.base import Id

from domain.values.users import Email, Password, UserName

# TODO: add tests
# TODO: Add User logic methods


@dataclass(eq=False)
class User(BaseEntity):
    username: UserName
    first_name: UserName
    last_name: UserName
    email: Email
    password: Password

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.value.encode('utf-8'))


if __name__ == '__main__':
    user = User(
        id=Id(1),
        username=UserName('test'),
        first_name=UserName('test'),
        last_name=UserName('test'),
        email=Email('fkgjd@example.com'),
        password=Password('test'),
    )
