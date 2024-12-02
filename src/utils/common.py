from pathlib import Path
from pprint import pprint
from typing import Any, TypeVar


def get_day_input(day: int):
    resources_path = Path(__file__).resolve().parents[2] / "resources"
    file = resources_path / f"day{day}.txt"
    with file.open("r") as f:
        return f.read().strip()


def print_result(part: int, result: Any) -> None:
    print(f"Part {part}: {result}")


def parse_int_input(file: str) -> list[list[int]]:
    return [[int(n) for n in line.split()] for line in file.split("\n")]


T = TypeVar("T")


def do_print(x: T) -> T:
    pprint(x)
    return x
