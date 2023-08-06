"Generate the gradients"

import colorsys as cs

from . import utils as u
from .hex import Hex


def rgb_gradients(start, end, steps):
    "RGB gradient between start and end"
    r = u.int_range(start.r, end.r, steps)
    g = u.int_range(start.g, end.g, steps)
    b = u.int_range(start.b, end.b, steps)
    gradient = [Hex(*i) for i in zip(r, g, b)]
    return [gradient]


def _hx_gradients(start, end, steps, from_rgb, to_rgb, max_=1):
    "Generic Hue * * function"
    start_hx = from_rgb(*start.values)
    end_hx = from_rgb(*end.values)
    hue_clock = u.inc_loop_range(start_hx[0], end_hx[0], steps, max_)
    hue_anti = u.dec_loop_range(start_hx[0], end_hx[0], steps, max_)
    x1 = u.step_range(start_hx[1], end_hx[1], steps)
    x2 = u.step_range(start_hx[2], end_hx[2], steps)
    return [
        [Hex.from_hex_values(*to_rgb(*i)) for i in zip(hue_clock, x1, x2)],
        [Hex.from_hex_values(*to_rgb(*i)) for i in zip(hue_anti, x1, x2)]
    ]


def hls_gradients(start, end, steps):
    "Hue, Lighting, Saturation based gradients"
    return _hx_gradients(start, end, steps, from_rgb=cs.rgb_to_hls,
                         to_rgb=cs.hls_to_rgb)


def hsv_gradients(start, end, steps):
    "Hue Saturation Value based gradients"
    return _hx_gradients(start, end, steps, from_rgb=cs.rgb_to_hsv,
                         to_rgb=cs.hsv_to_rgb)
