class WallTime:
    """Represents the current wall clock time."""

    def __init__(self, hour: int, minute: int):
        self.hour = hour
        self.minute = minute


class Word:
    def __init__(self, x: int, y: int, length: int):
        """
        Initialize a Word with its display coordinates and length

        Args:
            x (int): X coordinate on the display
            y (int): Y coordinate on the display
            length (int): Number of characters in the word
        """
        self.x = x
        self.y = y
        self.length = length
        self.period = 3  # global lettering period


class WordClock:
    """Word clock that displays time in natural language."""

    # Define constants for the clock
    PERIOD = 3  # lettering period: one letter's width plus a border

    # Time words in natural language
    TIME_WORDS = [
        "MOST ORA VAN",  # 00
        "ORA MULT OT_MULT PERCCEL",  # 05
        "ORA MULT TIZ_MULT PERCCEL",  # 10
        "MOST NEGYED VAN",  # 15
        "NEGYED MULT OT_MULT PERCCEL",  # 20
        "OT_MULVA PERC MULVA FEL",  # 25
        "MOST FEL VAN",  # 30
        "FEL MULT OT_MULT PERCCEL",  # 35
        "FEL MULT TIZ_MULT PERCCEL",  # 40
        "MOST HAROMNEGYED VAN",  # 45
        "TIZ_MULVA PERC MULVA ORA",  # 50
        "OT_MULVA PERC MULVA ORA",  # 55
    ]

    # Define the hour words
    HOURS = [
        Word(0, 12, 10),  # TIZENKETTO
        Word(15, 15, 3),  # EGY
        Word(15, 12, 5),  # KETTO
        Word(6, 18, 5),  # HAROM
        Word(9, 21, 4),  # NEGY
        Word(21, 18, 2),  # OT
        Word(0, 21, 3),  # HAT
        Word(24, 15, 3),  # HET
        Word(0, 15, 5),  # NYOLC
        Word(12, 9, 6),  # KILENC
        Word(24, 18, 3),  # TIZ
        Word(0, 12, 5),  # TIZEN
    ]

    # Define the positions for all words
    WORD_POSITIONS = {
        "MOST": Word(3, 0, 4),
        "ORA": Word(24, 21, 3),
        "VAN": Word(15, 24, 3),
        "MULT": Word(0, 24, 4),
        "OT_MULT": Word(27, 24, 2),
        "TIZ_MULT": Word(0, 27, 3),
        "OT_MULVA": Word(18, 0, 2),
        "TIZ_MULVA": Word(21, 0, 3),
        "PERC": Word(0, 6, 4),
        "PERCCEL": Word(12, 27, 7),
        "NEGYED": Word(15, 3, 6),
        "MULVA": Word(15, 6, 5),
        "FEL": Word(0, 9, 3),
        "HAROMNEGYED": Word(0, 3, 11),
    }

    def __init__(self, display):
        """Initialize the word clock with display.
        Args:
            display: The display to show the clock on
        """
        self.display = display

    def draw(self, wt: WallTime) -> None:
        """Draw current time on the display.

        Args:
            wt: WallTime object containing the current time
        """
        # Clear the display
        self.display.clear()

        hour = wt.hour % 12

        # Write the hour
        self.display.show(self.HOURS[hour])
        if hour == 11:  # TIZEN-EGY consists of two blocks
            self.display.show(self.HOURS[1])

        # Determine which words to light up based on time
        current_words = self.TIME_WORDS[wt.minute // 5]

        # Draw words for current time
        for word in current_words.split():
            if word not in self.WORD_POSITIONS:
                raise ValueError(f"Unknown word: {word}")
            self.display.show(self.WORD_POSITIONS[word])
