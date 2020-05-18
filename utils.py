from collections import defaultdict

import numpy as np


def new_grid(dim, fill=" "):
    return np.array([[f"{fill}" for _ in range(dim)] for _ in range(dim)])


def visualize_grid(grid, visited=None, path=None, start=None, goal=None):
    grid = np.copy(grid)
    # symbols for grid visualization
    border_sym = "+"
    space_sym = "  "
    visited_sym = "."
    path_sym = "x"
    start_sym = "s"
    goal_sym = "g"

    # mark the points visited
    if visited:
        for p in visited:
            grid[p] = visited_sym

    # draw path if provided
    if path:
        for p in path:
            grid[p] = path_sym

    if start:
        grid[start] = start_sym
    if goal:
        grid[goal] = goal_sym

    # add visual border at beginning and end of grid
    main_body = [space_sym.join([border_sym] + list(row) + [border_sym]) for row in grid]

    # add visual border at top and bottom of main body
    top = bottom = space_sym.join([border_sym] * (len(grid) + 2))
    whole = [top] + main_body + [bottom]

    return "\n".join(whole)


# inspired by this gist: https://gist.github.com/hrldcpr/2012250
def tree(): return defaultdict(tree)
