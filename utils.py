import numpy as np


def new_grid(dim, fill=" "):
    return np.array([[f"{fill}" for _ in range(dim)] for _ in range(dim)])


def visualize_grid(grid, visited=None):
    # symbols for grid visualization
    border_sym, space_sym, visited_sym = "+", "  ", "."

    if visited:
        # mark the points already visited if they are provided
        for p in visited:
            grid[p] = visited_sym

    # add visual border at beginning and end of grid
    main_body = [space_sym.join([border_sym] + list(row) + [border_sym]) for row in grid]

    # add visual border at top and bottom of main body
    top = bottom = space_sym.join([border_sym] * (len(grid) + 2))
    whole = [top] + main_body + [bottom]

    return "\n".join(whole)
