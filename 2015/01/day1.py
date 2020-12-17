
with open("./2015/1/input.txt") as f:
    a = f.readlines()[0].strip()


def floor_sum(x):
    char_map = {"(": 1, ")": -1}
    return sum(char_map[x] for x in x)


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
