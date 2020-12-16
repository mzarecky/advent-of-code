
import itertools

with open("./2020/9/input.txt") as f:
    data = f.readlines()
    data = [int(d.strip()) for d in data]


def is_sum_of(int_list, target):
    temp = list(
        filter(lambda x: x == target, map(sum, filter(lambda y: y[0] != y[1], itertools.combinations(int_list, 2))))
    )
    return True if len(temp) > 0 else False


def iter_preamble(int_list, preamble_size):
    for j in range(len(int_list) - (preamble_size+1)):
        yield int_list[j:(j+preamble_size)], int_list[j+preamble_size]


test_list = [35,20,15,25,47,40,62,55,65,95,102,117,150,182,127,219,299,277,309,576]

for lst, tar in iter_preamble(data, 25):
    print(f"{lst} -> {tar}")
    if not is_sum_of(lst, tar):
        print(f"-- {tar} is bad")
        break

# Part 2
invalid_num = 25918798

s = 0
cumsum_data = []
for a, b in enumerate(data):
    s += b
    cumsum_data += [(a, s)]

for a, b in itertools.combinations(cumsum_data, 2):
    if b[1] - a[1] == invalid_num:
        print(f"{a} - {b}")
        break

# (407, 44556268) - (424, 70475066)
minval = min(data[407:425])
maxval = max(data[407:425])
print(f"Weakness number: {minval + maxval}")
