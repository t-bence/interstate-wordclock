import time

import machine
import network
from interstate75 import DISPLAY_INTERSTATE75_32X32, Interstate75

# Enable the Wireless
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


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

    def draw(self, display):
        """
        Draw the word on the display by creating a rectangular block

        Args:
            display: The display object to draw on
        """
        display.rectangle(
            self.x, self.y, self.length * self.period - 1, self.period - 1
        )


def get_network_config() -> tuple[str, str]:
    """
    Retrieve the network configuration from secrets.py
    """
    try:
        from secrets import WIFI_PASSWORD, WIFI_SSID

        if WIFI_SSID == "":
            raise ValueError("WIFI_SSID in 'secrets.py' is empty!")
        if WIFI_PASSWORD == "":
            raise ValueError("WIFI_PASSWORD in 'secrets.py' is empty!")
    except ImportError:
        raise ImportError("'secrets.py' is missing!")
    except ValueError as e:
        print(e)
    return WIFI_SSID, WIFI_PASSWORD


def network_connect(SSID: str, PSK: str):
    """Connect to a wireless network using the provided SSID and PSK.

    Parameters
    ----------
    SSID : str
        Network SSID
    PSK : str
        Wifi password
    """

    # Number of attempts to make before timeout
    max_wait = 10

    # Sets the Wireless LED pulsing and attempts to connect to your local network.
    print("connecting...")
    wlan.config(pm=0xA11140)  # Turn WiFi power saving off for some slow APs
    wlan.connect(SSID, PSK)

    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("waiting for connection...")
        time.sleep(1)

    # Handle connection error. Switches the Warn LED on.
    if wlan.status() != 3:
        print("Unable to connect. Attempting connection again")


def sync_time():
    """Sync the system time using an NTP server."""
    import ntptime

    ssid, password = get_network_config()
    try:
        network_connect(ssid, password)
    except NameError:
        print("Create secrets.py with your WiFi credentials")

    if wlan.status() < 0 or wlan.status() >= 3:
        try:
            ntptime.settime()
        except OSError:
            print("Unable to sync with NTP server. Check network and try again.")


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

PERIOD = 3  # lettering period: one letter's width plus a border

# Setup for the display
i75 = Interstate75(
    display=DISPLAY_INTERSTATE75_32X32,
    stb_invert=False,
    panel_type=Interstate75.PANEL_GENERIC,
)

display = i75.display

# Colors
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

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


def get_current_time():
    # Get current time
    t = machine.RTC().datetime()
    hour = t[4]
    minute = t[5]
    return hour, minute


def draw_word_clock(hour: int, minute: int):
    # Clear the display
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)

    hour = hour % 12

    # Write the hour
    HOURS[hour].draw(display)
    if hour == 11:  # TIZEN-EGY consists of two blocks
        HOURS[1].draw(display)

    # Determine which words to light up based on time
    current_words = TIME_WORDS[minute // 5]

    # Draw words for current time
    for word in current_words.split():
        if word not in WORD_POSITIONS:
            raise ValueError(f"Unknown word: {word}")
        WORD_POSITIONS[word].draw(display)


def main():
    # Sync time once at startup
    sync_time()

    # Main loop
    while True:
        hour, minute = get_current_time()
        draw_word_clock(hour, minute)
        i75.update()
        time.sleep(60)  # Update every minute


if __name__ == "__main__":
    main()
