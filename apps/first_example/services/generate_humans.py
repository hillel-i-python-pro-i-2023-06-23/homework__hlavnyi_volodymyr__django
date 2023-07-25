from collections.abc import Iterator
from typing import NamedTuple

from faker import Faker

faker = Faker()


class Human(NamedTuple):
    name: str
    password: str
    email: str
    age: int = 18

    def __str__(self):
        return f"{self.name} ({self.age})"


def generate_human() -> Human:
    return Human(
        name=faker.first_name(),
        password=faker.password(),
        email=faker.email(),
        age=faker.pyint(min_value=18, max_value=100),
    )


def generate_humans(amount: int) -> Iterator[Human]:
    for _ in range(amount):
        yield generate_human()
