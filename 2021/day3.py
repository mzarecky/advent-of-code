import collections

with open("./2021/data/day3.txt") as f:
    data = [d.strip() for d in f.readlines()]


def get_bit(iter, i, mode='oxygen'):
    bit_counter = collections.Counter()
    bit_counter.update(map(lambda x: x[i], iter))
    if mode == 'oxygen':
        # most common first
        return (1, 0) if bit_counter['1'] >= bit_counter['0'] else (0, 1)
    else:
        # least common first
        return (0, 1) if bit_counter['1'] >= bit_counter['0'] else (1, 0)


def get_rates(iter):
    mult = list(map(lambda x: 2 ** x, range(len(iter)-1, -1, -1)))
    gamma = sum(map(lambda x: x[0] * x[1][0], zip(mult, iter)))
    epsilon = sum(map(lambda x: x[0] * x[1][1], zip(mult, iter)))
    return gamma, epsilon


def to_bin(iter):
    mult = list(map(lambda x: 2 ** x, range(len(iter)-1, -1, -1)))
    aa = sum(map(lambda x: x[0] * int(x[1]), zip(mult, iter)))
    return aa


# Part 1
bit_counts = list(map(lambda x: get_bit(data, x), range(len(data[0]))))
gamma, epsilon = get_rates(bit_counts)
print(f'Gamma = {gamma}, Epsilon = {epsilon}, Power Consumption = {gamma * epsilon}')


# Part 2
o_data = data.copy()
c_data = data.copy()
for j in range(len(data[0])):
    print(c_data)
    oxygen_bit = get_bit(o_data, j, mode='oxygen')
    co_bit = get_bit(c_data, j, mode='co2')
    print(co_bit)
    if len(o_data) > 1:
        o_data = list(filter(lambda x: x[j] == str(oxygen_bit[0]), o_data))
    if len(c_data) > 1:
        c_data = list(filter(lambda x: x[j] == str(co_bit[0]), c_data))

oxygen_rating = to_bin(o_data[0])
co_rating = to_bin(c_data[0])
print(f"Oxy={oxygen_rating}, Co={co_rating}, Life Support = {oxygen_rating * co_rating}")

