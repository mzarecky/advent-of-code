
import re
import collections
import functools


with open('./2020/22/input.txt') as f:
    data = [parse_input(d.strip()) for d in f.readlines()]

