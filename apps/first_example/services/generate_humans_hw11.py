from collections.abc import Iterator
from typing import NamedTuple

from faker import Faker

faker = Faker()


class Human_hw11(NamedTuple):
    name: str
    password: str
    email: str

    def __str__(self):
        return f"{self.name} ({self.email})"


def change_case(str):
    res = [str[0].lower()]
    for c in str[1:]:
        if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ."):
            res.append("_")
            res.append(c.lower())
        else:
            res.append(c)

    return "".join(res)


def generate_human_hw11() -> Human_hw11:
    name = change_case(faker.name())
    # faker - turn maximal level :)
    password = faker.password(length=32, special_chars=True, digits=True, upper_case=True, lower_case=True)
    email = f"{name}@{faker.email().split('@')[1]}"
    return Human_hw11(
        name=name,
        password=password,
        email=email,
    )


def generate_humans_hw11(amount: int) -> Iterator[Human_hw11]:
    for _ in range(amount):
        yield generate_human_hw11()
