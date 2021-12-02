import itertools

with open("./2021/data/day1.txt") as f:
    data = f.readlines()
    data = [int(d.strip()) for d in data]


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def tripwise(iterable):
    a, b, c = itertools.tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


# Part 1
num_increases = sum(map(lambda x: 1 if x[0] < x[1] else 0, pairwise(data)))
print(f"number of increases: {num_increases}")


# Part 2
dubs = list(pairwise(tripwise(data)))
num_increases = sum(map(lambda x: 1 if sum(x[0]) < sum(x[1]) else 0, dubs))
print(f"number of increases: {num_increases}")
