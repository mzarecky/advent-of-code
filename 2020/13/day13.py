
import math
import functools


def parse_data(input_str):
    temp = list(filter(lambda x: x[1] != 'x', enumerate(input_str.split(","))))
    return [(x[0], int(x[1]), (-1 * x[0]) % int(x[1])) for x in temp]


departure_time = 1014511

data =    [17, 41, 643, 23, 13, 29, 433, 37, 19]
offsets = [0,   7,  17, 25, 30, 46,  48, 54, 67]
offsets2 = [((-1*o) % d) % d for d, o in zip(data, offsets)]


def find_closest_departure(want_time, bus_id):
    n = math.ceil(want_time / bus_id) * bus_id
    wait_time = n - want_time
    return n, wait_time, wait_time * bus_id

arrival_time, wait_time, c = find_closest_departure(939, 59)
print(f"{arrival_time}, {wait_time}, {c}")

# Part 1
temp = sorted(map(lambda x: find_closest_departure(departure_time, x), data), key=lambda x: x[0])
print(temp[0])


# Part 2
def get_inverse(a, p):
    if a == 0:
        return 0
    for j in range(p):
        if (a * j) % p == 1:
            return j
    return None


"""
Chinese Remainder Theorem chunk

Note: Must use // here instead of /, even though M is divisible by p.
Example:
  M = 1182922135469659  
  a = 34, p = 41, m = 28851759401699, inv = 27, returns 461628150427184

34 * 28851759401699   * 27 % 1182922135469659 = 461628150427184
34 * 28851759401699.0 * 27 % 1182922135469659 = 461628150427182.0
"""
def crm_chunk(a, p, M):
    new_m = M // p
    inv = get_inverse(new_m, p)
    temp = (a * new_m) % M
    temp = (temp * inv) % M
    print(f"   a = {a}, p = {p}, m = {new_m}, inv = {inv}, returns {temp}")
    return temp


# data =    [17, 41, 643, 23, 13, 29, 433, 37, 19]
# offsets = [0,   7,  17, 25, 30, 46,  48, 54, 67]
# offsets2 = [((-1*o) % d) % d for d, o in zip(data, offsets)]

# data = [67, 7, 59, 61]
# offsets2 = [0, 6, 56, 57]

# data = [1789, 37, 47, 1889]
# offsets2 = [0, 36, 45, 1886]

data2 = parse_data("17,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,643,x,x,x,x,x,x,x,23,x,x,x,x,13,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,29,x,433,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,x,x,19")
data = [d[1] for d in data2]
offsets2 = [d[2] for d in data2]

M = functools.reduce(lambda x, y: x*y, data)
s = 0

for p, a in zip(data, offsets2):
    temp = crm_chunk(a, p, M)
    s = (s + temp) % M

print(s % M)
