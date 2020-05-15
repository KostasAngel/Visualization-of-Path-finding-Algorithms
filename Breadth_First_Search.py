import curses
import time
from collections import defaultdict, deque

import utils


# inspired by this gist: https://gist.github.com/hrldcpr/2012250
def tree(): return defaultdict(tree)


# Grid could be a class, and get_neighbors one of its methods
def get_neighbors(point, grid):
    # possible movements, only up down left right, maybe diagonally should be an option?
    dy, dx = [-1, 0, 1, 0], [0, 1, 0, -1]

    neighbors = []
    for i in range(4):
        # possible neighbors
        y, x = point[0] + dy[i], point[1] + dx[i]

        # check if neighbors are within the grid, skip if not
        if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
            if grid[y, x] == " ":
                neighbors.append((y, x))

    return neighbors


def main():
    # to store visited points, and allow to determine the shortest path at the end
    traversed_tree = tree()
    grid_dim = 10
    grid = utils.new_grid(grid_dim)

    grid[:9, 4] = "+"
    grid[1, 1:9] = "+"
    grid[3, 6:] = "+"

    start = (0, 0)
    goal = (9, 9)

    # double ended queue, to use as a FIFO queue
    q = deque([start])

    visited = []

    screen = curses.initscr()

    while q:  # checks if q is empty
        current_point = q.popleft()

        visited.append(current_point)  # mark as visited

        neighbors = get_neighbors(current_point, grid)

        for neighbor in neighbors:

            if neighbor not in visited:  # check if already visited this point
                if neighbor not in q:
                    q.append(neighbor)

                    screen.clear()
                    screen.addstr(utils.visualize_grid(grid, visited))
                    screen.refresh()
                    time.sleep(0.05)


if __name__ == '__main__':
    main()
