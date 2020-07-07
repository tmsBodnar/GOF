from cell import Cell
import re

cell= Cell
dim_regex = re.compile("(x *=)")
y_regex = re.compile("(y *=)")


def set_pattern_dimension(line):
    match = re.search(r"(x *= )\d", line)
    if match:
        matchx = re.search(r"\d", match.group())
        if matchx:
            cell.x = int(matchx.group())
    match2 = re.search(r"(y *= )\d", line)
    if match2:
        matchy = re.search(r"\d", match2.group())
        if matchy:
            cell.y = int(matchy.group())
    print(cell)


def load_pattern(file):
    for i, line in enumerate(file):
        if re.match(dim_regex, line):
            set_pattern_dimension(line)
