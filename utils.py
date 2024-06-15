import sys
import psutil

def clear_terminal():
    """Clears the terminal screen."""
    sys.stdout.write("\033[H\033[J")

def handle_error(message):
    """Handles errors by printing an error message and exiting."""
    print(f"Error: {message}")
    sys.exit(1)

def handle_exit():
    """Handles program exit gracefully."""
    print("Exiting program...")
    sys.exit(0)

def get_cpu_cores():
    """Returns the number of CPU cores as an integer."""
    try:
        return psutil.cpu_count(logical=True)
    except Exception as e:
        handle_error(f"Failed to get CPU core count: {e}")
