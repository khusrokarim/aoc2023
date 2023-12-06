import os
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)

input_lines = load_input_lines(1, test=TEST)

numbers = {
    **{str(i):str(i) for i in range(1,10)},
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def find_first(s, numbers=numbers):
    indices = {s.find(n): numbers[n] for n in numbers if s.find(n) > -1}
    first_index = min(indices)
    return indices[first_index]


def find_last(s):
    reversed_numbers = {k[::-1]: v for k, v in numbers.items()}
    reversed_s = s[::-1]
    return find_first(reversed_s, numbers=reversed_numbers)


def get_number_for_line(s):
    first_digit_str = find_first(s)
    last_digit_str = find_last(s)
    # indices = {s.find(n): numbers[n] for n in numbers if s.find(n) > -1}
    # first_index, last_index = min(indices), max(indices)
    # first_digit_str = indices[first_index]
    # last_digit_str = indices[last_index]
    # print(s, first_digit_str, last_digit_str)
    return int(first_digit_str + last_digit_str)


def solve_a():
    # running_total = 0
    # for line in input_lines:
    #     first_digit = next(c for c in line if c.isdigit())
    #     last_digit = next(c for c in reversed(line) if c.isdigit())
    #     running_total += int(first_digit + last_digit)
    # return running_total
    pass


def solve_b():
    return sum(get_number_for_line(l) for l in input_lines)


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
