from baby import Baby
from cell import Cell
import re
import sys

dim_regex = re.compile('(x *=)')
y_regex = re.compile('(y *=)')


def set_pattern_dimension(line, baby):
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


def find_and_set_row_multipliers(data):
    regex = re.compile("\d+\$", re.IGNORECASE)
    result = data
    for match in regex.finditer(data):
        start = -1
        row_multiplier = 0
        replaced = ''
        start = match.start()
        stop = match.end()
        match_row_multiplier_pattern = match.group()
        multiplier_count = re.search(r"\d+", match_row_multiplier_pattern)
        if multiplier_count:
            row_multiplier = int(multiplier_count.group())
            for indx in range(row_multiplier):
                replaced += '$'
        data = result.replace(result[start: stop], replaced )
    return data


def rle_decode(data, baby):
    cells = set()
    data.lower()
    data_rows = find_and_set_row_multipliers(data)

    row_list = data_rows.rsplit('$')
    for row_index, row in enumerate(row_list, start=0):
        repeater_pos = 0
        repeater = '0'
        count = 0
        last_digit_value = ''
        for index, letter in enumerate(row, start=0):
            if letter.isdigit():
                repeater += letter
                if last_digit_value != '':
                    count -= int(last_digit_value) - 1
                count += int(repeater) - 1
                repeater_pos = count - int(repeater) + 1 if count - int(repeater) >= 0 else 0
                last_digit_value += letter
            elif letter == 'b':
                repeater = '0'
                count += 1
                repeater_pos = 0
                last_digit_value = ''
            elif letter == 'o':
                if int(repeater) == 0:
                    cell = Cell.Cell(count, row_index)
                    cells.add(cell)
                else:
                    for place in range(int(repeater)):
                        cell = Cell.Cell(place + repeater_pos, row_index)
                        cells.add(cell)
                repeater = '0'
                count += 1
                repeater_pos = 0
                last_digit_value = ''
    baby.cells = cells
    return baby


def set_newborn_cells(line, baby):
    return rle_decode(line, baby)


def load_pattern(file):
    baby = Baby.Baby()
    pattern_line = ''
    dimension_index = sys.maxsize;
    for i, line in enumerate(file):
        if re.match(dim_regex, line):
            set_pattern_dimension(line, baby)
            dimension_index = i
        if i >= dimension_index + 1:
            pattern_line += str(line.rstrip())
    return set_newborn_cells(pattern_line, baby)
