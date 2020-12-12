
with open("./2020/10/input.txt") as f:
    data = f.readlines()
    data = sorted([int(d.strip()) for d in data])


test1 = sorted([16,10,15,5,1,11,7,19,6,12,4])
test2 = sorted([28,33,18,42,31,14,46,20,48,47,24,23,49,45,19,38,39,11,1,32,25,35,8,17,7,9,4,2,34,10,3])


def make_connections(input_list):
    temp = input_list.copy()
    temp = [0] + temp + [max(temp)+3]
    connections = list(zip(temp[:-1], temp[1:]))
    x1 = 0
    x3 = 0
    for j in map(lambda x: x[1]-x[0], connections):
        if j == 1:
            x1 += 1
        if j == 3:
            x3 += 1
    return x1, x3


x1, x3 = make_connections(test1)
print(f"1: {x1}, 3: {x3}, product: {x1*x3}")

x1, x3 = make_connections(test2)
print(f"1: {x1}, 3: {x3}, product: {x1*x3}")

# Part 1
x1, x3 = make_connections(data)
print(f"1: {x1}, 3: {x3}, product: {x1*x3}")


# Part 2
def find_combinations(input_list):
    if len(input_list) <= 2:
        return 1
    if len(input_list) == 3:
        if input_list[2] - input_list[0] <= 3:
            return 2
        else:
            return 1
    # lengths here are >= 4
    a = find_combinations(input_list[1:])
    if input_list[2] - input_list[0] <= 3:
        b = find_combinations(input_list[2:])
    else:
        b = 0
    if input_list[3] - input_list[0] <= 3:
        c = find_combinations(input_list[3:])
    else:
        c = 0

    return a + b + c


def find_forced(input_list):
    temp = input_list.copy()
    temp = [0] + temp + [max(temp) + 3]
    print(temp)
    t = list(enumerate(zip(temp[:-1], temp[1:])))
    forced = list(filter(lambda x: x[1][1] - x[1][0] == 3, t))
    f_ind = list(map(lambda x: x[0], forced))

    d = list(zip(f_ind[:-1], f_ind[1:]))

    bb = 1
    for left, right in d:
        print(temp[(left+1):(right+1)])
        bb *= find_combinations(temp[(left+1):(right+1)])
    return temp, t, forced, f_ind, bb


temp, t, forced, f_ind, bb = find_forced(data)

#find_combinations()
