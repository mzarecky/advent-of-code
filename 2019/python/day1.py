
with open("../data/data1.txt") as f:
    data = f.readlines()
    data = [int(x) for x in data]


def fuel_requirement(fuel):
    return max(fuel // 3 - 2, 0)


def fuel_requirement_recursive(fuel):
    need = max(fuel // 3 - 2, 0)
    if need == 0:
        return need
    else:
        return need + fuel_requirement_recursive(need)


# Part 1 ----
print(sum(map(fuel_requirement, data)))

# Part 2 ----
print(sum(map(fuel_requirement_recursive, data)))
