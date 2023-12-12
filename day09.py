import os
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)


def get_next_level(sequence):
    """
    >>> get_next_level([10, 13, 16, 21, 30, 45])
    [3, 3, 5, 9, 15]
    """
    return [b-a for a, b in zip(sequence, sequence[1:])]


def find_next_number(sequence):
    """
    >>> find_next_number([10, 13, 16, 21, 30, 45])
    68
    """
    if len(set(sequence)) == 1:
        return sequence[0]
    else:
        next_level = get_next_level(sequence)
        return sequence[-1] + find_next_number(next_level)


def as_list_of_ints(string):
    return [int(s) for s in string.split()]


sequences = load_input_lines(9, test=TEST, transform=as_list_of_ints)


def solve_a():
    return sum(find_next_number(sequence) for sequence in sequences)


def solve_b():
    reversed_sequences = [list(reversed(s)) for s in sequences]
    return sum(find_next_number(sequence) for sequence in reversed_sequences)


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
