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
        if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            res.append("_")
            res.append(c.lower())
        else:
            res.append(c)

    return "".join(res)


def generate_human_hw11() -> Human_hw11:
    name = change_case(f"{faker.first_name()}{faker.last_name()}")
    # faker - turn maximal level :)
    password = faker.password(length=32, special_chars=True, digits=True, upper_case=True, lower_case=True)
    email = f"{name}@{faker.email().split('@')[1]}"
    return Human_hw11(
        name=name,
        password=password,
        email=email,
    )


def check_unique(value, unique_values_list):
    return value not in unique_values_list


def generate_humans_hw11(amount: int) -> Iterator[Human_hw11]:
    unique_value_list = set()
    count_range = 0
    while count_range < amount:
        unique_value_list.add(generate_human_hw11().name)
        next_human = generate_human_hw11()
        if check_unique(next_human.name, unique_value_list):
            count_range += 1
            yield next_human
