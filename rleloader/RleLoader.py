from newborn import Newborn
from cell import Cell
import re


dim_regex = re.compile('(x *=)')
y_regex = re.compile('(y *=)')


new_born = Newborn


def set_pattern_dimension(line):
    match = re.search(r"(x *= )\d", line)
    if match:
        match_x = re.search(r"\d", match.group())
        if match_x:
            x = int(match_x.group())
    match2 = re.search(r"(y *= )\d", line)
    if match2:
        match_y = re.search(r"\d", match2.group())
        if match_y:
            y = int(match_y.group())
    new_born.dimension = (x, y)


def rle_decode(data):
    data.lower()
    count = 1
    x = 0
    for i in range(len(data)):
        if data[i] == '$':
            x += 1
        if data[i].isdigit() and data[i + 1] == 'o':
            count += int(data[i])
        if data[i] == 'o':
            cell = Cell
            cell.position = (x, i + count - 1)
            new_born.cells.add(cell)
            count = 1
    for cell in new_born.cells:
        print(cell.position)


def set_newborn_cells(line):
    rle_decode(line)


def load_pattern(file):
    dimension_index = -2;
    for i, line in enumerate(file):
        if re.match(dim_regex, line):
            set_pattern_dimension(line)
            dimension_index = i
        if i == dimension_index + 1:
            set_newborn_cells(str(line))
