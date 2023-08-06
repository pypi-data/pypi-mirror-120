"Utilities to create various ranges"


def step_range(start, stop, steps):
    "Produces a range of steps as per the parameter steps"
    step = (stop - start)/(steps - 1)
    return [(start + step * i) for i in range(steps)]


def int_range(start, stop, steps):
    "Same as step_range but only returns integers"
    return [int(i) for i in step_range(start, stop, steps)]


def inc_loop_range(start, stop, steps, max_=1):
    "Produces a range in the increasing (clockwise) direction modulus max_"
    if stop < start:
        stop += max_
    step = (stop - start)/(steps - 1)
    return [(start + step * i) % max_ for i in range(steps)]


def dec_loop_range(start, stop, steps, max_=1):
    "Produces a range in the decreasing (anticlockwise) direction modulus max_"
    if start < stop:
        start += max_
    step = (stop - start)/(steps - 1)
    return [(start + step * i) % max_ for i in range(steps)]
