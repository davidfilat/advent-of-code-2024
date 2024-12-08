from typing import Iterable, List, Optional

from cytoolz import compose
from cytoolz.functoolz import curry


def transpose_2d_matrix(matrix: List[List[int]]) -> List[List[int]]:
    return list(map(list, zip(*matrix)))


def rotate_matrix(matrix: List[List[int]]) -> List[List[int]]:
    return transpose_2d_matrix(matrix[::-1])


def mirror_matrix(matrix: Iterable[List[int]]) -> Iterable[List[int]]:
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
