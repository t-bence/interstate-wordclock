"""
This code is used to get Python data from the C++ source.
These numbers are the C++ data taken over as-is.

What I need to do is, write code to convert these numbers into
X-Y coordinates for the Python lib.
These coordinates start from the second to bottom row on the left,
so under "TÍZ", and are arranged in as a "snake". 

Tasks:
- figure out how the lib needs the coordinates
- write tests
- write code to convert the numbers into X-Y coordinates

The lib needs coordinates like this. This is the tuple that Strip.to_pixels returns.
display.rectangle(x, y, w, h)
x - the destination X coordinate
y - the destination Y coordinate
w - the width
h - the height

https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics#rectangle

"""

from dataclasses import dataclass

MOST = (105, 4)
ORA = (30, 3)
VAN = (14, 3)
MULT = (18, 4)
OT_MULT = (11, 2)  # a lent szereplo ot, tehat az ot perccel mult
TIZ_MULT = (0, 3)  # a lent szereplo tiz, a tiz perccel mult
OT_MULVA = (102, 2)  # a fent szereplo ot, tehat az ot perc mulva
TIZ_MULVA = (100, 3)  # a fent szereplo tiz; tiz perc mulva
PERC = (84, 4)
PERCCEL = (4, 7)
NEGYED = (93, 6)
MULVA = (78, 5)
FEL = (66, 3)
HAROMNEGYED = (88, 11)

HOURS = [
    (56, 10),    # TIZENKETTO, which is 0...
    (49, 3),     # EGY
    (56, 5),     # 2
    (37, 5),     # 3
    (25, 4),     # 4
    (35, 2),     # 5
    (22, 3),     # 6
    (52, 3),     # 7
    (44, 5),     # 8
    (70, 6),     # 9
    (33, 3),     # 10
    (61, 5),     # 11 (first part), TIZEN
    (49, 3)      # 11 (second part), EGY
]

@dataclass
class Strip:
    """A strip of a word"""
    x: int = 0
    y: int = 0
    length: int = 1
    
    def to_pixels(self, letter_width: int = 3) -> tuple[int, int, int, int]:
        """Return x, y, width, height of rectangle to display."""
        return (self.x * letter_width, self.y * letter_width,
            self.length * letter_width, letter_width)


def converter(input: tuple[int, int]) -> Strip:
    start, length = input
    letters_per_row = 11
    row = start // letters_per_row
    rem = start % letters_per_row

    y = letters_per_row - 2 - row

    if y % 2 == 0:
        x = letters_per_row - rem - length
    else:
        x = rem

    return Strip(x, y, length)


if __name__ == "__main__":
    assert Strip(0, 9, 3) == converter(TIZ_MULT)
    assert Strip(1, 0, 4) == converter(MOST)
    assert Strip(0, 1, 11) == converter(HAROMNEGYED)
    assert Strip(4, 9, 7) == converter(PERCCEL)
    assert Strip(0, 8, 4) == converter(MULT)

    assert (3, 0, 12, 3) == converter(MOST).to_pixels(3)

    import json
    print(
        json.dumps(
            [converter(h).to_pixels(3) for h in HOURS], indent=4
        )
    )
