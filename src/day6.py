# ruff: noqa: E731
import os
import sys
from copy import deepcopy
from enum import Enum
from multiprocessing import Pool
from typing import Optional

from cytoolz import (
    get,
    get_in,
    first,
    compose,
    count,
    unique,
    second,
    curry,
    juxt,
    pipe,
)
from cytoolz.curried import map, filter, drop
from toolz import identity

from utils.common import get_day_input, print_result
from utils.matrices import find_coordinates


class DIRECTION(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


T_GRID = list[list[str]]
T_COORDINATES = tuple[int, int]
T_PATH = list[tuple[DIRECTION, T_COORDINATES]]

DIRECTION_MAP = {
    DIRECTION.UP: (lambda x, y: (x - 1, y)),
    DIRECTION.DOWN: (lambda x, y: (x + 1, y)),
    DIRECTION.LEFT: (lambda x, y: (x, y - 1)),
    DIRECTION.RIGHT: (lambda x, y: (x, y + 1)),
}


def parse_lab_grid(text: str) -> T_GRID:
    lines = text.split("\n")
    return [list(line) for line in lines]


def find_start_position(grid: list[list[str]]) -> T_COORDINATES:
    guard_position_maker = "^"
    return find_coordinates(grid, guard_position_maker)


def get_next_direction(direction: DIRECTION) -> DIRECTION:
    return DIRECTION((direction.value % 4) + 1)


def get_next_direction_and_position(
    grid: T_GRID, current_position: T_COORDINATES, direction: DIRECTION
) -> tuple[DIRECTION, T_COORDINATES]:
    next_position = get(direction, DIRECTION_MAP)(*current_position)
    lab_item = "#"

    if get_in(next_position, grid) == lab_item:
        new_direction = get_next_direction(direction)
        return get_next_direction_and_position(grid, current_position, new_direction)

    return direction, next_position


def traverse_guard_path(grid: T_GRID, path: Optional[T_PATH] = None) -> T_PATH:
    if not path:
        guard_position = find_start_position(grid)
        if not guard_position:
            return []
        return traverse_guard_path(grid, [(DIRECTION.UP, guard_position)])

    direction, last_position = first(path)

    x, y = last_position

    if x not in range(len(grid)) or y not in range(len(grid[x])):
        return drop(1, path)

    new_direction, _ = new_step = get_next_direction_and_position(
        grid, last_position, direction
    )

    if new_step in path:
        if new_direction != get_next_direction(direction):
            return []
        raise RecursionError("Loop detected in the guard path")

    return traverse_guard_path(grid, [new_step, *path])


@curry
def add_block_in_grid(grid: T_GRID, block_position: T_COORDINATES) -> T_GRID:
    grid_copy = deepcopy(grid)
    x, y = block_position
    grid_copy[x][y] = "#"
    return grid_copy


def has_loop(grid: T_GRID) -> bool:
    try:
        traverse_guard_path(grid)
        return False
    except RecursionError:
        return True


@curry
def filter_with_multiprocessing(func, iterable, processes=os.cpu_count()):
    with Pool(processes=processes) as pool:
        return list(
            map(second, (filter(first, pool.map(juxt(func, identity), iterable))))
        )


traverse_initial_path = compose(
    unique,
    map(second),
    traverse_guard_path,
)

part_1 = compose(count, traverse_initial_path, parse_lab_grid)


def generate_all_coordinates(grid: T_GRID) -> list[T_COORDINATES]:
    width = len(grid[0])
    height = len(grid)
    return [(x, y) for x in range(width) for y in range(height)]


def part_2(text: str) -> int:
    grid = parse_lab_grid(text)
    all_coordinates = set(generate_all_coordinates(grid))
    initial_path = set(traverse_initial_path(grid))
    potential_new_block_coordinates = all_coordinates - initial_path
    return pipe(
        potential_new_block_coordinates,
        map(add_block_in_grid(grid)),
        filter_with_multiprocessing(has_loop),
        count,
    )


if __name__ == "__main__":
    sys.setrecursionlimit(
        10**6
    )  # Python enforces a recursion limit of 1000. We need it to be higher that the path length.
    text = get_day_input(6)
    print(len(text) * len(text[0]))
    print_result(1, part_1(text))
    print_result(2, part_2(text))
