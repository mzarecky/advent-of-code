
with open("./2021/data/day7.txt") as f:
    d = f.readline()
    data = d.strip().split(',')
    data = list(map(int, data))


def calculate_fuel(iter, step):
    return sum(map(lambda x: abs(x-step), iter))


def calculate_fuel_square(iter, step):
    def cost(s):
        return s * (s+1) / 2
    return sum(map(lambda x: cost(abs(x-step)), iter))


# Part 1
lower_bound, upper_bound = min(data), max(data)
results = {b: calculate_fuel(data, b) for b in range(lower_bound, upper_bound+1)}
print(f'Lowest fuel requirement: {min(results.values())}')


# Part 2
lower_bound, upper_bound = min(data), max(data)
results = {b: calculate_fuel_square(data, b) for b in range(lower_bound, upper_bound+1)}
print(f'Lowest fuel requirement: {min(results.values())}')
