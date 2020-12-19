
import itertools


class ConwayLights:
    def __init__(self, initial_state, force_corners_on=False):
        self.x_dim = len(initial_state[0])
        self.y_dim = len(initial_state)
        self.force_corners_on = force_corners_on
        self.state = {(x, y): False for x in range(self.x_dim) for y in range(self.y_dim)}
        self.corners = [(0, 0), (0, self.y_dim-1), (self.x_dim-1, 0), (self.x_dim-1, self.y_dim-1)]
        self.next_state = {}
        self.adj = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.step = 0
        self.set_initial_state(initial_state)

    def __str__(self):
        return ""

    def is_valid_pos(self, pos):
        return 0 <= pos[0] < self.x_dim and 0 <= pos[1] < self.y_dim

    def set_initial_state(self, initial_state):
        for y, s in enumerate(initial_state):
            for x, c in enumerate(s):
                if c == "#":
                    self.state[(x, y)] = True
        if self.force_corners_on:
            for pos in self.corners:
                self.state[pos] = True

    def get_num_adjacent(self, pos):
        w = filter(lambda y: self.is_valid_pos(y), map(lambda x: (x[0]+pos[0], x[1]+pos[1]), self.adj))
        return sum(map(lambda x: self.state[x], w))

    def get_total_on(self):
        return sum(self.state.values())

    def next(self):
        self.step += 1
        for pos in self.state:
            n = self.get_num_adjacent(pos)
            if (self.state[pos] and 2 <= n <= 3) or (not self.state[pos] and n == 3):
                self.next_state[pos] = True
            else:
                self.next_state[pos] = False
        self.state = self.next_state.copy()
        if self.force_corners_on:
            for pos in self.corners:
                self.state[pos] = True


# Parse Input
with open("./2015/18/input.txt") as f:
    data = [d.strip() for d in f.readlines()]

test_data = [".#.#.#", "...##.", "#....#", "..#...", "#.#..#", "####.."]

# Part 1
cl = ConwayLights(data)
while cl.step < 100:
    cl.next()
print(f"Total lights on: {cl.get_total_on()}")

# Part 2
cl = ConwayLights(data, force_corners_on=True)
while cl.step < 100:
    cl.next()
print(f"Total lights on: {cl.get_total_on()}")
