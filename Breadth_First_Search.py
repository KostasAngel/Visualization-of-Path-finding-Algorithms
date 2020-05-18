from collections import deque

import utils


def calculate_path(start, goal, child_parent_pairs):
    # if goal not in child_parent_pairs.values():
    #     raise AssertionError("No route to goal (goal not in child_parent_pairs)")
    reverse_path = [goal]
    while reverse_path[-1] != start:
        reverse_path.append(child_parent_pairs[reverse_path[-1]])

    return list(reversed(reverse_path))


# Grid could be a class, and get_neighbors one of its methods
def get_neighbors(point, grid):
    # possible movements, only up down left right, maybe diagonally should be an option?
    dy, dx = [-1, 0, 1, 0], [0, 1, 0, -1]

    neighbors = []
    for i in range(len(dy)):
        # possible neighbors
        y, x = point[0] + dy[i], point[1] + dx[i]

        # check if neighbors are within the grid
        if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
            if grid[y, x] == " ":
                neighbors.append((y, x))

    return neighbors


def main():
    grid_dim = 20
    grid = utils.new_grid(grid_dim)

    grid[:17, 4] = "+"
    grid[1, 1:9] = "+"
    grid[10, 6:18] = "+"
    grid[10:, 7] = "+"

    start = (0, 0)
    goal = (17, 17)

    # double ended queue, to use as a FIFO queue
    queue = deque([start])

    visited = []

    child_parent_pairs = dict()

    while queue:  # checks if queue is empty
        current_point = queue.popleft()

        visited.append(current_point)  # mark as visited

        neighbors = get_neighbors(current_point, grid)

        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in queue:  # check if already visited this point
                queue.append(neighbor)
                child_parent_pairs[neighbor] = current_point
                print(neighbor)

    print("Path to goal:", calculate_path(start, goal, child_parent_pairs))


if __name__ == '__main__':
    main()
