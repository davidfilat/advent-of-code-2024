from typing import Iterable, List


def transpose_2d_matrix(matrix: Iterable[List[int]]) -> Iterable[List[int]]:
    return list(map(list, zip(*matrix)))
