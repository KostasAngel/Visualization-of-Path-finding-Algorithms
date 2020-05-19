from collections import deque

import utils


def calculate(grid, start, goal):
    queue = deque([start])  # double ended queue, to use as a FIFO queue

    visited = []

    child_parent_pairs = dict()

    goal_reached = False

    while queue and not goal_reached:  # stops when all points have been considered or when goal is reached

        current_point = queue.popleft()  # get leftmost point in queue

        visited.append(current_point)  # mark point as visited

        neighbors = utils.get_neighbors(current_point, grid)

        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in queue:  # check if already visited this point
                queue.append(neighbor)
                child_parent_pairs[neighbor] = current_point

                goal_reached = neighbor == goal  # check if goal has been reached

    path = utils.calculate_path(start, goal, child_parent_pairs)

    return {"path": path, "visited": visited, "grid": grid, "start": start, "goal": goal}


def main():
    grid = utils.new_grid(20)

    grid[:17, 4] = "+"
    grid[1, 1:9] = "+"
    grid[10, 6:18] = "+"
    grid[10:, 7] = "+"

    res = calculate(grid=grid, start=(0, 0), goal=(17, 17))
    utils.visualize_asciimatics(res)


if __name__ == '__main__':
    main()
