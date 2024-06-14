import time
import psutil
import argparse
import os
import sys
from config import DEFAULT_LEN, DEFAULT_INTERVAL_MS
from cpu_monitor import draw
from utils import handle_error, handle_exit


def main(len_points, interval_ms):
    history = []

    while True:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            draw(cpu_percent, history, len_points)
            time.sleep(interval_ms / 1000.0)  # Convert interval from ms to seconds
        except KeyboardInterrupt:
            handle_exit()
        except Exception as e:
            handle_error(f"An unexpected error occurred: {e}")


def introduction():
    os.system("clear")
    print("                                        /$$                ")
    print("                                       | $$                ")
    print("  /$$$$$$   /$$$$$$  /$$$$$$   /$$$$$$ | $$$$$$$  /$$   /$$")
    print(" /$$__  $$ /$$__  $$|____  $$ /$$__  $$| $$__  $$| $$  | $$")
    print("| $$  \ $$| $$  \__/ /$$$$$$$| $$  \ $$| $$  \ $$| $$  | $$")
    print("| $$  | $$| $$      /$$__  $$| $$  | $$| $$  | $$| $$  | $$")
    print("|  $$$$$$$| $$     |  $$$$$$$| $$$$$$$/| $$  | $$|  $$$$$$$")
    print(" \____  $$|__/      \_______/| $$____/ |__/  |__/ \____  $$")
    print(" /$$  \ $$                   | $$                 /$$  | $$")
    print("|  $$$$$$/                   | $$                |  $$$$$$/")
    print(" \______/                    |__/                 \______/ ")
    print("")
    print("This program will have bugs, if you encounter them report them.")
    input("(press enter to continue)")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CPU Usage Monitor with Adjustable Graph Length"
    )
    parser.add_argument(
        "--len",
        type=int,
        default=DEFAULT_LEN,
        help="Number of data points to show horizontally (default: %(default)s)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL_MS,
        help="Update interval in milliseconds (default: %(default)s)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    try:
        if "--help" in sys.argv:
            parser = argparse.ArgumentParser(
                description="CPU Usage Monitor with Adjustable Graph Length"
            )
            parser.add_argument(
                "--len",
                type=int,
                default=DEFAULT_LEN,
                help="Number of data points to show horizontally (default: %(default)s)",
            )
            parser.add_argument(
                "--interval",
                type=int,
                default=DEFAULT_INTERVAL_MS,
                help="Update interval in milliseconds (default: %(default)s)",
            )
            parser.print_help()
        else:
            args = parse_arguments()
            introduction()
            main(args.len, args.interval)
    except Exception as e:
        handle_error(f"Unexpected error: {e}")
