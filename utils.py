import itertools
from heapq import heappop, heappush
from time import sleep

import numpy as np
from asciimatics.screen import ManagedScreen


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


# Grid could be a class, and get_neighbors one of its methods
def get_neighbors(point: tuple, grid: np.ndarray):
    """ Finds the neighboring points of the point of interest.

    :param point: The point whose neighbors are of interest, e.g. (0, 0).
    :param grid: A numpy array representing the grid the point is situated on.
    :returns: List with (up to 4) points next to provided point.
    """

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


def new_grid(dim: int = 64, fill: str = " "):
    """ Creates a new square grid.

    :param dim: The dimension of the side of the required square grid, defaults to 64.
    :param fill: A character representing each point in the grid, defaults to " ".
    :returns: A square ndarray with the required dimensions and fill.
    """
    return np.array([[f'{fill}' for _ in range(dim)] for _ in range(dim)])


def visualize_grid(grid, visited=None, path=None, start=None, goal=None, legend=True):
    grid = np.copy(grid)
    # symbols for grid visualization
    symbols = {"border": "+",
               "space": " ",
               "visited": "·",
               "path": "o",
               "start": "S",
               "goal": "G"}

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

    # add visual border at beginning and end of grid
    main_body = [symbols["space"].join([symbols["border"]] + list(row) + [symbols["border"]]) for row in grid]

    # add visual border at top and bottom of main body
    top = bottom = symbols["space"].join([symbols["border"]] * (len(grid) + 2))
    whole = [top] + main_body + [bottom]

    if legend:
        lgd = [f"{v} -> {k}" for k, v in symbols.items()]
        whole = whole + lgd

    return "\n".join(whole)


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
