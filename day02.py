import re
import os
from math import prod
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)


limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def parse_game_id(line):
    """
    >>> parse_game_id("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")
    5
    """
    id_part, _ = line.split(":")
    _, game_id_str = id_part.split()
    return int(game_id_str)

def parse_cube_set(set_str):
    """
    >>> parse_cube_set("6 red, 1 blue, 3 green")["blue"]
    1
    """
    cube_set_dict = {}
    str_by_colour = set_str.strip().split(", ")
    for colour_str in str_by_colour:
        number_str, colour = colour_str.split()
        cube_set_dict[colour] = int(number_str)
    return cube_set_dict

def split_cube_set_strs(line):
    """
    >>> split_cube_set_strs("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")
    ['6 red, 1 blue, 3 green', '2 blue, 1 red, 2 green']
    """
    _, score_part = line.split(": ")
    return score_part.split("; ")

def parse_game(line):
    """
    >>> parse_game("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")["id"]
    5
    >>> parse_game("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")["cube_sets"][1]["green"]
    2
    """
    set_strs = split_cube_set_strs(line)
    sets = [parse_cube_set(set_str) for set_str in set_strs]
    parsed_game = {"id": parse_game_id(line), "cube_sets": sets}
    return parsed_game

def game_is_possible(game):
    """
    >>> game = parse_game("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")
    >>> game_is_possible(game)
    True
    >>> game = parse_game("Game 5: 16 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")
    >>> game_is_possible(game)
    False
    """
    for cube_set in game["cube_sets"]:
        for colour, number in cube_set.items():
            if limits[colour] < number:
                return False
    return True


def minimum_possible_set(game):
    """
    >>> game = parse_game("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")
    >>> minimum_possible_set(game)["red"]
    6
    >>> minimum_possible_set(game)["green"]
    3
    >>> minimum_possible_set(game)["blue"]
    2
    """
    min_set = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for cube_set in game["cube_sets"]:
        for colour, number in cube_set.items():
            min_set[colour] = max(min_set[colour], number)
    return min_set


def power(cube_set):
    return prod(cube_set.values())


def power_of_minimum_set(game):
    """
    >>> game = parse_game("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")
    >>> power_of_minimum_set(game)
    36
    """
    return power(minimum_possible_set(game))


input_games = load_input_lines(2, test=TEST, transform=parse_game)


def solve_a():
    possible_games = [game["id"] for game in input_games if game_is_possible(game)]
    return sum(possible_games)

def solve_b():
    return sum(
        power(minimum_possible_set(game))
        for game in input_games
    )


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
