from functools import partial
from math import copysign
from operator import eq, ge, ne, sub

from cytoolz import (
    compose,
    compose_left,
    count,
    flip,
    identity,
    juxt,
    pipe,
)
from cytoolz.curried import cons, filter, map, sliding_window

from utils.common import get_day_input, parse_int_input, print_result
from utils.functools import apply
from utils.itertools import drop_nth

is_trend_moving_correctly = compose(
    all,
    map(all),  # Both conditions must be true
    map(
        juxt(partial(ne, 0), partial(ge, 3))
    ),  # Difference between the steps must be non-zero and between 1 and 3 steps
    map(abs),  # Calculate absolute difference
    map(apply(sub)),  # Calculate the difference between consecutive steps
    sliding_window(2),
)


is_trend_moving_in_the_same_direction = compose(
    all,
    map(apply(eq)),  # Signs must be equal
    sliding_window(2),  # Pair the sings of consecutive steps
    map(partial(copysign, 1)),  # Get the sign of the direction of the trend
    map(apply(sub)),
    sliding_window(2),
)

is_safe_report = compose(
    all,
    juxt(is_trend_moving_correctly, is_trend_moving_in_the_same_direction),
)

part_1 = compose_left(
    map(is_safe_report),
    filter(identity),
    count,
)


generate_all_drops = compose(apply(map), juxt(flip(drop_nth), compose(range, count)))

is_safe_with_tolerance = compose(
    any,
    map(is_safe_report),
    apply(cons),
    juxt(identity, generate_all_drops),
)


part_2 = compose_left(
    map(is_safe_with_tolerance),
    filter(identity),
    count,
)

if __name__ == "__main__":
    table = pipe("2", get_day_input, parse_int_input)
    print_result(1, part_1(table))
    print_result(2, part_2(table))
