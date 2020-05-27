import math

import utils


def calculate(grid, start, goal, h="manhattan"):
    """ Finds path from start to goal using the A* algorithm.

    Implementation of this algorithm was based on the example provided in Wikipedia:
    https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

    :param grid: A numpy array representing the grid where start and goal are located.
    :param start: A tuple representing the starting point, e.g. (0, 0).
    :param goal: A tuple representing the goal point, e.g. (10, 10).
    :param h: The heuristic the algorithm will use, defaults to the Manhattan distance. Currently options "manhattan"
     and "euclidean" are supported.
    """

    if h == "manhattan":
        h_score = manhattan_distance
    elif h == "euclidean":
        h_score = euclidean_distance
    else:
        raise NameError("Heuristic name provided not applicable/erroneous.")

    visited = []

    child_parent_pairs = dict()

    g_scores = dict()
    g_scores[start] = 0

    f_scores = dict()  # the f_score is calculated by f(n) = g(n) + h(n)
    f_scores[start] = g_scores[start] + h_score(start, goal)  # the g_score of start is 0

    pq = utils.PriorityQueue()
    pq.add_point(start, f_scores[start])  # add start to priority queue, priority in A* corresponds to the fScore

    while pq.has_points():
        # get point with lowest priority and remove from queue
        current_point = pq.get_lowest_priority_point()

        visited.append(current_point)

        if current_point == goal:
            path = utils.calculate_path(start, goal, child_parent_pairs)
            return {"path": path, "visited": visited, "grid": grid, "start": start, "goal": goal}

        for neighbor in utils.get_neighbors(current_point, grid):
            tentative_g_score = g_scores[current_point] + 1  # neighbors always 1 step away from current
            if neighbor in g_scores and g_scores[neighbor] < tentative_g_score:
                # neighbor already reached from another point that resulted in a lower g_score, so skip it
                continue

            # path to this neighbor is better than any previous, so record it
            child_parent_pairs[neighbor] = current_point
            g_scores[neighbor] = tentative_g_score
            f_scores[neighbor] = tentative_g_score + h_score(neighbor, goal)
            pq.add_point(neighbor, f_scores[neighbor])


def manhattan_distance(a: tuple, b: tuple):
    """ Calculates the Manhattan distance between two points.

    Manhattan distance on Wikipedia: https://en.wikipedia.org/wiki/Taxicab_geometry
    """
    return sum(abs(i - j) for i, j in zip(a, b))


def euclidean_distance(a: tuple, b: tuple):
    """ Calculates the Euclidean distance between two points.

    Euclidean distance on Wikipedia: https://en.wikipedia.org/wiki/Euclidean_distance
    """
    return math.sqrt(sum((i - j) ** 2 for i, j in zip(a, b)))


def main():
    # the code here is just for testing, the program can just call calculate() above and skip this
    grid = utils.new_grid(20)

    grid[:17, 4] = "+"
    grid[1, 1:9] = "+"
    grid[10, 6:18] = "+"
    grid[10:, 7] = "+"

    res = calculate(grid=grid, start=(0, 0), goal=(17, 17), h="manhattan")
    utils.visualize_asciimatics(res)


if __name__ == '__main__':
    main()
