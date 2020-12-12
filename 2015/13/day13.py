
import re
import itertools


def parse_data(x):
    a = re.match(r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.", x).groups()
    return {
        "deer": a[0],
        "speed": int(a[1]),
        "duration": int(a[2]),
        "rest": int(a[3]),
        "total": int(a[2]) + int(a[3]),
        "max_distance": int(a[1]) * int(a[2])
    }


with open("./2015/14/input.txt") as f:
    data = f.readlines()
    data = [parse_data(x) for x in data]


def decompose(n, duration, rest):
    total = duration + rest
    ktimes = n // total
    remainder = n % total
    if remainder >= duration:
        return ktimes, duration, remainder - duration
    else:
        return ktimes, remainder, 0


def fly_n_seconds(deer_dict, num_seconds):
    k_times, sec_duration, sec_rest = decompose(num_seconds, deer_dict["duration"], deer_dict["rest"])
    total_dist = k_times * deer_dict["max_distance"] + sec_duration * deer_dict["speed"]
    return total_dist


def fly_gen(speed, duration, rest):
    total = duration + rest
    current_dist = 0
    i = 0
    while True:
        if i < duration:
            current_dist += speed
        i += 1
        if i == total:
            i = 0
        yield current_dist


comet = fly_gen(16, 11, 162)
for j in range(1000):
    a = next(comet)
    print(a)

deer = [
    fly_gen(22, 8, 165),
    fly_gen(8, 17, 114),
    fly_gen(18, 6, 103),
    fly_gen(25, 6, 145),
    fly_gen(11, 12, 125),
    fly_gen(21, 6, 121),
    fly_gen(18, 3, 50),
    fly_gen(20, 4, 75),
    fly_gen(7, 20, 119)
]

deer = [
    fly_gen(14, 10, 127),
    fly_gen(16, 11, 162)
]

distances = [0] * len(deer)
points = [0] * len(deer)
for j in range(2503):
    for i in range(len(deer)):
        distances[i] = next(deer[i])

    # update points
    a = sorted(enumerate(distances), key=lambda x: x[1])
    max_d = a[-1][1]

    for k in filter(lambda x: x[1] == max_d, a):
        points[k[0]] += 1


distances = list(map(lambda x: (x["deer"], fly_n_seconds(x, 2503)), data))
temp = sorted(distances, key=lambda x: x[1])
print(f"Winning deer is {temp[-1][0]} at distance {temp[-1][1]}")
