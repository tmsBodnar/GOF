from baby import Baby
from cell import Cell
import re
import sys

dim_regex = re.compile('(x *=)')
y_regex = re.compile('(y *=)')
dimension = (10, 10)
cells = set()
baby = Baby.Baby(dimension, cells)


def set_pattern_dimension(line):
    match = re.search(r"(x *= )\d*", line)
    if match:
        match_x = re.search(r"\d+", match.group())
        if match_x:
            x = int(match_x.group())
    match2 = re.search(r"(y *= )\d*", line)
    if match2:
        match_y = re.search(r"\d+", match2.group())
        if match_y:
            y = int(match_y.group())
            baby.dimension = (x, y)


def rle_decode(data):
    data.lower()
    count = 0
    x = 0
    for i in range(len(data)):
        repeater = 1
        if data[i] == '$':
            count = 0;
            x += 1
        if data[i] == 'b':
            if data[i - 1].isdigit():
                count += int(data[i - 1]);
            else:
                count += 1;
        if data[i] == 'o':

            if data[i - 1].isdigit():
                repeater = int(data[i - 1])
                for j in range(repeater):
                    cell = Cell.Cell()
                    cell.position = {'x': x,
                                 'y': j + count}
                    baby.cells.add(cell)
            else:
                y = count
                cell = Cell.Cell()
                cell.position = {'x': x,
                                 'y': y}
                baby.cells.add(cell)
            count += 1
#    for cell in baby.cells:
#        for position in sorted(cell.position.items()):
#           print(str(position[0]) + ' : ' + str(position[1]))


def set_newborn_cells(line):
    rle_decode(line)


def load_pattern(file):
    pattern_line = ''
    dimension_index = sys.maxsize;
    for i, line in enumerate(file):
        if re.match(dim_regex, line):
            set_pattern_dimension(line)
            dimension_index = i
        if i >= dimension_index + 1:
            pattern_line += str(line.rstrip())
    set_newborn_cells(pattern_line)
    return baby
