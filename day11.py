import os
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)

def mark_vertical_expansion(lines):
    """
    >>> l = ["...#", "....", "#..."]
    >>> list(mark_vertical_expansion(l))
    ['...#', 'vvvv', '#...']
    """
    lines = list(lines)
    width = len(lines[0])
    for line in lines:
        if "#" not in line:
            line = line.replace(">", "x").replace(".", "v")
        yield line


def columns(lines):
    """
    >>> l = ["...#", "....", "#..."]
    >>> list(columns(l))
    ['..#', '...', '...', '#..']
    """
    lines = list(lines)
    width = len(lines[0])
    for i in range(width):
        yield "".join(line[i] for line in lines)


def mark_horizontal_expansion(lines):
    """
    >>> l = ["...#", "....", "#..."]
    >>> list(mark_horizontal_expansion(l))
    ['.>>#', '.>>.', '#>>.']
    """
    lines = list(lines)
    marked_columns = []
    for column in columns(lines):
        if "#" not in column:
            column = column.replace("v", "x").replace(".", ">")
        marked_columns.append(column)

    height = len(lines)
    for i in range(height):
        yield "".join(column[i] for column in marked_columns)


def find_x_coordinates(line, expand_by=1):
    """
    >>> list(find_x_coordinates("#....#......."))
    [0, 5]
    >>> list(find_x_coordinates("#.>..#......."))
    [0, 6]
    >>> list(find_x_coordinates("#.>v.#.......", expand_by=5))
    [0, 10]
    >>> list(find_x_coordinates("#.>vx#...v...", expand_by=5))
    [0, 15]
    """
    x_index = 0
    for character in line:
        if character == "#":
            yield x_index
        elif character in ">x":
            x_index += expand_by
        x_index += 1


def get_coordinates(lines, expand_by=1):
    """
    >>> l = ["...#", "....", "#..."]
    >>> list(get_coordinates(l))
    [(3, 0), (0, 2)]
    >>> l = [".>.#", ".>..", "#>.."]
    >>> list(get_coordinates(l))
    [(4, 0), (0, 2)]
    >>> l = [".>.#", "vxvv", "#>.."]
    >>> list(get_coordinates(l))
    [(4, 0), (0, 3)]
    >>> list(get_coordinates(l, expand_by=2))
    [(5, 0), (0, 4)]
    """
    line_number = 0
    lines = list(lines)
    all_x_coords = [find_x_coordinates(line, expand_by=expand_by) for line in lines]

    for line, x_coords in zip(lines, all_x_coords):
        if line[0] in "vx":
            line_number += expand_by
        else:
            for x in x_coords:
                yield (x, line_number)
        line_number += 1


def load_galaxies(expand_by=1):
    raw_map_lines = load_input_lines(11, test=TEST)
    map_marked_vertically = mark_vertical_expansion(raw_map_lines)
    map_marked = mark_horizontal_expansion(map_marked_vertically)
    galaxy_coordinates = get_coordinates(map_marked, expand_by=expand_by)
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
    total_distance = 0
    galaxies = load_galaxies(expand_by=999999)
    pairs = unique_pairs(galaxies)
    return sum(distance(*pair) for pair in pairs)


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
