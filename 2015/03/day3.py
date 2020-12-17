
import collections

with open("./2015/3/input.txt") as f:
    a = f.readlines()[0].strip()


def navigate(x):
    d = collections.defaultdict(int)
    nav_map = {
        "<": (-1, 0),
        ">": (1, 0),
        "^": (0, 1),
        "v": (0, -1)
    }
    pos = (0, 0)
    d[pos] = 1

    for p in x:
        pos = (pos[0] + nav_map[p][0], pos[1] + nav_map[p][1])
        d[pos] += 1

    return d


houses = navigate(a)
temp = len(houses.keys())
print(f"Part 1: {temp}")

santa_houses = set(list(navigate(a[0::2]).keys()))
robo_houses = set(list(navigate(a[1::2]).keys()))
all_houses = santa_houses.union(robo_houses)
temp = len(all_houses)
print(f"Part 2: {temp}")
