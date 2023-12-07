import os
from collections import Counter
from helpers import load_input_lines


TEST = os.environ.get("AOC_TEST", False)


def adjust_for_jokers(counts):
    """
    >>> counts = Counter('KTJJT')
    >>> counts = adjust_for_jokers(counts)
    >>> counts['K']
    1
    >>> counts['T']
    4
    """
    counts = counts.copy()
    if counts['J'] != 5:
        number_of_jokers = counts['J']
        del counts['J']
        most_common_card, most_common_count = counts.most_common(1)[0]
        counts[most_common_card] += number_of_jokers
    return counts


def hand_type_strength(hand, joker):
    """
    >>> hand_type_strength("AAAAA", joker=False)
    6
    >>> hand_type_strength("KTJJT", joker=False)
    2
    >>> hand_type_strength("KTJJT", joker=True)
    5
    """
    hand_types = (
        [1, 1],     # high card
        [2, 1],     # one pair
        [2, 2],     # two pair
        [3, 1],     # three of a kind
        [3, 2],     # full house
        [4, 1],     # four of a kind
        [5],        # five of a kind
    )
    counts = Counter(hand)
    if joker and not hand == "JJJJJ":
        counts = adjust_for_jokers(counts)
    highest_two_counts = sorted(counts.values(), reverse=True)[:2]
    return hand_types.index(highest_two_counts)


def hand_card_strength(hand, joker):
    """
    >>> hand_card_strength("KTJJT", joker=False)
    [11, 8, 9, 9, 8]
    >>> hand_card_strength("KTJJT", joker=True)
    [11, 9, 0, 0, 9]
    """
    cards = "J23456789TQKA" if joker else "23456789TJQKA"
    return [cards.index(card) for card in hand]


def hand_strength(hand, joker=False):
    """
    >>> hand_strength("KTJJT")
    (2, 11, 8, 9, 9, 8)
    """
    return (hand_type_strength(hand, joker), *hand_card_strength(hand, joker))


def parse_card(line):
    """
    >>> parse_card("KTJJT 220")
    {'hand': 'KTJJT', 'bid': 220}
    """
    hand, bid_str = line.split()
    bid = int(bid_str)
    return {
        "hand": hand,
        "bid": bid,
    }


def get_total_winnings(joker=False):
    cards = load_input_lines(7, test=TEST, transform=parse_card)
    card_strength = lambda card: hand_strength(card["hand"], joker)
    sorted_cards = sorted(cards, key=card_strength)
    ranked_cards = enumerate(sorted_cards, start=1)
    winnings = [
        rank * card["bid"]
        for rank, card in ranked_cards
    ]
    return sum(winnings)


def solve_a():
    return get_total_winnings()


def solve_b():
    return get_total_winnings(joker=True)


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
