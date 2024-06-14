# cpu_monitor.py

import time
import psutil
import os
from config import DEFAULT_LEN, HEIGHT
from utils import clear_terminal, handle_error

def check_terminal_size():
    """Checks if the terminal size is sufficient to display the graph."""
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        rows = int(rows)
        columns = int(columns)
        return rows >= HEIGHT + 4 and columns >= DEFAULT_LEN + 4
    except Exception as e:
        handle_error(f"Failed to check terminal size: {e}")

def draw(cpu_percent, history, len_points):
    """Draws the CPU usage graph."""
    if not check_terminal_size():
        clear_terminal()
        print("Terminal window is too small to display the graph properly.")
        return

    history.append(cpu_percent)
    if len(history) > len_points:
        history.pop(0)

    # Scale CPU usage to fit within the available height
    scaled_history = [int(min(HEIGHT, max(1, val // 5))) for val in history]  # Ensure at least 1 dot for any positive value

    # Prepare the graph lines
    lines = []
    for h in range(HEIGHT):
        line = ""
        for i in range(len(history)):
            if scaled_history[i] >= HEIGHT - h:
                line += "."
            else:
                line += " "
        lines.append(line)

    # Prepare x-axis line
    rx = "    " + "".join(str(i // 10) if i % 10 == 0 else " " for i in range(len_points))

    # Clear screen and draw border
    clear_terminal()
    print(f"CPU usage: Overall {cpu_percent:.1f}% ({time.strftime('%Y-%m-%d %H:%M:%S')})")
    print("┌" + "─" * len_points + "┐")  # Top border

    # Draw graph
    for line in lines:
        print("│" + line + "│")

    print("└" + "─" * len_points + "┘")  # Bottom border
    print("(each dot represents 5% cpu usage)")
