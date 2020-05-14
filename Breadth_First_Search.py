from collections import defaultdict
from collections import deque


def new_grid(dim):
    return [["." for _ in range(dim)] for _ in range(dim)]


# inspired by this gist: https://gist.github.com/hrldcpr/2012250
def tree(): return defaultdict(tree)


def get_neighbors(point, grid):
    # possible movements, only up down left right, maybe diagonally should be an option?
    dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]

    neighbors = []
    for i in range(4):
        # possible neighbors
        x, y = point[0] + dx[i], point[1] + dy[i]

        # check if neighbors are within the grid, skip if not
        if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
            continue

        neighbors.append((x, y))

    return neighbors


def main():
    # to store visited points, and allow to determine the shortest path at the end
    traversed_tree = tree()

    # double ended queue, to use as a FIFO queue
    q = deque()

    print(new_grid(4))


if __name__ == '__main__':
    main()
