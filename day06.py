import os
from math import ceil, prod, sqrt
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)

def number_of_winning_times(race_time, winning_distance):
    """
    Speed = charge_time.  Time = race_time - charge_time.
    So distance_travelled = charge_time * (race_time - charge_time).
    This is a quadratic equation.
    A charge_time will beat prev_winning_distance if:
    -charge_time^2 + race_time*charge_time - prev_winning_distance > 0

    >>> number_of_winning_times(7, 9)
    4
    >>> number_of_winning_times(15, 40)
    8
    >>> number_of_winning_times(30, 200)
    9
    """
    numerator_offset = sqrt((race_time**2) - (4*winning_distance))
    first_charge_time = (race_time + numerator_offset)/2.0
    second_charge_time = (race_time - numerator_offset)/2.0
    smaller_time, bigger_time = sorted((first_charge_time, second_charge_time))

    bracket_start, bracket_end_excl = int(smaller_time + 1), int(bigger_time + 1)
    if bracket_end_excl == bigger_time + 1:
        # This means we match the winning time; we need to beat it
        bracket_end_excl -= 1
    return bracket_end_excl - bracket_start


def load_races_part_a(test=TEST):
    """
    >>> list(load_races_part_a(test=True))
    [(7, 9), (15, 40), (30, 200)]
    """
    time_line, distance_line = load_input_lines(6, test=test)
    times = [int(time) for time in time_line.split()[1:]]
    distances = [int(distance) for distance in distance_line.split()[1:]]
    return zip(times, distances)


def parse_line_part_b(line):
    """
    >>> input_line = "Time:      7  15   30"
    >>> parse_line_part_b(input_line)
    71530
    """
    number_part = line.split()[1:]
    return int("".join(number_part))


def load_races_part_b(test=TEST):
    return load_input_lines(6, test=TEST, transform=parse_line_part_b)


def solve_a():
    product = 1
    for time, distance in load_races_part_a(test=TEST):
        product *= number_of_winning_times(time, distance)
    return product


def solve_b():
    return number_of_winning_times(*load_races_part_b())



if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
