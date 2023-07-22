from collections.abc import Iterator
from typing import NamedTuple

from faker import Faker

faker = Faker()


class User(NamedTuple):
    username: str
    email: str

    def get_dict(self) -> dict:
        return self._asdict()

    @classmethod
    def get_fieldnames(cls) -> list[str]:
        return list(cls._fields)

    @classmethod
    def from_raw_dict(cls, raw_data: dict) -> "User":
        return cls(
            username=raw_data["username"],
            email=raw_data["email"],
        )


def generate_user() -> User:
    return User(
        username=faker.first_name(),
        email=faker.email(),
    )


def generate_list_of_users(amount: int = 100) -> Iterator[User]:
    for _ in range(1, amount + 1):
        yield generate_user()


def generate_string_list_of_users(users, type_of_list="ol"):
    formatted_list = []
    for user in users:
        formatted_user = f"<li> Name: <b>{user.username}</b> - <span>email:{user.email}</span></li>"
        formatted_list.append(formatted_user)
    _temp_line = "\n".join(formatted_list)
    return f"<{type_of_list}>{_temp_line}</{type_of_list}>"
