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

if __name__ == "__main__":
    # some simple test cases
    assert "dcab" == invert_rows("abcd", letters_per_row=2)
    assert "efdcab" == invert_rows("abcdef", letters_per_row=2)

    characters = invert_rows(letters, 11)
    print(characters)
    print(len(characters))
