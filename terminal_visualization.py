from time import sleep

from asciimatics.screen import ManagedScreen


def visualize(grid):
    with ManagedScreen() as screen:
        for i, row in enumerate(grid.split("\n")):
            screen.print_at(row, 0, i)
        screen.refresh()
        sleep(0.05)
