"Main Module to bring it all together"

import click

from .hex import Hex
from . import gradients as g


@click.command()
@click.argument("start", type=Hex.from_hexcode)
@click.argument("end", type=Hex.from_hexcode)
@click.argument("steps", type=int, required=False, default=5)
def main(start, end, steps):
    "Generates a gradient from START to END STEPS long (ends inclusive)"

    mid = f"<--- {steps} Steps Gradient --->"
    print(start.swatch, " " * len(mid), end.swatch)
    print(start.name, mid, end.name)
    print()

    rgb = g.rgb_gradients(start, end, steps)
    hls = g.hls_gradients(start, end, steps)
    hsv = g.hsv_gradients(start, end, steps)

    bold = "\033[1m"
    reset = "\033[0m"

    print(f"{bold}RGB Gradients{reset}")
    print(*(i.swatch for i in rgb[0]))
    print(*(i.name for i in rgb[0]))
    print()

    print(f"{bold}HLS Gradients{reset}")
    print("Clockwise")
    print(*(i.swatch for i in hls[0]))
    print(*(i.name for i in hls[0]))
    print("Anti-lockwise")
    print(*(i.swatch for i in hls[1]))
    print(*(i.name for i in hls[1]))
    print()

    print(f"{bold}HSV Gradients{reset}")
    print("Clockwise")
    print(*(i.swatch for i in hsv[0]))
    print(*(i.name for i in hsv[0]))
    print("Anti-lockwise")
    print(*(i.swatch for i in hsv[1]))
    print(*(i.name for i in hsv[1]))


if __name__ == "__main__":
    main()
