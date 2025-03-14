"""
This is just same nasty code to reverse engineer the character layout from the string I could find.
"""

letters_per_row = 11

letters = "TIZUPERCCELTOONAVPTLUMHATNEGYKORAZITOMORAHIWNYOLCEGYHETUOTTEKNEZITFELGKILENCSOAVLUMACREPHAROMNEGYEDCZITOLTSOMB"

def invert_rows(letter_string: str, letters_per_row=11):
    """Reverses rows in a given string"""
    row_count = len(letter_string) // letters_per_row

    rows = [letter_string[r*letters_per_row:(r+1)*letters_per_row]
            for r in range(row_count)]

    result = ""
 
    for index, row in enumerate(rows):
        if index % 2 == 1:
            result = row[::-1] + result
        else:
            result = row + result

    return result

import unittest

class TestInvertRows(unittest.TestCase):
    #def test_single_row(self):
    #    self.assertEqual(invert_rows("abcdefghijklmnopqrstuvwxyz"), "abcdefghijklmnopqrstuvwxyz")

    def test_two_rows(self):
        self.assertEqual(
            invert_rows("abcd", letters_per_row=2),
            "abdc"
        )

    def test_three_rows(self):
        self.assertEqual(
            invert_rows('abcdef', letters_per_row=2),
            "abdcef"
        )

if __name__ == "__main__":
    #unittest.main()

    characters = invert_rows(letters, 11)
    print(characters)
    print(len(characters))
