# utils.py

import sys

def clear_terminal():
    """Clears the terminal screen."""
    sys.stdout.write("\033[H\033[J")

def handle_error(message):
    """Handles errors by printing an error message and exiting."""
    print(f"Error: {message}")
    sys.exit(1)

def handle_exit():
    """Handles program exit gracefully."""
    print("\nExiting...")
    sys.exit(0)