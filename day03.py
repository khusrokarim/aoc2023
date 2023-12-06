import re
import os
from math import prod
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)

schematic = load_input_lines(3, test=TEST)


def get_vertical_neighbours(neighbouring_line, number_start_i, number_end_i):
    """
    >>> get_vertical_neighbours("...*.S...E.", 6, 9)
    'S...E'
    >>> get_vertical_neighbours("...*.S...E.", 0, 3)
    '...*'
    """
    start_i = max(number_start_i-1, 0)
    end_i = number_end_i+1
    return neighbouring_line[start_i:end_i]


def find_numbers_with_neighbours(lines):
    """
    >>> schematic = load_input_lines(3, test=True)
    >>> numbers_with_neighbours = find_numbers_with_neighbours(schematic)
    >>> numbers_with_neighbours[0]
    {'number': 467, 'neighbours': '....*'}
    >>> numbers_with_neighbours[-1]
    {'number': 598, 'neighbours': '.*.....'}
    >>> numbers_with_neighbours[2]
    {'number': 35, 'neighbours': '..*.......'}
    >>> numbers_with_neighbours[3]
    {'number': 633, 'neighbours': '........#...'}
    """
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1
    matched_numbers = []

    for line_number, line in enumerate(lines):
        for number_match in re.finditer(r"\d+", line):
            x_start, x_end = number_match.span()
            line_above = lines[line_number-1] if line_number > 0 else None
            line_below = lines[line_number+1] if line_number < max_y else None

            neighbours = ""

            if line_above:
                neighbours += get_vertical_neighbours(line_above, x_start, x_end)
            if x_start > 0:
                neighbours += line[x_start-1]
            if x_end <= max_x:
                neighbours += line[x_end]
            if line_below:
                neighbours += get_vertical_neighbours(line_below, x_start, x_end)
            matched_numbers.append({"number": int(number_match.group()), "neighbours": neighbours})

    return matched_numbers


def contains_symbol(s):
    """
    >>> contains_symbol("...234...")
    False
    >>> contains_symbol("*..234...")
    True
    """
    return any(c not in ".1234567890" for c in s)


def get_part_numbers(numbers_with_neighbours):
    """
    >>> schematic = load_input_lines(3, test=True)
    >>> numbers_with_neighbours = find_numbers_with_neighbours(schematic)
    >>> part_numbers = get_part_numbers(numbers_with_neighbours)
    >>> part_numbers[0]
    467
    """
    return [
        n["number"] for n in numbers_with_neighbours
        if contains_symbol(n["neighbours"])
    ]


def get_number_locations(lines):
    """
    >>> schematic = load_input_lines(3, test=True)
    >>> locations = get_number_locations(schematic)
    >>> locations[0]["number"]
    467
    >>> locations[0]["locations"]
    [(0, 0), (1, 0), (2, 0)]
    """
    locations = []
    for line_number, line in enumerate(lines):
        for number_match in re.finditer(r"\d+", line):
            locations.append({
                "number": int(number_match.group()),
                "locations": [
                    (x, line_number)
                    for x in range(*number_match.span())
                ],
            })
    return locations


def get_star_locations(lines):
    """
    >>> schematic = load_input_lines(3, test=True)
    >>> locations = get_star_locations(schematic)
    >>> locations[0]
    (3, 1)
    """
    locations = []
    for line_number, line in enumerate(lines):
        for star_match in re.finditer(r"\*", line):
            locations.append((star_match.start(), line_number))
    return locations


def is_neighbour(location_1, location_2):
    """
    >>> is_neighbour((2, 3), (1, 3))
    True
    >>> is_neighbour((2, 3), (3, 4))
    True
    >>> is_neighbour((2, 3), (4, 3))
    False
    """
    x1, y1 = location_1
    x2, y2 = location_2
    return (
        (-1 <= (x1-x2) <= 1)
        and (-1 <= (y1-y2) <= 1)
        and (location_1 != location_2)
    )


def string_is_neighbour(location_1, string_locations):
    """
    >>> schematic = load_input_lines(3, test=True)
    >>> number_locations = get_number_locations(schematic)
    >>> string_is_neighbour((3, 1), number_locations[0]["locations"])
    True
    >>> string_is_neighbour((3, 1), number_locations[1]["locations"])
    False
    """
    return any(
        is_neighbour(location_1, location)
        for location in string_locations
    )


def is_gear(star_location, number_locations):
    """
    >>> schematic = load_input_lines(3, test=True)
    >>> number_locations = get_number_locations(schematic)
    >>> is_gear((3, 1), number_locations)
    {'is_gear': True, 'gear_ratio': 16345}
    >>> is_gear((3, 4), number_locations)
    {'is_gear': False, 'gear_ratio': 0}
    >>> is_gear((5, 8), number_locations)
    {'is_gear': True, 'gear_ratio': 451490}
    """
    neighbouring_numbers = [
        number_location["number"]
        for number_location in number_locations
        if string_is_neighbour(star_location, number_location["locations"])
    ]
    is_gear = len(neighbouring_numbers) == 2
    gear_ratio = prod(neighbouring_numbers) if is_gear else 0
    return {
        'is_gear': is_gear,
        'gear_ratio': gear_ratio,
    }



def solve_a():
    numbers_with_neighbours = find_numbers_with_neighbours(schematic)
    part_numbers = get_part_numbers(numbers_with_neighbours)
    return sum(part_numbers)


def solve_b():
    star_locations = get_star_locations(schematic)
    number_locations = get_number_locations(schematic)
    gear_ratios = [
        gear_ratio := is_gear(location, number_locations)["gear_ratio"]
        for location in star_locations
    ]
    return sum(gear_ratios)


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
