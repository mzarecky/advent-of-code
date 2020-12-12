
# turn on 605,875 through 960,987
# turn off 328,286 through 869,461
# toggle 673,573 through 702,884
def parse_input(x):
    a = x.split(",")
    b = a[1].split(" through ")
    c = a[0].rsplit(" ", 1)
    return {
        "c": c[0],
        "xs": int(c[1]),
        "ys": int(b[0]),
        "xe": int(b[1]),
        "ye": int(a[2])
    }


def lights_on(lights, xs, xe, ys, ye):
    for i in range(xs, xe+1):
        for j in range(ys, ye+1):
            lights[i][j] = 1


def lights_off(lights, xs, xe, ys, ye):
    for i in range(xs, xe+1):
        for j in range(ys, ye+1):
            lights[i][j] = -1


def lights_toggle(lights, xs, xe, ys, ye):
    for i in range(xs, xe+1):
        for j in range(ys, ye+1):
            lights[i][j] *= -1


def count_lights_on(lights):
    return map(lambda x: sum(map(lambda y: 0 if y == -1 else 1, x)), lights)


def lights_on2(lights, xs, xe, ys, ye):
    for i in range(xs, xe+1):
        for j in range(ys, ye+1):
            lights[i][j] += 1


def lights_off2(lights, xs, xe, ys, ye):
    for i in range(xs, xe+1):
        for j in range(ys, ye+1):
            if lights[i][j] > 0:
                lights[i][j] -= 1


def lights_toggle2(lights, xs, xe, ys, ye):
    for i in range(xs, xe+1):
        for j in range(ys, ye+1):
            lights[i][j] += 2


def count_lights_on2(lights):
    return map(lambda x: sum(x), lights)


with open("./2015/6/input.txt") as f:
    data = f.readlines()
    data = [parse_input(x.strip()) for x in data]


# Do the lighting
all_lights = [[-1 for x in range(1000)] for y in range(1000)]
for d in data:
    command = d['c']
    if command == 'turn on':
        lights_on(all_lights, d['xs'], d['xe'], d['ys'], d['ye'])
    elif command == 'turn off':
        lights_off(all_lights, d['xs'], d['xe'], d['ys'], d['ye'])
    elif command == 'toggle':
        lights_toggle(all_lights, d['xs'], d['xe'], d['ys'], d['ye'])


# Part 1
print(sum(count_lights_on(all_lights)))

# Do the lighting
all_lights = [[0 for x in range(1000)] for y in range(1000)]
for d in data:
    command = d['c']
    if command == 'turn on':
        lights_on2(all_lights, d['xs'], d['xe'], d['ys'], d['ye'])
    elif command == 'turn off':
        lights_off2(all_lights, d['xs'], d['xe'], d['ys'], d['ye'])
    elif command == 'toggle':
        lights_toggle2(all_lights, d['xs'], d['xe'], d['ys'], d['ye'])

# Part 2
print(sum(count_lights_on2(all_lights)))
