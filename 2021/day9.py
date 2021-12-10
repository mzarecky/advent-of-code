
import itertools


def parse_data(s):
    return [int(d) for d in s.strip()]


with open("./2021/data/day9.txt") as f:
    d = f.readlines()
    data = list(map(parse_data, d))


class SmokeBasin:
    def __init__(self, data):
        self.data = data
        self.dim_x = len(data[0])
        self.dim_y = len(data)
        self.low_points = []
        self.basin_locs = []
        self.risk_level = 0
        self.basins = {}

    @staticmethod
    def next_points(point_x, point_y):
        return [(point_x - 1, point_y), (point_x + 1, point_y), (point_x, point_y - 1), (point_x, point_y + 1)]

    def adjacency_generator(self, point_x, point_y):
        pts = self.next_points(point_x, point_y)
        return list(filter(lambda x: 0 <= x[0] < self.dim_x and 0 <= x[1] < self.dim_y, pts))

    def basin_adjacency_generator(self, point_x, point_y):
        pts = self.adjacency_generator(point_x, point_y)
        return list(filter(lambda x: data[x[1]][x[0]] != 9, pts))

    def find_low_points(self):
        self.low_points = []
        self.basin_locs = []
        for x, y in itertools.product(range(self.dim_x), range(self.dim_y)):
            current_value = self.data[y][x]
            if all(map(lambda z: current_value < self.data[z[1]][z[0]], self.adjacency_generator(x, y))):
                self.low_points.append(current_value)
                self.basin_locs.append((x, y))
        self.risk_level = sum(self.low_points) + len(self.low_points)

    def find_basin(self, point_x, point_y):
        found = {(point_x, point_y)}
        adj = {(point_x, point_y)}
        for pts in map(lambda x: self.basin_adjacency_generator(*x), found):
            adj.update(pts)

        while found != adj:
            tmp = adj.difference(found)
            for adj_pts, current_pt in zip(map(lambda x: self.basin_adjacency_generator(*x), tmp), tmp):
                found.update([current_pt])
                adj.update(adj_pts)

        self.basins[(point_x, point_y)] = found

    def find_all_basins(self):
        self.basins = {}
        for x, y in self.basin_locs:
            self.find_basin(x, y)


# Part 1
aa = SmokeBasin(data)
aa.find_low_points()
print(f"Risk level: {aa.risk_level}")

# Part 2
aa.find_all_basins()
cc = list(map(lambda x: len(x), aa.basins.values()))
cc.sort(reverse=True)
print(f"Largest Basins: {cc[0]} * {cc[1]} * {cc[2]} = {cc[0]*cc[1]*cc[2]}")

