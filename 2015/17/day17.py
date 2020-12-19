
test_data = [5, 5, 10, 15, 20]
data = [33, 14, 18, 20, 45, 35, 16, 35, 1, 13, 18, 13, 50, 44, 48, 6, 24, 41, 30, 42]
data = sorted(data)


def get_combinations(input_list, target):
    print(f"Target: {target}; List = {input_list}")
    if len(input_list) == 0:
        return 0

    if len(input_list) == 1:
        return 1 if input_list[0] == target else 0

    if len(input_list) == 2:
        s = 0
        s += (1 if input_list[0] == target else 0)
        s += (1 if input_list[1] == target else 0)
        s += (1 if input_list[0] + input_list[1] == target else 0)
        return s

    if sum(input_list) < target:
        return 0

    b = input_list[-1]
    exc_list = list(filter(lambda x: x <= target, input_list[:-1]))
    inc_list = list(filter(lambda x: x <= target - b, input_list[:-1]))
    return get_combinations(exc_list, target) + get_combinations(inc_list, target - b)


aa = get_combinations(test_data, 25)
print(f"combos = {aa}")
