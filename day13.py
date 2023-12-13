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


def is_possible_reflection(sequence_1, sequence_2, smudge):
    if smudge:
        matching = [s1 == s2 for s1, s2 in zip(sequence_1, sequence_2)]
        return matching.count(False) == 1
    else:
        return sequence_1 == sequence_2


def is_reflection(sequences, divide_at, smudge):
    before_reversed = list(reversed(sequences[:divide_at]))
    after = sequences[divide_at:]
    smudge_needed = smudge
    for sequence_1, sequence_2 in zip(before_reversed, after):
        # If we're looking for a smudge and there is one on this line, we no longer need a smudge
        if smudge_needed and is_possible_reflection(sequence_1, sequence_2, smudge=True):
            smudge_needed = False
        # If we're not looking for a smudge, this needs to be a straightforward reflection
        elif (not smudge_needed) and (not is_possible_reflection(sequence_1, sequence_2, smudge=False)):
            return False

    # If we reach this line, we either don't need a smudge and have found a simple reflection (good)
    # Or we do need a smudge and we haven't found one (bad)
    return not smudge_needed



def find_reflection(sequences, smudge):
    """
    >>> strings = ["abc", "def", "ghi", "ghi", "def"]
    >>> find_reflection(strings, smudge=False)
    3
    >>> lists = [list(s) for s in strings]
    >>> find_reflection(lists, smudge=False)
    3
    """
    sequence_pairs = zip(sequences, sequences[1:])
    for divide_at, (sequence_1, sequence_2) in enumerate(sequence_pairs, start=1):
        check_for_reflection = is_possible_reflection(sequence_1, sequence_2, smudge=False)
        if smudge:
            check_for_reflection = (
                check_for_reflection
                or is_possible_reflection(sequence_1, sequence_2, smudge=True)
            )
        if check_for_reflection and is_reflection(sequences, divide_at, smudge=smudge):
            return divide_at
    return 0


def find_horizontal_reflection(pattern, smudge=False):
    """
    >>> lines = load_input_lines(13, test=True)
    >>> pattern_1, pattern_2 = list(load_input_matrices(lines))
    >>> find_horizontal_reflection(pattern_2)
    4
    >>> find_horizontal_reflection(pattern_1, smudge=True)
    3
    >>> find_horizontal_reflection(pattern_2, smudge=True)
    1
    """
    return find_reflection(pattern.rows, smudge)


def find_vertical_reflection(pattern, smudge=False):
    """
    >>> lines = load_input_lines(13, test=True)
    >>> pattern = next(load_input_matrices(lines))
    >>> find_vertical_reflection(pattern)
    5
    """
    return find_reflection(pattern.columns, smudge)


def solve(smudge):
    summary = 0
    input_lines = load_input_lines(13, test=TEST)
    patterns = load_input_matrices(input_lines)
    for pattern in patterns:
        summary += find_vertical_reflection(pattern, smudge)
        summary += 100 * find_horizontal_reflection(pattern, smudge)
    return summary


def solve_a():
    return solve(smudge=False)

def solve_b():
    return solve(smudge=True)


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
