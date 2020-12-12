
import re
import itertools


def parse_data(x):
    a = re.match(r"(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).", x).groups()
    units = int(a[2])
    if a[1] == "lose":
        units *= -1
    return a[0], a[3], units


with open("./2015/13/input.txt") as f:
    data = f.readlines()
    data = [parse_data(x) for x in data]
    data = {(a, b): c for a, b, c in data}


def seat_people(input_data):
    people = set()
    for p, q in input_data.keys():
        people.add(p)
        people.add(q)
    n = len(people)
    output = dict()
    for p in itertools.permutations(people, n):
        seating_order = []
        for i in range(n-1):
            seating_order.append((p[i], p[i+1]))
            seating_order.append((p[i], p[i-1]))
        seating_order.append((p[-1], p[0]))
        seating_order.append((p[-1], p[-2]))
        score = sum(map(lambda x: input_data[x], seating_order))
        output[p] = score
    return output


def seat_people2(input_data):
    people = set('Yourself')
    for p, q in input_data.keys():
        people.add(p)
        people.add(q)
    n = len(people)
    output = dict()
    for p in itertools.permutations(people, n):
        seating_order = []
        for i in range(n-1):
            seating_order.append((p[i], p[i+1]))
            seating_order.append((p[i], p[i-1]))
        seating_order.append((p[-1], p[0]))
        seating_order.append((p[-1], p[-2]))
        score = 0
        for k in seating_order:
            if k in input_data:
                score += input_data[k]
        # score = sum(map(lambda x: input_data[x], seating_order))
        output[p] = score
    return output


d = seat_people(data)
best = sorted(d, key=lambda x: d[x])[-1]
print(d[best])


d = seat_people2(data)
best = sorted(d, key=lambda x: d[x])[-1]
print(d[best])

