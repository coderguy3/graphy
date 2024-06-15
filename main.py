import time
import psutil
import argparse
import os
import sys
import threading
from config import DEFAULT_LEN, DEFAULT_INTERVAL_MS
from cpu_monitor import draw
from utils import handle_error, handle_exit, get_cpu_cores

class CpuMonitor:
    def __init__(self, interval_ms):
        self.interval = interval_ms / 1000.0
        self.cpu_percent = 0
        self.running = True

    def start(self):
        self.thread = threading.Thread(target=self.update_cpu_percent)
        self.thread.start()

    def update_cpu_percent(self):
        while self.running:
            self.cpu_percent = psutil.cpu_percent(interval=self.interval)

    def stop(self):
        self.running = False
        self.thread.join()

def main(len_points, interval_ms):
    history = []
    cpu_monitor = CpuMonitor(interval_ms)
    cpu_monitor.start()

    try:
        while True:
            draw(cpu_monitor.cpu_percent, history, len_points)
            time.sleep(interval_ms / 1000.0)  # Convert interval from ms to seconds
    except KeyboardInterrupt:
        handle_exit()
    except Exception as e:
        handle_error(f"An unexpected error occurred: {e}")
    finally:
        cpu_monitor.stop()

def introduction():
    os.system('clear')
    print('                                        /$$                ')
    print('                                       | $$                ')
    print('  /$$$$$$   /$$$$$$  /$$$$$$   /$$$$$$ | $$$$$$$  /$$   /$$')
    print(' /$$__  $$ /$$__  $$|____  $$ /$$__  $$| $$__  $$| $$  | $$')
    print('| $$  \ $$| $$  \__/ /$$$$$$$| $$  \ $$| $$  \ $$| $$  | $$')
    print('| $$  | $$| $$      /$$__  $$| $$  | $$| $$  | $$| $$  | $$')
    print('|  $$$$$$$| $$     |  $$$$$$$| $$$$$$$/| $$  | $$|  $$$$$$$')
    print(' \____  $$|__/      \_______/| $$____/ |__/  |__/ \____  $$')
    print(' /$$  \ $$                   | $$                 /$$  | $$')
    print('|  $$$$$$/                   | $$                |  $$$$$$/')
    print(' \______/                    |__/                 \______/ ')
    print('')
    print('This program will have bugs, if you encounter them report them.')
    input("(press enter to continue)")

def parse_arguments():
    parser = argparse.ArgumentParser(description="CPU Usage Monitor with Adjustable Graph Length")
    parser.add_argument("--len", type=int, default=DEFAULT_LEN, help="Number of data points to show horizontally (default: %(default)s)")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL_MS, help="Update interval in milliseconds (default: %(default)s)")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_arguments()
        if not any(arg in sys.argv for arg in ["-h", "--help"]):
            introduction()
        main(args.len, args.interval)
    except Exception as e:
        handle_error(f"Unexpected error: {e}")
