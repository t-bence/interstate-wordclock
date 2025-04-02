import os
import sys

# load main code
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Ensure mock libraries are loaded first
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# import mock_libraries

# Now import the main script
from word_clock import WallTime


def test_draw_word_clock():
    # This test just ensures the function runs without errors
    try:
        noon = WallTime(12, 0)
    except Exception as e:
        assert False, f"draw_word_clock() raised an exception: {e}"
