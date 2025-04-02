from word_clock import WallTime


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
    import time

    import network

    # Initialize the wireless interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

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
    import network
    import ntptime

    # Initialize the wireless interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

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


def get_current_time() -> WallTime:
    """Retrieve the current time from the RTC module.

    Returns
    -------
    WallTime
        Current time with hour and minute values.
    """
    import machine

    t = machine.RTC().datetime()
    # datetime returns an 8-tuple:
    # (year, month, mday, hour, minute, second, weekday, yearday)
    return WallTime(hour=t[4], minute=t[5])
