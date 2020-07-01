import math

import numpy as np

import path_finding_algorithms.utils as utils


def calculate2(start: tuple, goal: tuple, grid: utils.Grid = utils.Grid()):
    """ Finds path from start to goal using Dijkstra's algorithm.

    Implementation of this algorithm was based on the example provided in Wikipedia:
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode

    :param start: A tuple representing the starting point, e.g. (0, 0).
    :param goal: A tuple representing the goal point, e.g. (10, 10).
    :param grid: A Grid object representing the space where start and goal are located, optional.
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

                # neighbors always 1 step away from current
                alt_distance = distances[current_point] + 1

                if alt_distance < distances[neighbor]:
                    distances[neighbor] = alt_distance
                    # update neighbor's priority with new distance
                    pq.add_point(neighbor, alt_distance)
                    child_parent_pairs[neighbor] = current_point

    path = utils.calculate_path(start, goal, child_parent_pairs)

    return {"path": path, "visited": visited, "grid": grid.to_ndarray(), "start": start, "goal": goal}


def main():
    # the code here is just for testing, the program can just call calculate() above and skip this
    grid = utils.Grid(size=19, create_maze=True)

    res = calculate2(grid=grid, start=(0, 0), goal=(18, 18))

    # the following allows visualizing results in the terminal (thus only works when script is run from the terminal)
    utils.visualize_asciimatics(res)


if __name__ == '__main__':
    main()
