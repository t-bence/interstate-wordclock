import time
import machine
import network
import ntptime
from interstate75 import DISPLAY_INTERSTATE75_32X32, Interstate75

# Check and import the Network SSID and Password from secrets.py
try:
    from secrets import WIFI_PASSWORD, WIFI_SSID
    if WIFI_SSID == "":
        raise ValueError("WIFI_SSID in 'secrets.py' is empty!")
    if WIFI_PASSWORD == "":
        raise ValueError("WIFI_PASSWORD in 'secrets.py' is empty!")
except ImportError:
    raise ImportError("'secrets.py' is missing from your Plasma 2350 W!")
except ValueError as e:
    print(e)

rtc = machine.RTC()

# Enable the Wireless
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


def network_connect(SSID, PSK):

    # Number of attempts to make before timeout
    max_wait = 10

    # Sets the Wireless LED pulsing and attempts to connect to your local network.
    print("connecting...")
    wlan.config(pm=0xa11140)  # Turn WiFi power saving off for some slow APs
    wlan.connect(SSID, PSK)

    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error. Switches the Warn LED on.
    if wlan.status() != 3:
        print("Unable to connect. Attempting connection again")


# Function to sync the Pico RTC using NTP
def sync_time():

    try:
        network_connect(WIFI_SSID, WIFI_PASSWORD)
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
    "ORA MULT TIZ_MULT PERCCEL",   # 10
    "MOST NEGYED VAN",       # 15
    "NEGYED MULT OT_MULT PERCCEL",# 20
    "OT_MULVA PERC MULVA FEL",   # 25
    "MOST FEL VAN",          # 30
    "FEL MULT OT_MULT PERCCEL",     # 35
    "FEL MULT TIZ_MULT PERCCEL",          # 40
    "MOST HAROMNEGYED VAN",         # 45
    "TIZ_MULVA PERC MULVA ORA",             # 50
    "OT_MULVA PERC MULVA ORA",            # 55
]

PERIOD = 3 # lettering period: one letter's width plus a border

# Setup for the display
i75 = Interstate75(
    display=DISPLAY_INTERSTATE75_32X32, stb_invert=False, panel_type=Interstate75.PANEL_GENERIC)
display = i75.display

# Colors
WHITE = display.create_pen(255, 255, 255)

# Word positions (x, y, width, height)
WORD_POSITIONS = {
    "MOST": (3, 0, 4),
    "ORA": (24, 21, 3),
    "VAN": (15, 24, 3),
    "MULT": (0, 24, 4),
    "OT_MULT": (27, 24, 2),
    "TIZ_MULT": (0, 27, 3),
    "OT_MULVA": (18, 0, 2),
    "TIZ_MULVA": (21, 0, 3),
    "PERC": (0, 6, 4),
    "PERCCEL": (12, 27, 7),
    "NEGYED": (15, 3, 6),
    "MULVA": (15, 6, 5),
    "FEL": (0, 9, 3),
    "HAROMNEGYED": (0, 3, 11)
}

HOURS = (
    (0, 12, 10),
    (15, 15, 3),
    (15, 12, 5),
    (6, 18, 5),
    (9, 21, 4),
    (21, 18, 2),
    (0, 21, 3),
    (24, 15, 3),
    (0, 15, 5),
    (12, 9, 6),
    (24, 18, 3),
    (0, 12, 5)
)

def write_characters(x: int, y: int, chars: int) -> None:
    """Draw a rectangle at the specified coordinates with the given characters."""
    display.rectangle(x, y, chars * PERIOD - 1, PERIOD - 1)


def draw_word_clock():
    # Clear the display
    display.set_pen(WHITE)
    display.clear()

    # Get current time
    t = machine.RTC().datetime()
    hour = t[4] % 12
    minute = t[5]

    # write the hour
    write_characters(*HOURS[hour])
    if hour == 11: # TIZEN-EGY consists of two blocks
        write_characters(*HOURS[1])

    # Determine which words to light up based on time
    current_words = TIME_WORDS[minute // 5]

    # Draw words for current time
    for word in current_words.split():
        if word not in WORD_POSITIONS:
            raise ValueError(f"Unknown word: {word}")
        write_characters(*WORD_POSITIONS[word])

        
    # Update display
    i75.update()

def main():
    # Sync time once at startup
    sync_time()

    # Main loop
    while True:
        draw_word_clock()
        time.sleep(60)  # Update every minute

if __name__ == "__main__":
    main()
