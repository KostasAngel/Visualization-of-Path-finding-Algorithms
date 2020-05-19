from time import sleep

import numpy as np
from asciimatics.screen import ManagedScreen


def calculate_path(start, goal, child_parent_pairs):
    # if goal not in child_parent_pairs.values():
    #     raise AssertionError("No route to goal (goal not in child_parent_pairs)")
    reverse_path = [goal]
    while reverse_path[-1] != start:
        reverse_path.append(child_parent_pairs[reverse_path[-1]])

    return list(reversed(reverse_path))


# Grid could be a class, and get_neighbors one of its methods
def get_neighbors(point, grid):
    # possible movements, only up down left right, maybe diagonally should be an option?
    dy, dx = [-1, 0, 1, 0], [0, 1, 0, -1]

    neighbors = []
    for i in range(len(dy)):
        # possible neighbors
        y, x = point[0] + dy[i], point[1] + dx[i]

        # check if neighbors are within the grid
        if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
            if grid[y, x] == " ":
                neighbors.append((y, x))

    return neighbors


def new_grid(dim, fill=" "):
    return np.array([[f'{fill}' for _ in range(dim)] for _ in range(dim)])


def visualize_grid(grid, visited=None, path=None, start=None, goal=None, legend=True):
    grid = np.copy(grid)
    # symbols for grid visualization
    symbols = {"border": "+",
               "space": " ",
               "visited": "·",
               "path": "o",
               "start": "S",
               "goal": "G"}

    # mark the points visited
    if visited:
        for p in visited:
            grid[p] = symbols["visited"]

    # draw path if provided
    if path:
        for p in path:
            grid[p] = symbols["path"]

    # draw start and goal
    if start:
        grid[start] = symbols["start"]
    if goal:
        grid[goal] = symbols["goal"]

    # add visual border at beginning and end of grid
    main_body = [symbols["space"].join([symbols["border"]] + list(row) + [symbols["border"]]) for row in grid]

    # add visual border at top and bottom of main body
    top = bottom = symbols["space"].join([symbols["border"]] * (len(grid) + 2))
    whole = [top] + main_body + [bottom]

    if legend:
        lgd = [f"{v} -> {k}" for k, v in symbols.items()]
        whole = whole + lgd

    return "\n".join(whole)


def visualize_asciimatics(res):
    with ManagedScreen() as screen:

        for i in range(1, len(res["visited"])):
            grid = visualize_grid(res["grid"], visited=res["visited"][:i + 1], start=res["start"], goal=res["goal"])

            for j, row in enumerate(grid.split("\n")):
                screen.print_at(row, 0, j)
            screen.refresh()
            sleep(0.03)
        grid = visualize_grid(res["grid"], visited=res["visited"][:i + 1], path=res["path"], start=res["start"],
                              goal=res["goal"])
        for j, row in enumerate(grid.split("\n")):
            screen.print_at(row, 0, j)
        screen.refresh()
        sleep(20)
