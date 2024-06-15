import time
import psutil
import os
from config import DEFAULT_LEN, HEIGHT
from utils import clear_terminal, handle_error

GRAPH_HEIGHT = 10
graph_symbol = "█"

def check_terminal_size():
    """Checks if the terminal size is sufficient to display the graph."""
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        rows = int(rows)
        columns = int(columns)
        return rows >= GRAPH_HEIGHT + 4 and columns >= DEFAULT_LEN + 4
    except Exception as e:
        handle_error(f"Failed to check terminal size: {e}")

def get_cpu_cores():
    """Returns the number of CPU cores as an integer."""
    try:
        return psutil.cpu_count(logical=True)
    except Exception as e:
        handle_error(f"Failed to get CPU core count: {e}")

def draw(cpu_percent, history, len_points):
    """Draws the CPU usage graph."""
    if not check_terminal_size():
        clear_terminal()
        print("Terminal window is too small to display the graph properly.")
        return

    history.append(cpu_percent)
    if len(history) > len_points:
        history.pop(0)

    # Scale CPU usage to fit within the new graph height
    scaled_history = [int(min(GRAPH_HEIGHT, max(1, val // 10))) for val in history]

    lines = []
    for h in range(GRAPH_HEIGHT):
        line = ""
        for i in range(len(history)):
            val = scaled_history[i] - (GRAPH_HEIGHT - h - 1)
            if val > 0:
                line += graph_symbol
            else:
                line += " "
        lines.append(line)

    clear_terminal()
    print(f"CPU usage: Overall {cpu_percent:.1f}% ({time.strftime('%Y-%m-%d %H:%M:%S')})")
    print("┌" + "─" * len_points + "┐")  # Top border

    # Draw graph
    for line in lines:
        print("│" + line + "│")

    print("└" + "─" * len_points + "┘")  # Bottom border
    print(f"CPU Cores: {get_cpu_cores()}") 

def main(len_points, interval_ms):
    history = []
    while True:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            draw(cpu_percent, history, len_points)
            time.sleep(interval_ms / 1000.0 - 1)  # Adjust for interval after the 1-second cpu_percent call
        except KeyboardInterrupt:
            handle_exit()
        except Exception as e:
            handle_error(f"An unexpected error occurred: {e}")
