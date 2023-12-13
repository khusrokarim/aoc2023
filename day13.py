import os
from helpers import load_input_lines, Matrix

TEST = os.environ.get("AOC_TEST", False)



def load_input_matrices(lines):
    pattern = []
    for line in lines:
        if not line:
            yield Matrix(pattern)
            pattern = []
        else:
            pattern.append(line)
    yield Matrix(pattern)


def find_reflection(sequences):
    """
    >>> strings = ["abc", "def", "ghi", "ghi", "def"]
    >>> find_reflection(strings)
    3
    >>> lists = [list(s) for s in strings]
    >>> find_reflection(lists)
    3
    """
    sequence_pairs = zip(sequences, sequences[1:])
    for divide_at, (sequence_1, sequence_2) in enumerate(sequence_pairs, start=1):
        if sequence_1 == sequence_2:
            before_reversed = list(reversed(sequences[:divide_at]))
            after = sequences[divide_at:]
            smaller_length = min(len(before_reversed), len(after))
            if before_reversed[:smaller_length] == after[:smaller_length]:
                return divide_at
    return 0


def find_horizontal_reflection(pattern):
    """
    >>> lines = load_input_lines(13, test=True)
    >>> _, pattern = list(load_input_matrices(lines))
    >>> find_horizontal_reflection(pattern)
    4
    """
    return find_reflection(pattern.rows)


def find_vertical_reflection(pattern):
    """
    >>> lines = load_input_lines(13, test=True)
    >>> pattern = next(load_input_matrices(lines))
    >>> find_vertical_reflection(pattern)
    5
    """
    return find_reflection(pattern.columns)


def solve_a():
    summary = 0
    input_lines = load_input_lines(13, test=TEST)
    patterns = load_input_matrices(input_lines)
    for pattern in patterns:
        summary += find_vertical_reflection(pattern)
        summary += 100 * find_horizontal_reflection(pattern)
    return summary


def solve_b():
    pass


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
