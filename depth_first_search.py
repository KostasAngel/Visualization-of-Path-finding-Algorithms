from collections import deque

import utils


def calculate(grid, start, goal):
    # Create a double ended queue. By always appending to the right of the queue, and then considering the right-most
    # points in the queue first, the deque works as a LIFO queue/stack
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
    utils.visualize_asciimatics(res)


if __name__ == '__main__':
    main()
