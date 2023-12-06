import os
from collections import deque, UserDict
from helpers import load_input_lines

TEST = os.environ.get("AOC_TEST", False)


class RangeMap(UserDict):
    """
    >>> range_map = RangeMap({98: (50, 2), 50: (52, 48)})
    >>> range_map[2]
    2
    >>> range_map[99]
    51
    """
    def __getitem__(self, key):
        for min_source_number, (destination_number, map_range) in self.data.items():
            max_source_number = min_source_number + map_range
            if min_source_number <= key < max_source_number:
                offset = destination_number - min_source_number
                return key + offset
        return key


class Almanac:
    seeds = []
    maps = {}
    current_source_name = None

    @classmethod
    def seeds_in_ranges(cls):
        """
        >>> Almanac.parse_input_line("seeds: 79 5 90 3")
        >>> list(Almanac.seeds_in_ranges())
        [79, 80, 81, 82, 83, 90, 91, 92]
        """
        remaining = cls.seeds.copy()
        while remaining:
            seed_number, range_length, *remaining = remaining
            yield from range(seed_number, seed_number + range_length)


    @classmethod
    def parse_input_line(cls, line):
        """
        >>> Almanac.parse_input_line("seeds: 79 14 55 13")
        >>> Almanac.seeds
        [79, 14, 55, 13]
        >>> Almanac.parse_input_line("seed-to-soil map:")
        >>> Almanac.maps['seed']['destination']
        'soil'
        >>> Almanac.parse_input_line("50 98 2")
        >>> Almanac.maps['seed']['entries']
        {98: (50, 2)}
        """
        match line.split():
            case ["seeds:", *seed_numbers]:
                cls.seeds = [int(seed) for seed in seed_numbers]
            case [map_name, "map:"]:
                cls.current_source_name, destination_name = map_name.split("-to-")
                cls.maps[cls.current_source_name] = {
                    "destination": destination_name,
                    "entries": RangeMap(),
                }
            case [destination_str, source_str, map_range_str]:
                source = int(source_str)
                destination = int(destination_str)
                map_range = int(map_range_str)
                cls.maps[cls.current_source_name]["entries"][source] = (destination, map_range)
            case "":
                pass

    @classmethod
    def source_to_destination(cls, source_name, destination_name, source_number):
        """
        >>> load_input_lines(5, test=True, transform=Almanac.parse_input_line, return_values=False)
        >>> Almanac.source_to_destination("seed", "location", 79)
        82
        """
        current_source = source_name
        current_source_number = source_number
        while True:
            source_map = cls.maps[current_source]
            current_destination_name = source_map["destination"]
            current_destination_number = source_map["entries"][current_source_number]
            if current_destination_name == destination_name:
                return current_destination_number
            current_source = current_destination_name
            current_source_number = current_destination_number


load_input_lines(5, test=TEST, transform=Almanac.parse_input_line, return_values=False)


def solve_a():
    return min(
        Almanac.source_to_destination("seed", "location", seed)
        for seed in Almanac.seeds
    )


def solve_b():
    print("creating list")
    seeds = list(Almanac.seeds_in_ranges())
    print("list is length:", len(seeds))
    return min(
        Almanac.source_to_destination("seed", "location", seed)
        for seed in seeds
    )


if __name__ == "__main__":
    print(solve_a())
    print(solve_b())
