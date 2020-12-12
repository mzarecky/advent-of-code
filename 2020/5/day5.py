
import functools

with open("./2020/5/input.txt") as f:
    data = f.readlines()
    data = [d.strip() for d in data]


def convert(s):
    cc = s[0:7]
    dd = s[7:10]
    ll = [64, 32, 16, 8, 4, 2, 1]
    rr = [4, 2, 1]
    row = sum(map(lambda x: x[1] if x[0] == 'B' else 0, zip(cc, ll)))
    col = sum(map(lambda x: x[1] if x[0] == 'R' else 0, zip(dd, rr)))
    return row, col, row*8 + col


a, b, c = convert('BFFFBBFRRR')
print(f"{a}, {b}, {c}")
a, b, c = convert('FFFBBBFRRR')
print(f"{a}, {b}, {c}")
a, b, c = convert('BBFFBBFRLL')
print(f"{a}, {b}, {c}")

# Part 1
print(max(map(lambda x: convert(x)[2], data)))

# Part 2 (row, col, seat_id)
all_seats = list(map(lambda x: convert(x), data))
aa = sorted(all_seats, key=lambda x: x[2])

potential_seats = set(range(15, 948))
used_seats = set([d[2] for d in all_seats])


found_seat = potential_seats - used_seats
print(f"Missing seat: {found_seat}")
