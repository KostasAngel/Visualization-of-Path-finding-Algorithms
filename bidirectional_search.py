from collections import deque

import utils


def calculate(start: tuple, goal: tuple, grid: utils.Grid = utils.Grid()):
    """ Finds path from start to goal using the Bidirectional Search algorithm.

    NOT FUNCTIONAL YET

    Starts to search from both start and goal simultaneously, performing Breadth-First search at both ends,
    until the two searches intersect.

    :param start: A tuple representing the starting point, e.g. (0, 0).
    :param goal: A tuple representing the goal point, e.g. (10, 10).
    :param grid: A Grid object representing the space where start and goal are located, optional.
    """

    queue_start, queue_goal = deque([start]), deque([goal])

    visited = [start, goal]

    child_parent_pairs = dict()

    found_path = False

    intersect_point = None

    while queue_start and queue_goal and not found_path:

        for i, [q, q_other] in enumerate(zip([queue_start, queue_goal], [queue_goal, queue_start])):
            if q:
                x = q.pop()
                if x == [goal, start][i] or x in q_other:
                    # success
                    found_path = True
                    intersect_point = x
                    print("intersect_point", intersect_point, flush=True)
                    # break
                for neighbor in grid.get_point_neighbors(x):
                    if neighbor not in visited:
                        visited.append(neighbor)
                        q.appendleft(neighbor)
                        child_parent_pairs[neighbor] = x

                        # if i == 0:
                        #     child_parent_pairs[neighbor] = x
                        # else:
                        #     child_parent_pairs[x] = neighbor

    start_to_intersect = utils.calculate_path(intersect_point, start, child_parent_pairs)
    goal_to_intersect = utils.calculate_path(goal, intersect_point, child_parent_pairs)

    path = start_to_intersect.extend(reversed(goal_to_intersect[:-1]))
    print(path)
    return {"path": path, "visited": visited, "grid": grid.to_ndarray(), "start": start, "goal": goal}


def main():
    # grid = utils.new_grid(20)
    #
    # grid[:17, 4] = "+"
    # grid[1, 1:9] = "+"
    # grid[10, 6:18] = "+"
    # grid[10:, 7] = "+"

    # the code here is just for testing, the program can just call calculate() above and skip this
    grid = utils.Grid(size=3)

    res = calculate(grid=grid, start=(0, 0), goal=(2, 2))

    # the following allows visualizing results in the terminal (thus only works when script is run from the terminal)
    utils.visualize_asciimatics(res)


if __name__ == '__main__':
    main()
