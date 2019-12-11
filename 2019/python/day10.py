
import math
import collections


class AsteroidMap:
    def __init__(self, asteroid_map):
        self.width = len(asteroid_map[0])
        self.height = len(asteroid_map)
        self.am = {(x, y): my_am[y][x] for y in range(len(asteroid_map)) for x in range(len(asteroid_map[0]))}
        self.asteroid_locations = [x for x in self.am.keys() if self.am[x] == "#"]

    def is_visible(self, src, dest):
        dir_x = dest[0] - src[0]
        dir_y = dest[1] - src[1]
        n = math.gcd(dir_x, dir_y)
        # n * <unit_x, unit_y>
        dir_x //= n
        dir_y //= n
        if self.am[dest] == ".":
            return False
        if n == 1:
            return True
        for j in range(1, n):
            if self.am[(src[0] + dir_x * j, src[1] + dir_y * j)] == "#":
                return False
        return True

    def find_all_visible_asteroids(self, src):
        num_found = 0
        for j in self.asteroid_locations:
            if j == src:
                continue
            if self.is_visible(src, j):
                num_found += 1
        return num_found

    @staticmethod
    def get_angle(src, dest):
        dy = dest[1] - src[1]
        dx = dest[0] - src[0]
        if dx == 0:
            return -90.0 if dy < 0 else 90.0
            # return 0 if dy > 0 else 180.0
        elif dy == 0:
            return 180.0 if dx < 0 else 0.0
            # return 90.0 if dx > 0 else 270.0
        elif dx < 0 and dy > 0:
            # Quadrant 4 is the special case
            return math.degrees(math.atan2(dy, dx))
        else:
            return math.degrees(math.atan2(dy, dx))

    @staticmethod
    def reorder_angle(angle):
        return 450.0 + angle if angle < -90.0 else angle + 90.0

    @staticmethod
    def get_dist(src, dest):
        return (dest[1]-src[1])**2 + (dest[0]-src[0])**2

    def stats_from_location(self, src):
        """
        Due to orientation of map, start at -90.0 moving counter-clockwise
        """
        return {d: {"angle": self.reorder_angle(self.get_angle(src, d)),
                    "dist": self.get_dist(src, d),
                    "dx": d[0]-src[0],
                    "dy": d[1]-src[1]} for d in self.asteroid_locations if d != src}


def find_best_asteroid(asteroid_map: AsteroidMap):
    best_found = 0
    best_location = None
    num_found = 0
    for src in asteroid_map.asteroid_locations:
        num_found = asteroid_map.find_all_visible_asteroids(src)
        if num_found > best_found:
            best_found = num_found
            best_location = src
    return best_found, best_location


def make_angle_map(angle_stats):
    kk = collections.defaultdict(list)
    for j in angle_stats:
        kk[angle_stats[j]["angle"]].append((angle_stats[j]["dist"], j))
    for j in kk:
        kk[j] = sorted(kk[j], key=lambda x: x[0])
    return kk


def print_in_order(angle_map, want_pos, verbose=False):
    max_depth = max([len(angle_map[x]) for x in angle_map])
    pos = 0
    for current_depth in range(max_depth):
        for angle in sorted(angle_map.keys()):
            if len(angle_map[angle]) >= (current_depth+1):
                pos += 1
                if verbose or want_pos == pos:
                    print(pos, "; ", angle_map[angle][current_depth])


if __name__ == "__main__":
    # Part 1 ----
    with open("../data/data10.txt") as f:
        my_am = f.readlines()
    my_am = [x.strip() for x in my_am]

    aa = AsteroidMap(my_am)
    best_found, best_loc = find_best_asteroid(aa)
    print("Found", best_found, "asteroids at", best_loc)  # 288 at (17,22)
    bb = aa.stats_from_location(best_loc)
    cc = make_angle_map(bb)

    # Part 2 ----
    print_in_order(cc, 200, verbose=False)  # 200 ;  (157, (6, 16))
