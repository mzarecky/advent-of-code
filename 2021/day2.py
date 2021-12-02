import itertools

with open("./2021/data/day2.txt") as f:
    data = f.readlines()
    data = [d.strip().split(" ") for d in data]
    data = [(d[0], int(d[1])) for d in data]


class Submarine:
    def __init__(self):
        self.depth = 0
        self.h_pos = 0
        self.mapper = {'forward': self.forward, 'up': self.up, 'down': self.down}

    def forward(self, units):
        self.h_pos += units

    def up(self, units):
        self.depth -= units

    def down(self, units):
        self.depth += units

    def movement(self, iter):
        for direction, units in iter:
            self.mapper[direction](units)


class Submarine2:
    def __init__(self):
        self.depth = 0
        self.h_pos = 0
        self.aim = 0
        self.mapper = {'forward': self.forward, 'up': self.up, 'down': self.down}

    def forward(self, units):
        self.h_pos += units
        self.depth += self.aim * units

    def up(self, units):
        # self.depth -= units
        self.aim -= units

    def down(self, units):
        # self.depth += units
        self.aim += units

    def movement(self, iter):
        for direction, units in iter:
            self.mapper[direction](units)


# Part 1
aa = Submarine()
aa.movement(data)
print(f"Depth={aa.depth}, HorizontalPos={aa.h_pos}, Result={aa.depth*aa.h_pos}")


# Part 2
aa = Submarine2()
aa.movement(data)
print(f"Depth={aa.depth}, HorizontalPos={aa.h_pos}, Result={aa.depth*aa.h_pos}")
