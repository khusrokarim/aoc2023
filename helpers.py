from pathlib import Path


class Matrix:

    def __init__(self, lines, starting_location=(0, 0)):
        self.rows = list(lines)
        self.width = len(lines[0])
        self.height = len(lines)
        self.columns = [
            [line[i] for line in lines]
            for i in range(self.width)
        ]
        self.x, self.y = starting_location


def file_path(day_number, test=False, test_suffix=""):
    suffix = test_suffix if test else ""
    path = Path('.') / 'input'
    if test:
        path = path / 'test'
    return path / f'{day_number}{suffix}'


def load_input_lines(day_number, test=False, transform=None, strip=True, return_values=True, test_suffix=""):
    path = file_path(day_number, test, test_suffix)
    with open(path) as input_file:
        if strip:
            return_val = [l.strip() for l in input_file.readlines()]
        else:
            return_val = input_file.readlines()
    if transform:
        return_val = [transform(l) for l in return_val]
    if return_values:
        return return_val


def load_input_matrix(*args, **kwargs):
    lines = load_input_lines(*args, **kwargs)
    return Matrix(lines)
