
import functools
import re

with open("./2015/5/input.txt") as f:
    a = f.readlines()
    a = [x.strip() for x in a]


def has_vowels(x):
    return len(list(filter(lambda y: y in ['a', 'e', 'i', 'o', 'u'], x))) >= 3


def has_repeats(x):
    for a, b in zip(x[0:-1], x[1:]):
        if a == b:
            return True
    return False


def has_no_bad(x):
    return not functools.reduce(lambda a, b: a or b, map(lambda y: y in x, ['ab', 'cd', 'pq', 'xy']))


def is_nice(x):
    return has_vowels(x) and has_repeats(x) and has_no_bad(x)


def is_nice2(x):
    a = re.search(r"(.).\1", x) is not None
    b = re.search(r"(..).*\1", x) is not None
    return a and b


temp = sum(map(is_nice, a))
print(f"Part 1: {temp}")

temp = sum(map(is_nice2, a))
print(f"Part 2: {temp}")
