
def parse_data(x):
    return x[0], int(x[1:])


with open("./2020/12/input.txt") as f:
    data = f.readlines()
    data = [parse_data(d.strip()) for d in data]


test1 = [("F", 10), ("N", 3), ("F", 7), ("R", 90), ("F", 11)]


class Ship:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.facing = (1, 0)
        self.faces = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        self.ind = {(1, 0): 0, (0, -1): 1, (-1, 0): 2, (0, 1): 3}

    def move_north(self, value):
        self.y_pos += value

    def move_south(self, value):
        self.y_pos -= value

    def move_east(self, value):
        self.x_pos += value

    def move_west(self, value):
        self.x_pos -= value

    def turn_left(self, value):
        current_ind = self.ind[self.facing]
        dir = value // 90
        next_dir = (current_ind - dir) % 4
        self.facing = self.faces[next_dir]

    def turn_right(self, value):
        current_ind = self.ind[self.facing]
        dir = value // 90
        next_dir = (current_ind + dir) % 4
        self.facing = self.faces[next_dir]

    def move_forward(self, value):
        self.x_pos += value * self.facing[0]
        self.y_pos += value * self.facing[1]

    def move(self, command, value):
        if command == "N":
            self.move_north(value)
        if command == "S":
            self.move_south(value)
        if command == "E":
            self.move_east(value)
        if command == "W":
            self.move_west(value)
        if command == "L":
            self.turn_left(value)
        if command == "R":
            self.turn_right(value)
        if command == "F":
            self.move_forward(value)


# Part 1
aa = Ship()
for c, v in data:
    aa.move(c, v)

dist = abs(aa.x_pos) + abs(aa.y_pos)
print(f"Manhattan dist: {dist}")


class Waypoint:
    def __init__(self):
        self.ship_x_pos = 0
        self.ship_y_pos = 0
        self.waypoint_x_pos = 10
        self.waypoint_y_pos = 1

    def move_north(self, value):
        self.waypoint_y_pos += value

    def move_south(self, value):
        self.waypoint_y_pos -= value

    def move_east(self, value):
        self.waypoint_x_pos += value

    def move_west(self, value):
        self.waypoint_x_pos -= value

    def turn_left(self, value):
        times = value // 90
        for _ in range(times):
            self.waypoint_x_pos, self.waypoint_y_pos = -1 * self.waypoint_y_pos, self.waypoint_x_pos

    def turn_right(self, value):
        times = value // 90
        for _ in range(times):
            self.waypoint_x_pos, self.waypoint_y_pos = self.waypoint_y_pos, -1 * self.waypoint_x_pos

    def move_forward(self, value):
        self.ship_x_pos += value * self.waypoint_x_pos
        self.ship_y_pos += value * self.waypoint_y_pos

    def move(self, command, value):
        if command == "N":
            self.move_north(value)
        if command == "S":
            self.move_south(value)
        if command == "E":
            self.move_east(value)
        if command == "W":
            self.move_west(value)
        if command == "L":
            self.turn_left(value)
        if command == "R":
            self.turn_right(value)
        if command == "F":
            self.move_forward(value)


# Part 2
aa = Waypoint()
for c, v in data:
    aa.move(c, v)

dist = abs(aa.ship_x_pos) + abs(aa.ship_y_pos)
print(f"Manhattan dist: {dist}")
