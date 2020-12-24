
import collections


def parse_directions(input_string):
    n = len(input_string)
    i = 0
    output = []
    while i < n:
        if input_string[i] in ('n', 's'):
            output.append(input_string[i:i+2])
            i += 2
        else:
            output.append(input_string[i])
            i += 1
    return output


class HexGrid:
    def __init__(self):
        self.grid = collections.defaultdict(bool)
        self.x = 0
        self.y = 0
        self.z = 0
        self.dispatch = {
            "e": self._e,
            "w": self._w,
            "ne": self._ne,
            "nw": self._nw,
            "se": self._se,
            "sw": self._sw
        }

    def _e(self):
        self.x += 1
        self.y -= 1

    def _w(self):
        self.x -= 1
        self.y += 1

    def _ne(self):
        self.x += 1
        self.z -= 1

    def _nw(self):
        self.y += 1
        self.z -= 1

    def _se(self):
        self.y -= 1
        self.z += 1

    def _sw(self):
        self.x -= 1
        self.z += 1

    def check_e(self, pos):
        x, y, z = pos
        return self.grid[(x+1, y-1, z)]

    def check_w(self, pos):
        x, y, z = pos
        return self.grid[(x-1, y+1, z)]

    def check_ne(self, pos):
        x, y, z = pos
        return self.grid[(x+1, y, z-1)]

    def check_nw(self, pos):
        x, y, z = pos
        return self.grid[(x, y+1, z-1)]

    def check_se(self, pos):
        x, y, z = pos
        return self.grid[(x, y-1, z+1)]

    def check_sw(self, pos):
        x, y, z = pos
        return self.grid[(x-1, y, z+1)]

    def move_to_space(self, directions):
        for d in directions:
            self.dispatch[d]()

    def which_touching_black_tile(self):
        temp = list(filter(lambda x: self.grid[x], self.grid.keys()))
        my_set = set()
        for pos in temp:
            my_set.add(pos)
            x, y, z = pos
            my_set.add((x+1, y-1, z))
            my_set.add((x-1, y+1, z))
            my_set.add((x+1, y, z-1))
            my_set.add((x-1, y, z+1))
            my_set.add((x, y+1, z-1))
            my_set.add((x, y-1, z+1))
        return my_set

    def conway_step(self):
        next_grid = collections.defaultdict(bool)
        my_set = self.which_touching_black_tile()
        for pos in my_set:
            state = self.grid[pos]
            num_black = self.check_e(pos) + self.check_w(pos) + self.check_ne(pos) + self.check_nw(pos) + \
                        self.check_se(pos) + self.check_sw(pos)

            # Only update ones that are changing
            if state and (num_black == 0 or num_black > 2):
                next_grid[pos] = False
            elif not state and num_black == 2:
                next_grid[pos] = True

        for p in next_grid:
            self.grid[p] = next_grid[p]

    def flip_tile(self):
        p = (self.x, self.y, self.z)
        self.grid[p] = not self.grid[p]

    def count_black(self):
        return sum(self.grid.values())

    def return_to_center(self):
        self.x, self.y, self.z = 0, 0, 0


# Part 1
with open('./2020/24/input.txt') as f:
    data = [parse_directions(d.strip()) for d in f.readlines()]

hex_grid = HexGrid()
for directions in data:
    hex_grid.return_to_center()
    hex_grid.move_to_space(directions)
    hex_grid.flip_tile()

print(f"Tiles up: {hex_grid.count_black()}")

# Part 2
for j in range(100):
    hex_grid.conway_step()
    ct = hex_grid.count_black()
    print(f"Day {j+1}: {ct}")

