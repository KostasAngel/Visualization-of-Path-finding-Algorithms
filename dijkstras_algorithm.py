import math

import numpy as np

import utils


def calculate(grid: np.ndarray, start: tuple, goal: tuple):
    # temporary for backwards compatibility
    if start == (0, 0) and goal == (62, 62):
        return calculate2(start, goal, utils.Grid(create_maze=True))
    else:
        return calculate2(start, goal, utils.Grid(custom_grid=grid))


def calculate2(start: tuple, goal: tuple, grid: utils.Grid = utils.Grid()):
    """ Finds path from start to goal using Dijkstra's algorithm.

    Implementation of this algorithm was based on the example provided in Wikipedia:
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode

    :param grid: A numpy array representing the grid where start and goal are located.
    :param start: A tuple representing the starting point, e.g. (0, 0).
    :param goal: A tuple representing the goal point, e.g. (10, 10).
    """

    pq = utils.PriorityQueue()
    distances = dict()
    child_parent_pairs = dict()
    visited = []

    # add all points in grid to priority queue with infinite distances and no parents
    for y, x in np.ndindex(grid.to_ndarray().shape):
        distances[(y, x)] = math.inf
        child_parent_pairs[(y, x)] = ""
        pq.add_point((y, x), math.inf)

    # update starting point's distance and priority to 0
    distances[start] = 0
    pq.add_point(start, priority=0)

    while pq.has_points():
        # get point with lowest priority and remove from queue
        current_point = pq.get_lowest_priority_point()
        visited.append(current_point)

        if current_point == goal:
            # goal has been reached
            break

        for neighbor in grid.get_point_neighbors(current_point):
            if pq.contains_point(neighbor):

                alt_distance = distances[current_point] + 1  # neighbors always 1 step away from current

                if alt_distance < distances[neighbor]:
                    distances[neighbor] = alt_distance
                    pq.add_point(neighbor, alt_distance)  # update neighbor's priority with new distance
                    child_parent_pairs[neighbor] = current_point

    path = utils.calculate_path(start, goal, child_parent_pairs)

    return {"path": path, "visited": visited, "grid": grid.to_ndarray(), "start": start, "goal": goal}


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
