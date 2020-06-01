import itertools
import random
from collections import deque
from heapq import heappop, heappush
from time import sleep

import numpy as np
from asciimatics.screen import ManagedScreen


class Grid(object):
    EMPTY, WALL = 0, 1

    def __init__(self, custom_grid: np.ndarray = None, size: int = 64, create_maze: bool = False,
                 start: tuple = (0, 0), random_seed: int = None):
        """ Create a grid object.

        Essentially a 2D array representing the space on which path-finding will work. Zeros represent empty spaces
        and ones represent walls.

        :param custom_grid: A numpy array representing a custom grid. The array should be square, with zeros
         representing empty spaces and ones walls or other obstacles. If custom_grid is specified, all other input
         parameters are ignored.
        :param size: Optional number denoting the side length of a new empty square grid.
        :param create_maze: If True, the generated grid object contains a random maze.
        :param start: The start point on the grid, to make sure it is located in a corridor, in the case where a
         random maze is requested.
        :param random_seed: When provided, the generated maze produced is always the same, for reproducible results.
        """
        self.maze_history = []

        if custom_grid is not None:
            # create grid from provided numpy array
            self.grid = np.copy(custom_grid)  # copy provided array to prevent changes on it from elsewhere
        else:
            # create empty grid
            self.grid = np.zeros(shape=(size, size), dtype=int)

            if create_maze:  # uses the DFS algorithm to create random mazes

                if random_seed is not None:
                    random.seed(random_seed)

                self.grid[:, :] = Grid.WALL  # mark all points as walls

                queue = deque([start])

                child_parent_pairs = dict()

                while queue:
                    current_point = queue.pop()
                    if current_point != start:
                        parent = child_parent_pairs[current_point]
                        in_between_point = tuple(p + (c - p) // 2 for p, c in zip(parent, current_point))
                        self.maze_history.append(in_between_point)
                        # mark point in between current and its parent as corridor
                        self.grid[in_between_point] = Grid.EMPTY

                    self.grid[current_point] = Grid.EMPTY  # mark as corridor
                    self.maze_history.append(current_point)

                    neighbors = self.get_point_neighbors(current_point, d=2)
                    random.shuffle(neighbors)
                    for neighbor in neighbors:  # shuffle neighbors so next popped will be random
                        child_parent_pairs[neighbor] = current_point
                        queue.append(neighbor)

    def to_ndarray(self):
        """ Returns the grid as numpy array.

        :return: A 2D ndarray representing the grid.
        """
        return self.grid

    def get_maze_history(self):
        """
        TODO
        :return:
        """
        return self.maze_history

    def get_point_neighbors(self, point: tuple, d: int = 1):
        """ Finds the orthogonally neighboring points of the point provided.

        :param point: The point whose neighbors on the grid are of interest, e.g. (0, 0).
        :param d: Distance to neighbors required, for path-finding should always be 1 (the default). d=2 is used
         internally to create mazes.
        :return: List of up to 4 points adjacent to the provided point.
        """

        # possible movements, only up down left right, maybe diagonally should be an option?
        dy, dx = [-d, 0, d, 0], [0, d, 0, -d]

        neighbors = []
        for i in range(len(dy)):
            # possible neighbors
            y, x = point[0] + dy[i], point[1] + dx[i]

            # check if neighbors are within the grid
            if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
                # check if neighbors are valid
                if self.grid[y, x] == Grid.EMPTY and d == 1:  # immediate neighbors
                    neighbors.append((y, x))
                elif self.grid[y, x] == Grid.WALL and d == 2:  # neighbors at distance = 2, used when creating mazes
                    neighbors.append((y, x))

        return neighbors


class PriorityQueue(object):
    """ Priority queue that supports setting the priority of entries,
    allows updating of entries, and has built-in tie-breaking capabilities,
    i.e. when two entries have the same priority, the one added earlier is
    returned.

    Since it is not easy to replace an entry in the heap, they are
    instead marked as REMOVED in the separate entry_finder dictionary,
    and an updated entry is placed in the heap. REMOVED entries are
    filtered out when they are popped from the heap, and are found to
    be marked as such.

    A counter is used to mark when each entry was inserted in the queue,
    so that when more than one points have equal priority, the one
    inserted first is returned.

    Based on a combination of the following examples:

    - https://stackoverflow.com/a/407922
    - https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    """

    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()
        self.REMOVED = '<removed-task>'

    def add_point(self, point: tuple, priority: float = 0):
        """ Adds point to the priority queue, if it doesn't already
        exist in it. If the point already exists, the old entry is
        marked as removed, and the point is re-added to the queue.

        :param point: Point to be added in the queue.
        :param priority: Priority of the point, e.g. for A* this is
         equivalent to the fScore.
        """
        if point in self.entry_finder:
            self.remove_point(point)
        count = next(self.counter)
        entry = [priority, count, point]
        self.entry_finder[point] = entry
        heappush(self.pq, entry)

    def contains_point(self, point: tuple):
        """ Returns whether a point is still in the queue.

        :param point: Point to be checked if still in queue.
        """
        return point in self.entry_finder

    def get_lowest_priority_point(self):
        """ Removes and returns the point with the lowest priority in
        the queue.

        In case of multiple points with equal priority, the one entered
        first is returned.

        :raises: KeyError if priority queue is empty
        """
        while self.pq:
            priority, count, point = heappop(self.pq)
            if point is not self.REMOVED:
                del self.entry_finder[point]
                return point
        raise KeyError("Pop from empty priority queue")

    def has_points(self):
        return len(self.entry_finder) != 0

    def remove_point(self, point):
        # For internal use in the class. "Removing" an entry from the priority queue is done simply by marking it
        # REMOVED. Doing so relies on the fact that an entry in entry_finder is the exact same in memory as the one in
        # the heap, so by editing it here, it is edited in the heap as well.
        entry = self.entry_finder.pop(point)
        entry[-1] = self.REMOVED


def calculate_path(start, goal, child_parent_pairs):
    """ Calculates the path to the goal from a child-parent dictionary.

    :param dict child_parent_pairs: Dictionary containing information
    :param tuple goal: Coordinates of goal point, e.g. (5, 5)
    :param tuple start: Coordinates of start point, e.g. (0, 0)
    :returns: List of points (tuples), from start to goal
    """

    # TODO is there a better way to check this?
    if goal not in child_parent_pairs.keys():
        raise AssertionError("No route to goal (goal not in child_parent_pairs)")

    reverse_path = [goal]

    while reverse_path[-1] != start:
        reverse_path.append(child_parent_pairs[reverse_path[-1]])

    return list(reversed(reverse_path))


def new_grid(dim: int = 64, fill: str = " "):
    """ Creates a new square grid.
    TODO delete since it functionality is implemented in Grid class
    :param dim: The dimension of the side of the required square grid, defaults to 64.
    :param fill: A character representing each point in the grid, defaults to " ".
    :returns: A square ndarray with the required dimensions and fill.
    """
    return np.array([[f'{fill}' for _ in range(dim)] for _ in range(dim)])


def visualize_grid(grid, visited=None, path=None, start=None, goal=None, legend=True):
    if type(grid) is Grid:
        grid = np.copy(grid.to_ndarray())
    else:
        grid = np.copy(grid)

    grid = grid.astype(str)

    # symbols for grid visualization
    symbols = {"border": "+",
               "space": " ",
               "visited": "·",
               "path": "o",
               "start": "S",
               "goal": "G"}

    # mark walls and empty spaces
    grid[grid == f"{Grid.WALL}"] = symbols["border"]
    grid[grid == f"{Grid.EMPTY}"] = symbols["space"]

    # mark the points visited
    if visited:
        for p in visited:
            grid[p] = symbols["visited"]

    # draw path if provided
    if path:
        for p in path:
            grid[p] = symbols["path"]

    # draw start and goal
    if start:
        grid[start] = symbols["start"]
    if goal:
        grid[goal] = symbols["goal"]

    # draw border
    grid = np.pad(grid, 1, mode="constant", constant_values=symbols["border"])  # add border around grid

    # convert to string
    main_body = [symbols["space"].join(row) for row in grid]

    if legend:
        lgd = [f"{v} -> {k}" for k, v in symbols.items()]
        main_body = main_body + lgd

    return "\n".join(main_body)


def visualize_asciimatics(res):
    with ManagedScreen() as screen:
        # print visited one by one
        for i in range(1, len(res["visited"])):
            grid = visualize_grid(res["grid"], visited=res["visited"][:i + 1], start=res["start"], goal=res["goal"])

            for j, row in enumerate(grid.split("\n")):
                screen.print_at(row, 0, j)
            screen.refresh()
            sleep(0.03)
        # print path
        grid = visualize_grid(res["grid"], visited=res["visited"], path=res["path"], start=res["start"],
                              goal=res["goal"])
        for j, row in enumerate(grid.split("\n")):
            screen.print_at(row, 0, j)

        screen.refresh()
        sleep(20)


def visualize_maze_creation(grid: Grid):
    full_grid = np.copy(grid.to_ndarray())
    full_grid[:, :] = Grid.WALL
    with ManagedScreen() as screen:
        for point in grid.get_maze_history():
            full_grid[point] = Grid.EMPTY
            g = visualize_grid(grid=full_grid)

            for j, row in enumerate(g.split("\n")):
                screen.print_at(row, 0, j)
            screen.refresh()
            sleep(0.005)
    sleep(20)
