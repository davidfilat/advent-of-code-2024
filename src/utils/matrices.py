from typing import Iterable, List

from cytoolz import compose


def transpose_2d_matrix(matrix: Iterable[List[int]]) -> Iterable[List[int]]:
    return list(map(list, zip(*matrix)))


def rotate_matrix(matrix: Iterable[List[int]]) -> Iterable[List[int]]:
    return transpose_2d_matrix(matrix[::-1])


def mirror_matrix(matrix: Iterable[List[int]]) -> Iterable[List[int]]:
    return list(map(compose(list, reversed), matrix))
