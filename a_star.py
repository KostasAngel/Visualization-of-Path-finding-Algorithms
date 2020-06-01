import numpy as np

import heuristics
import utils


def calculate(grid: np.ndarray, start: tuple, goal: tuple, heuristic: str = "manhattan"):
    # temporary for backwards compatibility
    if start == (0, 0) and goal == (62, 62):
        return calculate2(start, goal, utils.Grid(create_maze=True), heuristic)
    else:
        return calculate2(start, goal, utils.Grid(custom_grid=grid), heuristic)


def calculate2(start: tuple, goal: tuple, grid: utils.Grid = utils.Grid(), heuristic: str = "manhattan"):
    """ Finds path from start to goal using the A* algorithm.

    Implementation of this algorithm was based on the example provided in Wikipedia:
    https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

    :param grid: A numpy array representing the grid where start and goal are located.
    :param start: A tuple representing the starting point, e.g. (0, 0).
    :param goal: A tuple representing the goal point, e.g. (10, 10).
    :param heuristic: The heuristic the algorithm will use, defaults to the Manhattan distance. Currently options
     "manhattan" and "euclidean" are supported.
    """

    if heuristic == "manhattan":
        h_score = heuristics.manhattan_distance
    elif heuristic == "euclidean":
        h_score = heuristics.euclidean_distance
    else:
        raise NameError("Heuristic name provided not applicable/erroneous.")

    visited = []

    child_parent_pairs = dict()

    g_scores = dict()
    g_scores[start] = 0

    f_scores = dict()  # the f_score is calculated by f(n) = g(n) + h(n)
    f_scores[start] = g_scores[start] + h_score(start, goal)  # the g_score of start is 0

    # create a priority queue, and add start to it; priority in A* corresponds to the fScore, and the points with
    # lowest fScores are considered first
    pq = utils.PriorityQueue()
    pq.add_point(start, f_scores[start])

    while pq.has_points():
        # get point with lowest priority and remove from queue
        current_point = pq.get_lowest_priority_point()

        visited.append(current_point)

        if current_point == goal:
            # goal has been reached
            # do not return from here, by returning below the case where no path is found is captured
            break

        for neighbor in grid.get_point_neighbors(current_point):
            tentative_g_score = g_scores[current_point] + 1  # neighbors always 1 step away from current
            if neighbor in g_scores and g_scores[neighbor] < tentative_g_score:
                # neighbor already reached from another point that resulted in a lower g_score, so skip it
                continue

            # path to this neighbor is better than any previous, so record it
            child_parent_pairs[neighbor] = current_point
            g_scores[neighbor] = tentative_g_score
            f_scores[neighbor] = tentative_g_score + h_score(neighbor, goal)
            pq.add_point(neighbor, f_scores[neighbor])

    path = utils.calculate_path(start, goal, child_parent_pairs)

    return {"path": path, "visited": visited, "grid": grid.to_ndarray(), "start": start, "goal": goal}


def main():
    # the code here is just for testing, the program can just call calculate() above and skip this
    grid = utils.new_grid(20)

    grid[:17, 4] = "+"
    grid[1, 1:9] = "+"
    grid[10, 6:18] = "+"
    grid[10:, 7] = "+"

    res = calculate(grid=grid, start=(0, 0), goal=(17, 17), heuristic="manhattan")

    # the following allows visualizing results in the terminal (thus only works when script is run from the terminal)
    utils.visualize_asciimatics(res)


if __name__ == '__main__':
    main()
