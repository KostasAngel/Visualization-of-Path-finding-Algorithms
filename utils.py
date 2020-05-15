import numpy as np


def new_grid(dim, fill="."):
    return [[f"{fill}" for _ in range(dim)] for _ in range(dim)]


def visualize_grid(visited, dim):
    # symbols for grid visualization
    border_sym, space_sym, visited_sym = "+", "  ", "."

    # create empty grid
    grid = np.array(new_grid(dim, fill=" "))

    # mark the points already visited
    for p in visited:
        grid[p] = visited_sym

    # add visual border at beginning and end of grid
    main_body = [space_sym.join([border_sym] + list(row) + [border_sym]) for row in grid]

    # add visual border at top and bottom
    top = bottom = space_sym.join([border_sym] * (dim + 2))
    whole = [top] + main_body + [bottom]

    return "\n".join(whole)
