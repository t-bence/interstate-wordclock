from display import Display, Word
from time_service import get_current_time, sync_time
from word_clock import WordClock


def main():
    # Initialize the display
    display = Display()

    # Create a word clock with our display
    word_clock = WordClock(display)

    # Sync time once at startup
    sync_time()

    # Main loop
    while True:
        wall_time = get_current_time()
        word_clock.draw(wall_time)
        display.update()

        # Sleep for a minute before next update
        import time

        time.sleep(60)  # Update every minute


if __name__ == "__main__":
    main()
