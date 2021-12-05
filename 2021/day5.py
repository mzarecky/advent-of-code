
import collections
import re


def cmp(a, b):
    return (a < b) - (a > b)


def parse_input(s):
    temp = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', s)
    x1, y1, x2, y2 = temp.groups()
    if x1 == x2:
        line_type = 'v'
    elif y1 == y2:
        line_type = 'h'
    else:
        line_type = 'd'
    return int(x1), int(y1), int(x2), int(y2), line_type


def line_generator(x1, y1, x2, y2):
    x_dir = cmp(x1, x2)
    y_dir = cmp(y1, y2)
    cur_x = x1
    cur_y = y1
    yield cur_x, cur_y
    while cur_x != x2 or cur_y != y2:
        cur_x += x_dir
        cur_y += y_dir
        yield cur_x, cur_y


def count_dangerous(counter):
    return sum(map(lambda x: x > 1, counter.values()))


with open("./2021/data/day5.txt") as f:
    data = [parse_input(d.strip()) for d in f.readlines()]

# Part 1
vent_grid = collections.Counter()
for x1, y1, x2, y2, line_type in data:
    if line_type == 'd':
        continue
    for p in line_generator(x1, y1, x2, y2):
        vent_grid.update([p])

print(f"Num dangerous (part 1): {count_dangerous(vent_grid)}")


# Part 2
vent_grid = collections.Counter()
for x1, y1, x2, y2, line_type in data:
    for p in line_generator(x1, y1, x2, y2):
        vent_grid.update([p])

print(f"Num dangerous (part 2): {count_dangerous(vent_grid)}")

