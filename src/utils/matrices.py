from typing import Iterable, Optional

from cytoolz import compose
from cytoolz.functoolz import curry


def transpose_2d_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return list(map(list, zip(*matrix)))


def rotate_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return transpose_2d_matrix(matrix[::-1])


def mirror_matrix(matrix: Iterable[list[int]]) -> Iterable[list[int]]:
    return list(map(compose(list, reversed), matrix))


@curry
def find_coordinates(matrix: list[list[str]], target: str) -> Optional[tuple[int, int]]:
    return next(
        (
            (row_index, col_index)
            for row_index, row in enumerate(matrix)
            for col_index, element in enumerate(row)
            if element == target
        ),
        None,
    )


def grid_to_string(matrix: list[list[any]]) -> str:
    return "\n".join("".join(row) for row in matrix)


def print_grid(grid: list[list[any]]) -> list[list[any]]:
    print("\n" + grid_to_string(grid) + "\n")
    return grid
