from collections import deque

import numpy as np

import path_finding_algorithms.utils as utils


def calculate(grid: np.ndarray, start: tuple, goal: tuple):
    # temporary for backwards compatibility
    # here I'm replacing the grids from the old method to make sure the revised algorithms work as expected
    return calculate2(start, goal, utils.Grid())


def calculate2(start: tuple, goal: tuple, grid: utils.Grid = utils.Grid()):
    """ Finds path from start to goal using the Breadth-First Search algorithm.

    Works by creating a double ended queue (deque) - by always appending to the **right** of the queue,
    and then considering the **left-most** points in the queue first, the deque essentially works as a FIFO queue.

    :param start: A tuple representing the starting point, e.g. (0, 0).
    :param goal: A tuple representing the goal point, e.g. (10, 10).
    :param grid: A Grid object representing the space where start and goal are located, optional.
    """

    queue = deque([start])

    visited = []

    child_parent_pairs = dict()

    while queue:  # stops when all points have been considered or when goal is reached

        current_point = queue.pop()  # get right-most point in queue

        visited.append(current_point)  # mark point as visited

        if current_point == goal:
            # goal has been reached
            # do not return from here, by returning below the case where no path is found is captured
            break

        for neighbor in grid.get_point_neighbors(current_point):
            if neighbor not in visited and neighbor not in queue:  # check if already visited this point
                queue.appendleft(neighbor)  # append to the left of the queue
                child_parent_pairs[neighbor] = current_point

    path = utils.calculate_path(start, goal, child_parent_pairs)

    return {"path": path, "visited": visited, "grid": grid.to_ndarray(), "start": start, "goal": goal}


def main():
    # grid = utils.new_grid(20)
    #
    # grid[:17, 4] = "+"
    # grid[1, 1:9] = "+"
    # grid[10, 6:18] = "+"
    # grid[10:, 7] = "+"

    # the code here is just for testing, the program can just call calculate() above and skip this
    grid = utils.Grid(size=19, create_maze=True)

    res = calculate2(grid=grid, start=(0, 0), goal=(18, 18))

    # the following allows visualizing results in the terminal (thus only works when script is run from the terminal)
    utils.visualize_asciimatics(res)


if __name__ == '__main__':
    main()
