import re


class Hex:
    __FULL = re.compile(r"#?([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})$", re.I)
    __PARTIAL = re.compile(r"#?([0-9A-F])([0-9A-F])([0-9A-F])$", re.I)

    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    @classmethod
    def from_hexcode(cls, string):
        if match := cls.__FULL.match(string):
            r = int(match.group(1), 16)
            g = int(match.group(2), 16)
            b = int(match.group(3), 16)
            return cls(r, g, b)
        if match := cls.__PARTIAL.match(string):
            r = int(match.group(1) * 2, 16)
            g = int(match.group(2) * 2, 16)
            b = int(match.group(3) * 2, 16)
            return cls(r, g, b)
        raise ValueError("Not a valid color")

    @classmethod
    def from_hex_values(cls, r, g, b):
        r = round(r * 256)
        g = round(g * 256)
        b = round(b * 256)
        return cls(r, g, b)

    def __iter__(self):
        return iter((self.r, self.g, self.b))

    def __str__(self):
        return self.name.strip()

    @property
    def red(self):
        return self.r

    @property
    def blue(self):
        return self.b

    @property
    def green(self):
        return self.g

    @property
    def values(self):
        "Returns colors as floats between 0 and 1"
        return (self.r/256, self.g/256, self.b/256)

    @property
    def swatch(self):
        "Returns a terminal color swatch"
        start = f"\033[48;2;{self.r};{self.g};{self.b}m"
        end = "\033[0;5;0m"
        return f"{start}         {end}"

    @property
    def name(self):
        "Returns name - same length as the swatch"
        def p_hex(num):
            h = hex(num)[2:]
            if len(h) == 1:
                h = f"0{h}"
            return h.upper()
        return f" #{p_hex(self.r)}{p_hex(self.g)}{p_hex(self.b)} "
