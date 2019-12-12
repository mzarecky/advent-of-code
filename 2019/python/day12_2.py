import itertools
import math


class Cycle:
    def __init__(self, pos):
        self.n = len(pos)
        self.pos = pos[:]
        self.velocity = [0] * len(pos)
        self.i = 0
        self.cycle_length = 0
        self.cycle_start = 0
        self.cycles = {}

    def __str__(self):
        return f"iter={self.i}; " + \
               f"pos=<{', '.join([str(x) for x in self.pos])}>; " + \
               f"velocity=<{', '.join([str(x) for x in self.velocity])}>"

    def cmp(self, a, b):
        if self.pos[a] < self.pos[b]:
            return 1
        elif self.pos[a] > self.pos[b]:
            return -1
        else:
            return 0

    def update_position(self):
        self.pos = [sum(x) for x in zip(self.pos, self.velocity)]

    def update_gravity(self):
        for pos in itertools.combinations(range(self.n), 2):
            pos1, pos2 = pos
            update = self.cmp(pos1, pos2)
            self.velocity[pos1] += update
            self.velocity[pos2] -= update

    def create_cycles(self, verbose=False):
        state = tuple(self.pos + self.velocity)
        self.i = 0
        while state not in self.cycles:
            if verbose:
                print(self.__str__())
            self.cycles[state] = self.i
            self.update_gravity()
            self.update_position()
            state = tuple(self.pos + self.velocity)
            self.i += 1
        self.cycle_length = self.i - self.cycles[state]
        self.cycle_start = self.cycles[state]

    def print_stats(self):
        print(f"start = {self.cycle_start}; length = {self.cycle_length}; end = {self.i}")


def lcm(a, b):
    return a * b // math.gcd(a, b)


# Test 1 ----
aa = Cycle([-1, 2, 4, 3])
bb = Cycle([0, -10, -8, 5])
cc = Cycle([2, -7, 8, -1])

print(aa)
print(bb)
print(cc)

aa.create_cycles()
bb.create_cycles()
cc.create_cycles()

# 2772 = 9 * 4 * 7 * 11
aa.print_stats()  # 18 = 2 * 9
bb.print_stats()  # 28 = 4 * 7
cc.print_stats()  # 44 = 4 * 11

print(lcm(aa.cycle_length, lcm(bb.cycle_length, cc.cycle_length)))

# Test 2 ----
aa = Cycle([-8, 5, 2, 9])
bb = Cycle([-10, 5, -7, -8])
cc = Cycle([0, 10, 3, -3])

print(aa)
print(bb)
print(cc)

aa.create_cycles()
bb.create_cycles()
cc.create_cycles()

# 4686774924 = 3 * 4 * 13^2 * 983 * 2351
aa.print_stats()  # 2028 = 4 * 3 * 13^2
bb.print_stats()  # 5898 = 2 * 3 * 983
cc.print_stats()  # 4702 = 2 * 2351

print(lcm(aa.cycle_length, lcm(bb.cycle_length, cc.cycle_length)))

# Part 2 ----

# <x=0, y=4, z=0>
# <x=-10, y=-6, z=-14>
# <x=9, y=-16, z=-3>
# <x=6, y=-1, z=2>

aa = Cycle([0, -10, 9, 6])
bb = Cycle([4, -6, -16, -1])
cc = Cycle([0, -14, -3, 2])
aa.create_cycles()
bb.create_cycles()
cc.create_cycles()
aa.print_stats()
bb.print_stats()
cc.print_stats()

print(lcm(aa.cycle_length, lcm(bb.cycle_length, cc.cycle_length)))
