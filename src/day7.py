import operator
from functools import lru_cache
from itertools import product
from typing import Callable, cast

from cytoolz import compose, curry, first
from cytoolz.curried import filter, get, map
from cytoolz.itertoolz import interleave

from utils.common import get_day_input, print_result
from utils.functools import apply

T_OPERATION = Callable[[int, int], int]
T_COMBINATION = list[int | T_OPERATION]


def parse_input(raw: str) -> list[tuple[int, list[int]]]:
    return [
        (int(result.strip()), list(map(int, values.strip().split(" "))))
        for row in raw.strip().split("\n")
        if ":" in row
        for result, values in [row.strip().split(":", 1)]
    ]


def concatenate(*args: int) -> int:
    return int("".join(map(str, args)))


PRECEDENCE = {operator.add: 1, operator.mul: 2, concatenate: 3}


def generate_possible_operations_order(
    operations: list[T_OPERATION],
    n: int,
) -> list[list[T_OPERATION]]:
    return map(
        list,
        product(
            operations,
            repeat=n - 1,
        ),
    )


def generate_all_list_with_operation_combinations(
    numbers: list[int], operations: list[T_OPERATION]
) -> list[T_COMBINATION]:
    operators_combinations = generate_possible_operations_order(
        operations, len(numbers)
    )

    return [
        list(interleave([numbers, operators])) for operators in operators_combinations
    ]


@lru_cache(maxsize=None)
def apply_operation(op: T_OPERATION, a: int, b: int) -> int:
    return op(a, b)


def apply_operations_without_precedence(combination: T_COMBINATION) -> int:
    if len(combination) == 1:
        return first(combination)

    a, op, b, *rest = combination
    return apply_operations_without_precedence(
        cast(T_COMBINATION, [apply_operation(op, a, b), *rest])
    )


def apply_operations_with_precedence(combination: T_COMBINATION) -> int:
    def apply_max_operator(equation: T_COMBINATION) -> int:
        max_operator = first(
            sorted(equation, key=lambda x: get(x, PRECEDENCE, 0), reverse=True)
        )

        if not callable(max_operator):
            return max_operator

        idx = equation.index(max_operator)
        result = max_operator(equation[idx - 1], equation[idx + 1])
        return apply_max_operator(equation[: idx - 1] + [result] + equation[idx + 2 :])

    return apply_max_operator(combination)


@curry
def is_equation_valid(
    method: Callable[[T_COMBINATION], int],
    operations: list[T_OPERATION],
    result: int,
    numbers: list[int],
) -> int:
    all_combinations = generate_all_list_with_operation_combinations(
        numbers, operations
    )

    def is_combination_valid(
        combination: T_COMBINATION,
    ) -> bool:
        return method(combination) == result

    return next(
        (
            result
            for combination in all_combinations
            if is_combination_valid(combination)
        ),
        None,
    )


part_1 = compose(
    sum,
    map(first),
    filter(
        apply(
            is_equation_valid(
                apply_operations_without_precedence,
                [
                    operator.add,
                    operator.mul,
                ],
            )
        )
    ),
    parse_input,
)

part_2 = compose(
    sum,
    map(first),
    filter(
        apply(
            is_equation_valid(
                apply_operations_without_precedence,
                [operator.add, operator.mul, concatenate],
            )
        )
    ),
    parse_input,
)


if __name__ == "__main__":
    text = get_day_input(7)
    print_result(1, part_1(text))
    print_result(2, part_2(text))
