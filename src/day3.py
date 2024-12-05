import re
from dataclasses import dataclass, field
from functools import partial, reduce
from operator import mul
from typing import cast

from cytoolz import compose, first, flip, pipe
from cytoolz.curried import cons, map

from utils.common import get_day_input, print_result
from utils.functools import apply

TCOMMAND = tuple[str, str]


@dataclass
class ExecutionState:
    condition: str = "do"
    results: list[int] = field(default_factory=list)


def find_valid_operations(text: str) -> list[TCOMMAND]:
    pattern = r"mul\((\d+),(\d+)\)"
    return re.findall(pattern, text)


part_1 = compose(sum, map(apply(mul)), map(map(int)), find_valid_operations)


def find_operation_with_conditions(text: str) -> list[TCOMMAND]:
    pattern = r"(mul|do|don't)\((\d*),?(\d*)\)"
    matches = re.finditer(pattern, text)
    return [cast(TCOMMAND, match.groups()) for match in matches]


def should_execute(current_state: ExecutionState, operation: str):
    return operation if operation in ("do", "don't") else current_state.condition


def apply_operation(condition: str, command: TCOMMAND):
    operation, *args = command
    if condition == "do" and operation == "mul":
        return pipe(args, map(int), apply(mul))


def apply_commands(current_state: ExecutionState, command: TCOMMAND):
    condition = should_execute(current_state, first(command))
    result = apply_operation(condition, command)
    return ExecutionState(
        condition=condition,
        results=(
            cons(result, current_state.results)
            if result is not None
            else current_state.results
        ),
    )


part_2 = compose(
    sum,
    partial(flip(getattr), "results"),
    lambda commands: reduce(apply_commands, commands, ExecutionState()),
    find_operation_with_conditions,
)
if __name__ == "__main__":
    table = get_day_input(3)
    print_result(1, part_1(table))
    print_result(2, part_2(table))
