
import itertools


class Moon:
    def __init__(self, pos, velocity=[0, 0, 0]):
        self.pos = pos[:]
        self.velocity = velocity[:]

    def __str__(self):
        return f"pos=<{self.pos[0]}, {self.pos[1]}, {self.pos[2]}>;" + \
               f"vel=<{self.velocity[0]}, {self.velocity[1]}, {self.velocity[2]}>"

    def update_gravity(self, other):
        update = [self.cmp(j[0], j[1]) for j in zip(self.pos, other.pos)]
        self.velocity = [sum(x) for x in zip(self.velocity, update)]
        other.velocity = [sum(x) for x in zip(other.velocity, [-1*y for y in update])]

    def update_position(self):
        self.pos = [sum(x) for x in zip(self.pos, self.velocity)]

    @staticmethod
    def calculate_energy(energy):
        return sum([abs(x) for x in energy])

    @staticmethod
    def cmp(a, b):
        if a < b:
            return 1
        elif a > b:
            return -1
        else:
            return 0

    def calculate_total_energy(self):
        return self.calculate_energy(self.velocity) * self.calculate_energy(self.pos)


def parse_input(data):
    return [[int(y[2:]) for y in x[1:-1].split(", ")] for x in data]


def solution_1(moon_positions, max_iterations, verbose=False):
    my_moons = [Moon(x) for x in moon_positions]
    num_iterations = 0
    n = len(my_moons)

    if verbose:
        print("Iteration =", num_iterations)
        for j in range(n):
            print(my_moons[j])
        print("-------------------------------------------")

    while num_iterations < max_iterations:
        # Update gravity on each combination
        for j in itertools.combinations(range(n), 2):
            my_moons[j[0]].update_gravity(my_moons[j[1]])

        # Update position
        for j in range(n):
            my_moons[j].update_position()

        num_iterations += 1
        if verbose:
            print("Iteration =", num_iterations)
            for j in range(n):
                print(my_moons[j])
            print("-------------------------------------------")

    # Get energy of each
    return sum([x.calculate_total_energy() for x in my_moons])


# Tests ----
aa = parse_input([
    "<x=-1, y=0, z=2>",
    "<x=2, y=-10, z=-7>",
    "<x=4, y=-8, z=8>",
    "<x=3, y=5, z=-1>"])
print(aa)
print(solution_1(aa, 10))  # 179

aa = parse_input([
    "<x=-8, y=-10, z=0>",
    "<x=5, y=5, z=10>",
    "<x=2, y=-7, z=3>",
    "<x=9, y=-8, z=-3>"])
print(aa)
print(solution_1(aa, 100))  # 1940


# Part 1 ----
with open("../data/data12.txt") as f:
    data = f.readlines()
    data = [x.strip() for x in data]

aa = parse_input(data)
print(aa)
print(solution_1(aa, 1000))

