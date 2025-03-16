"""
MicroPython docs: https://docs.micropython.org/en/latest/library/machine.RTC.html
"""

import time

import machine
import network
import ntptime
from interstate75 import DISPLAY_INTERSTATE75_32X32, Interstate75

SHADOW_OFFSET = 1

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
    max_wait = 5

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


# Setup for the display
i75 = Interstate75(
    display=DISPLAY_INTERSTATE75_32X32, stb_invert=False, panel_type=Interstate75.PANEL_GENERIC)
display = i75.display

WIDTH, HEIGHT = display.get_bounds()

# Pens
WHITE = display.create_pen(255, 255, 255)
display.set_pen(WHITE)

sync_time()

HOURS = [
    (0, 12, 30, 3),
    (15, 15, 9, 3),
    (15, 12, 15, 3),
    (6, 18, 15, 3),
    (9, 21, 12, 3),
    (21, 18, 6, 3),
    (0, 21, 9, 3),
    (24, 15, 9, 3),
    (0, 15, 15, 3),
    (12, 9, 18, 3),
    (24, 18, 9, 3),
    (0, 12, 15, 3),
    (15, 15, 9, 3)
]

while True:

    display.clear()

    year, month, day, hour, minute, second, microsecond, tzinfo = rtc.datetime()

    hour = hour % 12
    index = minute // 5

    # showWords(TIME_WORDS[index], WORD_LENGTH)

    if (index >= 3): # if it's past the first quarter
        hour = (hour + 1) % 12 # show next hour

    display.rectangle(*HOURS[hour])
    if (hour == 11):
        display.rectangle(*HOURS[12]) # 11 consists of two word parts in Hungarian

    i75.update()

    time.sleep(1)
