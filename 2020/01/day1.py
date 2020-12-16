
import itertools

with open("./2020/1/input.txt") as f:
    data = f.readlines()
    data = [int(d.strip()) for d in data]


def part1(data, target):
    for j in itertools.combinations(data, 2):
        if sum(j) == target:
            return j


def part2(data, target, n=3):
    for j in itertools.combinations(data, n):
        if sum(j) == target:
            return j


a, b = part1(data, 2020)
print(f"Part 1 is {a*b}")

a, b, c = part2(data, 2020, 3)
print(f"Part 2 is {a*b*c}")


def find_floor(x, f):
    char_map = {"(": 1, ")": -1}
    s = 0
    p = 0
    for c in x:
        s += char_map[c]
        p += 1
        if s == f:
            break
    return p


print(f"Part 1: {floor_sum(a)}")
print(f"Part 2: {find_floor(a, -1)}")
