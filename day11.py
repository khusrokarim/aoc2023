import os
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)


def expand_vertically(lines):
    """
    >>> l = ["...#", "....", "#..."]
    >>> list(expand_vertically(l))
    ['...#', '....', '....', '#...']
    """
    for line in lines:
        yield line
        if set(line) == {"."}:
            yield line


def columns(lines):
    """
    >>> l = ["...#", "....", "#..."]
    >>> ["".join(c) for c in list(columns(l))]
    ['..#', '...', '...', '#..']
    """
    lines = list(lines)
    width = len(lines[0])
    for i in range(width):
        yield [line[i] for line in lines]


def expand_horizontally(lines):
    """
    >>> l = ["...#", "....", "#..."]
    >>> list(expand_horizontally(l))
    ['.....#', '......', '#.....']
    """
    expanded_columns = []
    for column in columns(lines):
        expanded_columns.append(column)
        if set(column) == {"."}:
            expanded_columns.append(column)

    height = len(expanded_columns[0])
    for i in range(height):
        yield "".join(column[i] for column in expanded_columns)


def find_galaxy_x_coordinates(lines):
    """
    >>> list(find_galaxy_x_coordinates(["#....#.......", ".#..........."]))
    [[0, 5], [1]]
    """
    for line in lines:
        yield [x for x, galaxy in enumerate(line) if galaxy == "#"]


def append_galaxy_y_coordinates(x_coords_by_line):
    """
    >>> list(append_galaxy_y_coordinates([[9], [0, 4]]))
    [(9, 0), (0, 1), (4, 1)]
    """
    for y, line in enumerate(x_coords_by_line):
        for x in line:
            yield (x, y)


def load_galaxies():
    raw_map_lines = load_input_lines(11, test=TEST)
    map_expanded_vertically = expand_vertically(raw_map_lines)
    map_expanded = expand_horizontally(map_expanded_vertically)
    x_coordinates = find_galaxy_x_coordinates(map_expanded)
    galaxy_coordinates = append_galaxy_y_coordinates(x_coordinates)
    return list(galaxy_coordinates)


def unique_pairs(galaxies):
    """
    >>> list(unique_pairs([(9, 0), (0, 1), (4, 1)]))
    [((9, 0), (0, 1)), ((9, 0), (4, 1)), ((0, 1), (4, 1))]
    """
    galaxies = list(galaxies)
    number_of_galaxies = len(galaxies)
    for i in range(number_of_galaxies - 1):
        for j in range(i+1, number_of_galaxies):
            yield (galaxies[i], galaxies[j])


def distance(galaxy_1, galaxy_2):
    """
    >>> distance((1, 6), (5, 11))
    9
    """
    x1, y1 = galaxy_1
    x2, y2 = galaxy_2
    return abs(x1-x2) + abs(y1-y2)


def solve_a():
    total_distance = 0
    galaxies = load_galaxies()
    pairs = unique_pairs(galaxies)
    return sum(distance(*pair) for pair in pairs)


def solve_b():
    pass


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
