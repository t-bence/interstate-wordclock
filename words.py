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
"""

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
