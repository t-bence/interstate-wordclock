from interstate75 import DISPLAY_INTERSTATE75_32X32, Interstate75

from word_clock import Word


class Display:
    def __init__(self):
        """Initialize the display hardware."""
        self.i75 = Interstate75(
            display=DISPLAY_INTERSTATE75_32X32,
            stb_invert=False,
            panel_type=Interstate75.PANEL_GENERIC,
        )
        self.display = self.i75.display

        # Colors
        self.BLACK = self.display.create_pen(0, 0, 0)
        self.WHITE = self.display.create_pen(255, 255, 255)

    def clear(self):
        """Clear the display."""
        self.display.set_pen(self.BLACK)
        self.display.clear()

    def show(self, word: Word):
        """Display a word on the screen.

        Args:
            word: The Word object to display
        """
        self.display.set_pen(self.WHITE)
        self.display.rectangle(
            word.x, word.y, word.length * word.period - 1, word.period - 1
        )

    def update(self):
        """Update the display to show all drawn content."""
        self.i75.update()
