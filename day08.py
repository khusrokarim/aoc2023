import os
from math import lcm
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)


class Node:

    all_nodes = {}
    selected_nodes = []

    def __init__(self, name, left_name=None, right_name=None):
        self.name = name
        self.left_name = left_name
        self.right_name = right_name
        self.L = None
        self.R = None
        Node.all_nodes[name] = self

    @classmethod
    def create_edges(cls):
        for node in cls.all_nodes.values():
            node.L = cls.all_nodes[node.left_name]
            node.R = cls.all_nodes[node.right_name]

    @classmethod
    def from_line(cls, line):
        name, rest = line.split(" = ")
        left_name, right_name = rest[1:-1].split(", ")
        return cls(name, left_name, right_name)

    def __repr__(self):
        return self.name


def follow_directions(node, directions, end_func):
    steps = 0
    valid_end_nodes = {node for node in Node.all_nodes.values() if end_func(node)}
    current_node = node
    while not current_node in valid_end_nodes:
        direction = next(directions)
        current_node = getattr(current_node, direction)
        steps += 1
    return steps


def repeat_iterable(iterable):
    """
    >>> s = repeat_iterable("ab")
    >>> [next(s), next(s), next(s)]
    ['a', 'b', 'a']
    """
    iterable = list(iterable)
    while True:
        try:
            yield from iterable
        except StopIteration:
            iterable = list(iterable)
            yield from iterable


def transform(line):
    """
    >>> transform("")
    >>> s = transform("abc")
    >>> [next(s), next(s), next(s), next(s)]
    ['a', 'b', 'c', 'a']
    >>> node = transform("AAA = (BBB, CCC)")
    >>> node.left_name
    'BBB'
    """
    if line:
        if "=" in line:
            return Node.from_line(line)
        elif line:
            return repeat_iterable(line)


def build_map(test=TEST, test_suffix=""):
    """
    >>> directions, nodes = build_map(test=True, test_suffix="a")
    >>> next(directions)
    'L'
    >>> Node.all_nodes["BBB"].L.name
    'AAA'
    """
    directions, empty, *nodes = load_input_lines(8, test, transform=transform, test_suffix=test_suffix)
    Node.create_edges()
    return (directions, nodes)


def solve_a():
    def part_a_end_func(node):
        return node.name == "ZZZ"

    directions, nodes = build_map(test=TEST, test_suffix="a")
    node = Node.all_nodes["AAA"]
    return follow_directions(node, directions, part_a_end_func)


def solve_b():
    def part_b_end_func(node):
        return node.name[2] == "Z"

    directions, nodes = build_map(test=TEST, test_suffix="b")
    nodes = [node for node in nodes if node.name[2] == "A"]
    steps_by_node = []
    for node in nodes:
        steps = follow_directions(node, directions, part_b_end_func)
        steps_by_node.append(steps)
    return lcm(*steps_by_node)


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
