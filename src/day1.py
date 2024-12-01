from collections import Counter
from operator import sub, mul
from typing import Callable

from cytoolz import juxt, first, second, compose, identity
from cytoolz.curried import compose_left, map, get
from toolz import pipe

from utils.common import get_day_input, print_result
from utils.functools import apply
from utils.matrices import transpose_2d_matrix


def parse_input(file: str) -> list[list[int]]:
    return [[int(n) for n in line.split()] for line in file.split("\n")]


part_1 = compose_left(
    compose(map(sorted), transpose_2d_matrix),  # Sort columns
    apply(map(compose(abs, sub))),  # Calculate distance between elements in columns
    sum,
)


def similarity_calculator(right_list: list[int]) -> Callable[[int], tuple[int, int]]:
    int_counter = Counter(right_list)
    return juxt(identity, get(seq=int_counter, default=0))


part_2 = compose_left(
    transpose_2d_matrix,
    compose(list, reversed),
    juxt(  # Initialize calculator with right column and prepare left column list
        compose(similarity_calculator, first),
        second,
    ),
    apply(map),  # Apply calculator and the list with left column to map
    map(apply(mul)),  # Multiply the numbers and their respective scores
    sum,
)

if __name__ == "__main__":
    table = pipe("1", get_day_input, parse_input)

    print_result(1, part_1(table))
    print_result(2, part_2(table))
