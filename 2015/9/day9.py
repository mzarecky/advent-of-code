
import itertools


def parse_data(x):
    x = x.strip()
    a = x.split(" = ")
    b = a[0].split(" to ")
    return b[0], b[1], int(a[1])


with open("./2015/9/input.txt") as f:
    data = f.readlines()
    data = [parse_data(x) for x in data]


def find_all_distances(input_data):
    distances = dict()
    places = set()
    for p1, p2, d in input_data:
        # print(f"{p1} -> {p2} = {d}")
        places.add(p1)
        places.add(p2)
        distances[(p1, p2)] = d
        distances[(p2, p1)] = d

    all_distances = dict()
    n = len(places)
    for p in itertools.permutations(places, n):
        # print(p)
        s = 0
        for j in zip(p[0:n-1], p[1:n]):
            # print(f"-- {j} -> {distances[j]}")
            s += distances[j]
        all_distances[p] = s

    return all_distances


aa = find_all_distances(data)
for j in aa:
    print(f"{j} -> {aa[j]}")

ss = sorted(aa, key=lambda x: aa[x])
shortest = ss[0]
longest = ss[-1]
print(f"Shortest distance: {shortest} -> {aa[shortest]}")
print(f"Shortest distance: {longest} -> {aa[longest]}")
