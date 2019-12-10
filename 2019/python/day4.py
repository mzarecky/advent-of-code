
import functools


def password_valid_1(password: str):
    n = len(password)
    is_increasing = functools.reduce(lambda x, y: x and y, map(lambda x: password[x] <= password[x+1], range(n-1)))
    has_doubles = functools.reduce(lambda x, y: x or y, map(lambda x: password[x] == password[x+1], range(n-1)))
    return is_increasing and n == 6 and has_doubles


def password_valid_2(password: str):
    n = len(password)
    is_increasing = functools.reduce(lambda x, y: x and y, map(lambda x: password[x] <= password[x+1], range(n-1)))
    next_same = [y for y in map(lambda x: password[x] == password[x + 1], range(n-1))]
    next_same = [False] + next_same + [False]
    has_doubles = functools.reduce(
        lambda x, y: x or y,
        map(lambda x: next_same[(x-1):(x+2)] == [False, True, False],
            range(1, len(next_same))))
    return is_increasing and n == 6 and has_doubles


def solution_1(p_range: str):
    range_limits = [int(x) for x in p_range.split("-")]
    num_good = 0
    for j in range(range_limits[0], range_limits[1]+1):
        if password_valid_1(str(j)):
            num_good += 1
    return num_good


def solution_2(p_range: str):
    range_limits = [int(x) for x in p_range.split("-")]
    num_good = 0
    for j in range(range_limits[0], range_limits[1]+1):
        if password_valid_2(str(j)):
            num_good += 1
    return num_good


print(password_valid_1("111111"))
print(password_valid_1("223450"))
print(password_valid_1("123789"))

print(password_valid_2("112233"))
print(password_valid_2("123444"))
print(password_valid_2("111122"))

with open("../data/data4.txt") as f:
    my_input = f.read().strip()
print(solution_1("234208-765869"))
print(solution_2("234208-765869"))
