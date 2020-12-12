
with open("./2020/11/input.txt") as f:
    data = f.readlines()
    data = [d.strip() for d in data]


test1 = [
    "L.LL.LL.LL",
    "LLLLLLL.LL",
    "L.L.L..L..",
    "LLLL.LL.LL",
    "L.LL.LL.LL",
    "L.LLLLL.LL",
    "..L.L.....",
    "LLLLLLLLLL",
    "L.LLLLLL.L",
    "L.LLLLL.LL",
]


class SeatLayout:
    def __init__(self, layout):
        self.layout = layout
        self.previous_layout = None
        self.rows = len(layout)
        self.cols = len(layout[0])
        self.num_iterations = 0

    def __str__(self):
        x = "=" * self.rows + "\n"
        x += "\n".join(self.layout) + "\n"
        return x

    def get_adjacent_positions(self, i, j):
        # layout[i][j]
        pos = [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]
        return filter(lambda x: 0 <= x[0] < self.rows and 0 <= x[1] < self.cols, pos)

    def get_occupied_sum(self, i, j):
        # print(f'i={i}, j={j}')
        return sum(map(lambda x: 1 if self.layout[x[0]][x[1]] == "#" else 0, self.get_adjacent_positions(i, j)))

    def next_character(self, i, j):
        num_occupied = self.get_occupied_sum(i, j)
        if num_occupied == 0 and self.layout[i][j] == "L":
            return "#"
        elif num_occupied >= 4 and self.layout[i][j] == "#":
            return "L"
        else:
            return self.layout[i][j]

    def next_layout(self):
        temp = ["" for _ in self.layout]
        for i in range(self.rows):
            it = map(lambda x: (i, x), range(self.cols))
            temp[i] = "".join(map(lambda x: self.next_character(x[0], x[1]), it))
        self.previous_layout = self.layout.copy()
        self.layout = temp.copy()

    def stabilize(self, max_iter=100):
        self.num_iterations = 0
        for j in range(max_iter):
            self.next_layout()
            self.num_iterations += 1
            if self.layout == self.previous_layout:
                break

    def count(self):
        return sum(map(lambda x: x.count("#"), self.layout))


# Part 1
aa = SeatLayout(data)
print(aa)
aa.stabilize(max_iter=1000)
print(f"Occupied Seats: {aa.count()}")


# Part 2
class ViewSeatLayout:
    def __init__(self, layout):
        self.layout = layout
        self.previous_layout = None
        self.rows = len(layout)
        self.cols = len(layout[0])
        self.num_iterations = 0

    def __str__(self):
        x = "=" * self.rows + "\n"
        x += "\n".join(self.layout) + "\n"
        return x

    def look(self, i, j, dir_i, dir_j):
        """Returns 1 if occupied in that direction, else 0"""
        i += dir_i
        j += dir_j
        while 0 <= i < self.rows and 0 <= j < self.cols:
            if self.layout[i][j] == "#":
                return 1
            elif self.layout[i][j] == "L":
                return 0
            i += dir_i
            j += dir_j
        return 0

    def get_occupied_sum(self, i, j):
        directions = [(-1, -1), (-1, 0), (-1, +1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return sum(map(lambda x: self.look(i, j, x[0], x[1]), directions))

    def next_character(self, i, j):
        num_occupied = self.get_occupied_sum(i, j)
        if num_occupied == 0 and self.layout[i][j] == "L":
            return "#"
        elif num_occupied >= 5 and self.layout[i][j] == "#":
            return "L"
        else:
            return self.layout[i][j]

    def next_layout(self):
        temp = ["" for _ in self.layout]
        for i in range(self.rows):
            it = map(lambda x: (i, x), range(self.cols))
            temp[i] = "".join(map(lambda x: self.next_character(x[0], x[1]), it))
        self.previous_layout = self.layout.copy()
        self.layout = temp.copy()

    def stabilize(self, max_iter=100):
        self.num_iterations = 0
        for j in range(max_iter):
            self.next_layout()
            self.num_iterations += 1
            if self.layout == self.previous_layout:
                break

    def count(self):
        return sum(map(lambda x: x.count("#"), self.layout))


aa = ViewSeatLayout(data)
print(aa)
aa.stabilize(max_iter=1000)
print(f"Occupied Seats: {aa.count()}")
