
from collections import Counter

with open("./2021/data/day6.txt") as f:
    d = f.readline()
    data = d.strip().split(',')
    data = list(map(int, data))
    counts = Counter(data)


def life_generator(n):
    while True:
        if n == 0:
            yield n
            n = 6
        else:
            yield n
            n -= 1


class Lanternfish:
    def __init__(self, n):
        self.n = n

    def next(self):
        if self.n == 0:
            self.n = 6
        else:
            self.n -= 1

    def __str__(self):
        return f'{self.n}'

    def __repr__(self):
        return f'{self.n}'


class FishSchool:
    def __init__(self, counts):
        self.max_life = 8
        self.n = [0] * (self.max_life + 1)
        for k, v in counts.items():
            self.n[k] = v

    def next(self):
        num_zero = self.n[0]
        for d in range(1, 9):
            self.n[d-1] = self.n[d]

        self.n[6] += num_zero
        self.n[8] = num_zero

    def __repr__(self):
        return repr(self.n)

    def __str__(self):
        return str(self.n)

# Part 1
state = list(map(Lanternfish, data))
num_days = 80
print(f'Current state: {state}')
for _ in range(num_days):
    # print(f'Start {_ + 1:2d} days: {state}')
    num_zero = sum(map(lambda x: x.n == 0, state))
    for fish in state:
        fish.next()

    for j in range(num_zero):
        state.append(Lanternfish(8))
    # print(f'  End {_+1:2d} days: {state}')

print(f'Total number of fish after {num_days} days: {len(state)}')


# Part 2
state = FishSchool(counts)
num_days = 256
for _ in range(num_days):
    state.next()

print(f'Total fish: {sum(state.n)}')
