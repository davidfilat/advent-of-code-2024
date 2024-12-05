import re
from itertools import product

from cytoolz import compose, concat, pipe, count
from cytoolz.curried import iterate, juxt, map, mapcat, take, get_in, filter
from more_itertools import flatten
from toolz import identity, curry

from utils.common import get_day_input, print_result
from utils.matrices import rotate_matrix


def diagonals_to_rows(matrix: list[str]) -> list[str]:
    num_rows = len(matrix)
    num_cols = len(matrix[0]) if num_rows > 0 else 0

    def get_diagonal(start_row, start_col):
        return "".join(
            matrix[r][c]
            for r, c in zip(range(start_row, num_rows), range(start_col, num_cols))
        )

    diagonals_from_cols = reversed(
        list(map(lambda col: get_diagonal(0, col), range(num_cols)))
    )
    diagonals_from_rows = map(lambda row: get_diagonal(row, 0), range(1, num_rows))

    return list(concat([diagonals_from_cols, diagonals_from_rows]))


def find_all_xmas_instances(line: str):
    pattern = r"XMAS"
    return len(re.findall(pattern, line))


part_1 = compose(
    sum,
    map(find_all_xmas_instances),
    flatten,
    mapcat(
        juxt(map("".join), diagonals_to_rows)
    ),  # Append the diagonals of each version and transforms rows to strings
    take(4),  # Generate all rotated versions of the matrix
    iterate(rotate_matrix),
)


@curry
def is_valid_x_mas(matrix: list[str], center_coords: tuple[int, int]) -> bool:
    def get_in_matrix(x: int, y: int) -> str:
        return get_in((x, y), matrix)

    center = get_in_matrix(*center_coords)

    x1, y1 = center_coords
    top_right, top_left, bottom_right, bottom_left = corners = [
        get_in_matrix(x1 - 1, y1 - 1),
        get_in_matrix(x1 - 1, y1 + 1),
        get_in_matrix(x1 + 1, y1 - 1),
        get_in_matrix(x1 + 1, y1 + 1),
    ]

    return (
        center == "A"
        and all([c in ("S", "M") for c in corners])
        and bottom_left != top_right
        and bottom_right != top_left
    )


def find_x_mas_count(matrix: list[str]) -> int:
    is_valid_x_mas_check = is_valid_x_mas(matrix)
    x_range, y_range = (range(len(matrix))[1:-1], range(len(matrix[0]))[1:-1])

    return pipe(
        product(x_range, y_range), map(is_valid_x_mas_check), filter(identity), count
    )


part_2 = find_x_mas_count

if __name__ == "__main__":
    matrix = get_day_input(4).split("\n")
    print_result(1, part_1(matrix))
    print_result(2, part_2(matrix))
