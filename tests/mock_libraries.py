import sys
from typing import Any


class MockMachine:
    class RTC:
        def __init__(self):
            self._datetime = (2023, 9, 15, 0, 10, 30, 0, 0)  # Example fixed datetime

        def datetime(self, *args):
            # If no args, return current datetime
            # If args provided, set datetime (optional)
            return self._datetime


class MockNetwork:
    STA_IF = "station"

    class WLAN:
        def __init__(self, interface):
            self._status = 3  # Simulate connected state
            self._active = False

        def active(self, active=None):
            if active is not None:
                self._active = active
            return self._active

        def connect(self, ssid, password):
            # Simulate connection
            pass

        def status(self):
            return self._status

        def config(self, **kwargs):
            # Simulate network configuration
            pass


class MockNTPTime:
    def settime(self):
        # Simulate NTP time sync
        pass


class MockInterstate75:
    DISPLAY_INTERSTATE75_32X32 = "mock_display"
    PANEL_GENERIC = "generic"

    class Interstate75:
        PANEL_GENERIC = "generic"

        def __init__(self, display: Any, stb_invert: bool, panel_type: Any):
            self.display = MockInterstate75.Display()

    class Display:
        def create_pen(self, r, g, b):
            return f"pen_{r}_{g}_{b}"

        def set_pen(self, color):
            pass

        def clear(self):
            pass

        def rectangle(self, x, y, width, height):
            pass

    def __init__(self, **kwargs):
        self.display = self.Display()

    def update(self):
        pass


# Patch the original libraries with mocks
sys.modules["machine"] = MockMachine()
sys.modules["network"] = MockNetwork()
sys.modules["ntptime"] = MockNTPTime()
sys.modules["interstate75"] = MockInterstate75()
