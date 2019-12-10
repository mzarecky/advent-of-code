
import collections


class WirePath:
    def __init__(self, wire_path):
        self.wire_path = wire_path
        self.x_pos = 0
        self.y_pos = 0
        self.position = 0
        self.full_path = collections.defaultdict(list)

        self.dispatch = {
            "U": self._up,
            "D": self._down,
            "L": self._left,
            "R": self._right
        }
        self._traverse_path()

    def _up(self): self.y_pos += 1

    def _down(self): self.y_pos -= 1

    def _right(self): self.x_pos += 1

    def _left(self): self.x_pos -= 1

    def _traverse_path(self):
        for direction in self.wire_path:
            my_direction = direction[0]
            for j in range(direction[1]):
                self.dispatch[my_direction]()
                self.position += 1
                self.full_path[(self.x_pos, self.y_pos)].append(self.position)


def find_intersections(wire1: WirePath, wire2: WirePath):
    set1 = set(wire1.full_path.keys())
    set2 = set(wire2.full_path.keys())
    return set1.intersection(set2)


def solution_1(w1, w2):
    wire_1 = WirePath(w1)
    wire_2 = WirePath(w2)
    crosses = find_intersections(wire_1, wire_2)
    return min([abs(x[0]) + abs(x[1]) for x in crosses])


def solution_2(w1, w2):
    wire_1 = WirePath(w1)
    wire_2 = WirePath(w2)
    crosses = find_intersections(wire_1, wire_2)
    return min([sum(x) for x in zip([min(wire_1.full_path[x]) for x in crosses],
                                    [min(wire_2.full_path[x]) for x in crosses])])


def to_wire_tuple(data):
    return [(x[0], int(x[1:])) for x in data]


with open("../data/data3.txt") as f:
    data = f.readlines()
    data = [to_wire_tuple(x.strip().split(",")) for x in data]

print(solution_1(data[0], data[1]))
print(solution_2(data[0], data[1]))


# Tests ----
data = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
data = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
data = [to_wire_tuple(x.strip().split(",")) for x in data]

wire_1 = WirePath(data[0])
wire_2 = WirePath(data[1])
crosses = find_intersections(wire_1, wire_2)
print(crosses)
