from collections import defaultdict

import numpy as np


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


# inspired by this gist: https://gist.github.com/hrldcpr/2012250
def tree(): return defaultdict(tree)
