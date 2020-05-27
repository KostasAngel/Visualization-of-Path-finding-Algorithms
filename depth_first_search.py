from collections import deque

import numpy as np

import utils


def calculate(grid: np.ndarray, start: tuple, goal: tuple):
    """ Finds path from start to goal using the Depth-First Search algorithm.

    Works by creating a double ended queue (deque) - by always appending to the **right** of the queue,
    and then considering the **right-most** points in the queue first, the deque essentially works as a LIFO
    queue/stack.

    :param grid: A numpy array representing the grid where start and goal are located.
    :param start: A tuple representing the starting point, e.g. (0, 0).
    :param goal: A tuple representing the goal point, e.g. (10, 10).
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

        for neighbor in utils.get_neighbors(current_point, grid):
            if neighbor not in visited:  # check if already visited this point
                queue.append(neighbor)  # append to the right of the queue
                child_parent_pairs[neighbor] = current_point

    path = utils.calculate_path(start, goal, child_parent_pairs)

    return {"path": path, "visited": visited, "grid": grid, "start": start, "goal": goal}


def main():
    # the code here is just for testing, the program can just call calculate() above and skip this
    grid = utils.new_grid(20)

    grid[:17, 4] = "+"
    grid[1, 1:9] = "+"
    grid[10, 6:18] = "+"
    grid[10:, 7] = "+"

    res = calculate(grid=grid, start=(0, 0), goal=(17, 17))

    # the following allows visualizing results in the terminal (thus only works when script is run from the terminal)
    utils.visualize_asciimatics(res)


if __name__ == '__main__':
    main()
