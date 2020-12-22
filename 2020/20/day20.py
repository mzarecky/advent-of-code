
import itertools
import collections
import re


def make_tiles(tiles, size=12):
    all_tiles = {}
    for j in range((len(tiles)+1)//size):
        tile_id = int(tiles[size*j][5:-1])
        all_tiles[tile_id] = tiles[size*j+1:size*j+size-1]
    return all_tiles


class Tile:
    def __init__(self, tile_id, tiles):
        self.tile_id = tile_id
        self.tiles = tiles.copy()
        self.dim = len(tiles)

        # Edges
        self.upper = ""
        self.lower = ""
        self.left = ""
        self.right = ""
        self.set_edges()
        self.all_edges = self.find_possible_edges()

    def __str__(self):
        return "| " + " | \n| ".join(self.tiles) + " |"

    def set_edges(self):
        self.upper = self.tiles[0]
        self.lower = self.tiles[-1]
        self.left = "".join(map(lambda x: x[0], self.tiles))
        self.right = "".join(map(lambda x: x[-1], self.tiles))

    def find_possible_edges(self):
        return {
            self.upper, self.lower, self.right, self.left,
            "".join(reversed(self.upper)), "".join(reversed(self.lower)),
            "".join(reversed(self.right)), "".join(reversed(self.left))
        }

    def compare_edges(self, other):
        return self.all_edges & other.all_edges

    def rotate(self):
        rng = list(range(self.dim - 1, -1, -1))
        output = ["" for _ in range(self.dim)]
        for _ in range(self.dim):
            temp = "".join(map(lambda x: self.tiles[x][_], rng))
            output[_] = temp
        for j, r in enumerate(output):
            self.tiles[j] = r
        self.set_edges()

    def flip(self):
        r = self.dim // 2
        for j in range(r):
            self.tiles[j], self.tiles[self.dim - 1 - j] = self.tiles[self.dim - 1 - j], self.tiles[j]
        self.set_edges()


def find_connections(tiles):
    can_connect = set()
    for t1, t2 in itertools.combinations(tiles.keys(), 2):
        edges = tiles[t1].compare_edges(tiles[t2])
        if edges != set():
            can_connect.add((t1, t2))
            can_connect.add((t2, t1))
    return can_connect


def categorize_tiles(connections):
    output = {"corner": set(), "edge": set(), "inner": set()}
    counts = collections.defaultdict(int)
    for a, b in connections:
        counts[a] += 1
        counts[b] += 1
    for k, v in counts.items():
        if v == 8:
            output["inner"].add(k)
        elif v == 6:
            output["edge"].add(k)
        elif v == 4:
            output["corner"].add(k)
    output["dim"] = len(output["edge"]) // 4 + 2
    return counts, output


with open('./2020/20/input.txt') as f:
    data = [d.strip() for d in f.readlines()]

all_tiles = make_tiles(data)
my_tiles = {k: Tile(k, v) for k, v in all_tiles.items()}
connections = find_connections(my_tiles)
counts, pieces = categorize_tiles(connections)


# Part 1
# Tiles in the corner should have lowest number of connections
temp = sorted(counts.items(), key=lambda x: x[1])
aa = temp[0][0] * temp[1][0] * temp[2][0] * temp[3][0]
print(f"Corner product: {aa}")


# Part 2
def filter_connection(connections, pieces, want):
    temp = list(map(lambda x: x[1], filter(lambda x: x[0] == want, connections)))
    c = list(filter(lambda x: x in pieces["corner"], temp))
    e = list(filter(lambda x: x in pieces["edge"], temp))
    i = list(filter(lambda x: x in pieces["inner"], temp))
    print(f"{want}\n")
    print(f"  corner: {c}")
    print(f"    edge: {e}")
    print(f"   inner: {i}")


with open('./2020/20/test3.txt') as f:
    tile_map = [d.strip().split(" ") for d in f.readlines()]
    tile_map = [list(map(int, _)) for _ in tile_map]


# Manually set upper left corner orientation
def set_orientation(tile_hash, tile_map):
    def compare(curr_id, left_id=None, upper_id=None):
        if left_id is not None:
            a = tile_hash[left_id].right == tile_hash[curr_id].left
        else:
            a = True
        if upper_id is not None:
            b = tile_hash[upper_id].lower == tile_hash[curr_id].upper
        else:
            b = True
        return a and b

    def find_orientation(curr_id, left_id=None, right_id=None):
        if compare(curr_id, left_id, right_id):
            return True
        tile_hash[curr_id].rotate()
        if compare(curr_id, left_id, right_id):
            return True
        tile_hash[curr_id].rotate()
        if compare(curr_id, left_id, right_id):
            return True
        tile_hash[curr_id].rotate()
        if compare(curr_id, left_id, right_id):
            return True
        tile_hash[curr_id].rotate()

        tile_hash[curr_id].flip()
        if compare(curr_id, left_id, right_id):
            return True
        tile_hash[curr_id].rotate()
        if compare(curr_id, left_id, right_id):
            return True
        tile_hash[curr_id].rotate()
        if compare(curr_id, left_id, right_id):
            return True
        tile_hash[curr_id].rotate()
        if compare(curr_id, left_id, right_id):
            return True
        return False

    # set first row
    for i in range(2, len(tile_map[0])):
        curr_id = tile_map[0][i]
        left_id = tile_map[0][i-1]
        upper_id = None
        find_orientation(curr_id, left_id, upper_id)

    # set first col
    for i in range(2, len(tile_map[0])):
        curr_id = tile_map[i][0]
        left_id = None
        upper_id = tile_map[i-1][0]
        find_orientation(curr_id, left_id, upper_id)

    # set everything else
    for i in range(1, len(tile_map[0])):
        for j in range(1, len(tile_map[0])):
            curr_id = tile_map[i][j]
            left_id = tile_map[i][j-1]
            upper_id = tile_map[i-1][j]
            find_orientation(curr_id, left_id, upper_id)


def make_big_map(tile_hash, tile_map):
    def remove_edges(tiles):
        return list(map(lambda x: x[1:-1], tiles[1:-1]))

    def mzip(key_list):
        temp = list(map(lambda x: remove_edges(tile_hash[x].tiles), key_list))
        return list(map(lambda x: "".join(x), zip(*temp)))

    output = []
    for k in tile_map:
        output += mzip(k)
    return output


def check_sea_monster(r1, r2, r3):
    check1 = re.match(r"..................#.", r1)
    check2 = re.match(r"#....##....##....###", r2)
    check3 = re.match(r".#..#..#..#..#..#...", r3)
    # t = r1.count("#") + r2.count("#") + r3.count("#")
    if check1 and check2 and check3:
        return 1
    else:
        return 0


def rotate_map(big_map):
    dim = len(big_map)
    rng = list(range(dim-1, -1, -1))
    output = ["" for _ in range(dim)]
    for _ in range(dim):
        temp = "".join(map(lambda x: big_map[x][_], rng))
        output[_] = temp
    return output


def flip_map(big_map):
    dim = len(big_map)
    r = dim // 2
    for j in range(r):
        big_map[j], big_map[dim-1-j] = big_map[dim-1-j], big_map[j]


def find_sea_monsters(big_map):
    dim = len(big_map)
    roughness = 0
    for row in range(dim-2):
        for col in range(dim-19):
            # print(f"{col}: {big_map[row][col:col+20]}")
            roughness += check_sea_monster(big_map[row][col:col+20], big_map[row+1][col:col+20], big_map[row+2][col:col+20])
    return roughness



set_orientation(my_tiles, tile_map)


big_map = make_big_map(my_tiles, tile_map)
num_pound = sum(map(lambda x: x.count("#"), big_map))

for x in range(1, 11):
    temp = tile_map[x][11]
    temp2 = (temp, tile_map[x+1][11]) in connections and (temp, tile_map[x-1][11]) in connections and (temp, tile_map[x][10]) in connections
    if not temp2:
        print(f"{row}, {col}, {temp}")




temp = find_sea_monsters(big_map)
print(f"Sea monsters: {temp}")
big_map = rotate_map(big_map)
temp = find_sea_monsters(big_map)
print(f"Sea monsters: {temp}")
big_map = rotate_map(big_map)
temp = find_sea_monsters(big_map)
print(f"Sea monsters: {temp}")
big_map = rotate_map(big_map)
temp = find_sea_monsters(big_map)
print(f"Sea monsters: {temp}")
big_map = rotate_map(big_map)
flip_map(big_map)
temp = find_sea_monsters(big_map)
print(f"Sea monsters: {temp}")
big_map = rotate_map(big_map)
temp = find_sea_monsters(big_map)
print(f"Sea monsters: {temp}")
big_map = rotate_map(big_map)
temp = find_sea_monsters(big_map)
print(f"Sea monsters: {temp}")
big_map = rotate_map(big_map)
temp = find_sea_monsters(big_map)
print(f"Sea monsters: {temp}")


r1 = ".#.#...#.###...#.##.##.."
r2 = "#.#.##.###.#.##.##.#####"
r3 = "..##.###.####..#.####.##"
temp = check_sea_monster(r1[2:22], r2[2:22], r3[2:22])
print(temp)


with open('./2020/20/test4.txt') as f:
    big_map = [d.strip() for d in f.readlines()]
