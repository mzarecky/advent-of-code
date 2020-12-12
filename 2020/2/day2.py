
import re


# 3-7 x: xjxbgpxxgtx
def parse_data(x):
    temp = re.split("[- :]", x)
    return int(temp[0]), int(temp[1]), temp[2], temp[-1]


def is_valid(len1, len2, char, password):
    num_char = sum(map(lambda x: x == char, password))
    return len1 <= num_char <= len2


def is_valid2(len1, len2, char, password):
    p1 = password[len1 - 1] == char
    p2 = password[len2 - 1] == char
    return p1 ^ p2


with open("./2020/2/input.txt") as f:
    data = f.readlines()
    data = [parse_data(d.strip()) for d in data]


# part 1
s = 0
for p1, p2, c, pwd in data:
    temp = is_valid(p1, p2, c, pwd)
    if temp:
        s += 1

# part 2
s = 0
for p1, p2, c, pwd in data:
    temp = is_valid2(p1, p2, c, pwd)
    if temp:
        s += 1
print(f"Part 2: {s}")
