from pathlib import Path
from typing import Any


def get_day_input(day: int):
    resources_path = Path(__file__).resolve().parents[2] / "resources"
    file = resources_path / f"day{day}.txt"
    with file.open("r") as f:
        return f.read().strip()


def print_result(part: int, result: Any) -> None:
    print(f"Part {part}: {result}")
