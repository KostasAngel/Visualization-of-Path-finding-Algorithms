from collections import deque

import utils


def calculate(grid, start, goal):
    # double ended queue, to use as a FIFO queue
    queue = deque([start])

    visited = []

    child_parent_pairs = dict()
    # todo stop when goal is reached
    while queue:  # checks if queue is empty, stops when all points have been considered
        current_point = queue.popleft()

        visited.append(current_point)  # mark as visited

        neighbors = utils.get_neighbors(current_point, grid)

        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in queue:  # check if already visited this point
                queue.append(neighbor)
                child_parent_pairs[neighbor] = current_point

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
