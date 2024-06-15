import time
import psutil
import os
from config import DEFAULT_LEN, HEIGHT
from utils import clear_terminal, handle_error

# Graph symbols for CPU usage representation
graph_up = {
    0.0: " ", 0.1: "⢀", 0.2: "⢠", 0.3: "⢰", 0.4: "⢸",
    1.0: "⡀", 1.1: "⣀", 1.2: "⣠", 1.3: "⣰", 1.4: "⣸",
    2.0: "⡄", 2.1: "⣄", 2.2: "⣤", 2.3: "⣴", 2.4: "⣼",
    3.0: "⡆", 3.1: "⣆", 3.2: "⣦", 3.3: "⣶", 3.4: "⣾",
    4.0: "⡇", 4.1: "⣇", 4.2: "⣧", 4.3: "⣷", 4.4: "⣿"
}

CORE_COUNT = psutil.cpu_count(logical=True)

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

    # Scale CPU usage to fit within the graph symbols
    scaled_history = [min(HEIGHT, max(0, val / 4)) for val in history]  # Scale to match the symbol's range

    # Prepare the graph lines
    lines = []
    for h in range(HEIGHT):
        line = ""
        for i in range(len(history)):
            index = HEIGHT - h - 1
            if scaled_history[i] >= index:
                symbol_index = round(scaled_history[i] - index, 1)
                line += graph_up.get(symbol_index, " ")
            else:
                line += " "
        lines.append(line)

    # Clear screen and draw border
    clear_terminal()
    print(f"CPU usage: Overall {cpu_percent:.1f}% ({time.strftime('%Y-%m-%d %H:%M:%S')})")
    print("┌" + "─" * len_points + "┐")  # Top border

    # Draw graph
    for line in lines:
        print("│" + line + "│")

    print("└" + "─" * len_points + "┘")  # Bottom border
    print(f"this system has {CORE_COUNT} cores")

