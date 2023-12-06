import os
import re
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)


def parse_card(line):
    """
    >>> card_line = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    >>> card = parse_card(card_line)
    >>> card["card_id"]
    1
    >>> card["winning_numbers"] == {41, 48, 83, 86, 17}
    True
    >>> card["my_numbers"] == {83, 86, 6, 31, 17, 9, 48, 53}
    True
    """
    pattern = r"Card +(?P<card_id>\d+): +(?P<winning_str>[0-9 ]+)\| +(?P<my_number_str>[0-9 ]+)"
    line_sections = re.match(pattern, line).groupdict()
    winning_numbers = {int(number) for number in line_sections["winning_str"].split()}
    my_numbers = {int(number) for number in line_sections["my_number_str"].split()}
    return {
        "card_id": int(line_sections["card_id"]),
        "winning_numbers": winning_numbers,
        "my_numbers": my_numbers,
    }

def get_points(card):
    """
    >>> card_line = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    >>> card = parse_card(card_line)
    >>> get_points(card)
    8
    >>> card_line = "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
    >>> card = parse_card(card_line)
    >>> get_points(card)
    0
    """
    number_of_winning = len(card["winning_numbers"] & card["my_numbers"])
    if number_of_winning > 0:
        return 2 ** (number_of_winning-1)
    return 0


def get_card_copies(card):
    """
    >>> card_line = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
    >>> card = parse_card(card_line)
    >>> get_card_copies(card)
    [2, 3, 4, 5]
    """
    number_of_winning = len(card["winning_numbers"] & card["my_numbers"])
    if number_of_winning > 0:
        first_copy = card["card_id"] + 1
        last_copy = first_copy + number_of_winning
        return list(range(first_copy, last_copy))
    return []


cards = load_input_lines(4, test=TEST, transform=parse_card)


def solve_a():
    return sum(get_points(card) for card in cards)


def solve_b():
    card_counts = {card["card_id"]: 1 for card in cards}
    for card in cards:
        current_card_id = card["card_id"]
        copies = get_card_copies(card)
        for card_id in copies:
            card_counts[card_id] += card_counts[current_card_id]
    return sum(card_counts.values())


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
