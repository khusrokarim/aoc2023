from pathlib import Path


def file_path(day_number, test=False):
    path = Path('.') / 'input'
    if test:
        path = path / 'test'
    return path / f'{day_number}'


def load_input_lines(day_number, test=False, transform=None, strip=True, return_values=True):
    path = file_path(day_number, test)
    with open(path) as input_file:
        if strip:
            return_val = [l.strip() for l in input_file.readlines()]
        else:
            return_val = input_file.readlines()
    if transform:
        return_val = [transform(l) for l in return_val]
    if return_values:
        return return_val
