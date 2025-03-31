import os
import sys

# load main code
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ensure mock libraries are loaded first
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import mock_libraries

# Now import the main script
import main


def test_draw_word_clock():
    # This test just ensures the function runs without errors
    try:
        main.draw_word_clock(12, 12)
    except Exception as e:
        assert False, f"draw_word_clock() raised an exception: {e}"
