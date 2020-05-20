import math

import utils


def calculate():
    pass


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
    grid = utils.new_grid()
    print(euclidean_distance((0, 0), (1, 0)))


if __name__ == '__main__':
    main()
