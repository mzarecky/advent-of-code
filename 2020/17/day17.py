
import collections
import itertools

with open("./2020/17/input.txt") as f:
    data = [d.strip() for d in f.readlines()]

test_data = ['.#.', '..#', '###']


class ConwayCubes:
    def __init__(self, initial_state):
        self.state_map = {".": False, "#": True}
        self.num_cycles = 0
        self.neighbors = list(itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]))
        self.neighbors.remove((0, 0, 0))
        self.coords = collections.defaultdict(bool)
        self._next = self.coords.copy()
        for row, s in enumerate(initial_state):
            for col, c in enumerate(s):
                self.coords[(row, col, 0)] = self.state_map[c]

    def _add(self, pos, adj):
        return (pos[0] + adj[0], pos[1] + adj[1], pos[2] + adj[2],)

    def num_active_neighbors(self, pos):
        return sum(map(lambda x: self.coords[self._add(pos, x)], self.neighbors))

    def total_active(self):
        return sum(self.coords.values())

    def find_bounds(self):
        current_active = list(map(lambda y: y[0], filter(lambda x: x[1], self.coords.items())))
        x_min = min(map(lambda x: x[0], current_active))
        x_max = max(map(lambda x: x[0], current_active))
        y_min = min(map(lambda x: x[1], current_active))
        y_max = max(map(lambda x: x[1], current_active))
        z_min = min(map(lambda x: x[2], current_active))
        z_max = max(map(lambda x: x[2], current_active))

        return x_min, x_max, y_min, y_max, z_min, z_max

    def cycle(self):
        self.num_cycles += 1
        self._next = self.coords.copy()
        x_min, x_max, y_min, y_max, z_min, z_max = self.find_bounds()
        for pos in itertools.product(range(x_min-1, x_max+2), range(y_min-1, y_max+2), range(z_min-1, z_max+2)):
            active_neighbors = self.num_active_neighbors(pos)
            if self.coords[pos] and (active_neighbors < 2 or active_neighbors > 3):
                self._next[pos] = False
            if not self.coords[pos] and active_neighbors == 3:
                self._next[pos] = True
        self.coords = self._next.copy()


class ConwayCube4:
    def __init__(self, initial_state):
        self.state_map = {".": False, "#": True}
        self.num_cycles = 0
        self.neighbors = list(itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]))
        self.neighbors.remove((0, 0, 0, 0))
        self.coords = collections.defaultdict(bool)
        self._next = self.coords.copy()
        for row, s in enumerate(initial_state):
            for col, c in enumerate(s):
                self.coords[(0, row, col, 0)] = self.state_map[c]

    def _add(self, pos, adj):
        return (pos[0] + adj[0], pos[1] + adj[1], pos[2] + adj[2], pos[3] + adj[3])

    def num_active_neighbors(self, pos):
        return sum(map(lambda x: self.coords[self._add(pos, x)], self.neighbors))

    def total_active(self):
        return sum(self.coords.values())

    def find_bounds(self):
        current_active = list(map(lambda y: y[0], filter(lambda x: x[1], self.coords.items())))
        w_min = min(map(lambda x: x[0], current_active))
        w_max = max(map(lambda x: x[0], current_active))
        x_min = min(map(lambda x: x[1], current_active))
        x_max = max(map(lambda x: x[1], current_active))
        y_min = min(map(lambda x: x[2], current_active))
        y_max = max(map(lambda x: x[2], current_active))
        z_min = min(map(lambda x: x[3], current_active))
        z_max = max(map(lambda x: x[3], current_active))

        return w_min, w_max, x_min, x_max, y_min, y_max, z_min, z_max

    def cycle(self):
        self.num_cycles += 1
        self._next = self.coords.copy()
        w_min, w_max, x_min, x_max, y_min, y_max, z_min, z_max = self.find_bounds()
        for pos in itertools.product(range(w_min-1, w_max+2), range(x_min-1, x_max+2), range(y_min-1, y_max+2), range(z_min-1, z_max+2)):
            active_neighbors = self.num_active_neighbors(pos)
            if self.coords[pos] and (active_neighbors < 2 or active_neighbors > 3):
                self._next[pos] = False
            if not self.coords[pos] and active_neighbors == 3:
                self._next[pos] = True
        self.coords = self._next.copy()


# Test
aa = ConwayCubes(test_data)
while aa.num_cycles < 6:
    aa.cycle()
print(aa.total_active())

aa = ConwayCube4(test_data)
while aa.num_cycles < 6:
    aa.cycle()
print(aa.total_active())


# Part 1
aa = ConwayCubes(data)
while aa.num_cycles < 6:
    aa.cycle()
print(aa.total_active())

# Part 2
aa = ConwayCube4(data)
while aa.num_cycles < 6:
    aa.cycle()
print(aa.total_active())
