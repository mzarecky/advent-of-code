
test_data = [5, 5, 10, 15, 20]
data = [33, 14, 18, 20, 45, 35, 16, 35, 1, 13, 18, 13, 50, 44, 48, 6, 24, 41, 30, 42]
data = sorted(data)


def get_combinations(input_list, target, verbose=False):
    if verbose:
        print(f"Target: {target}; List = {input_list}")
    if sum(input_list) < target:
        return 0

    if sum(input_list) == target:
        return 1

    if len(input_list) == 1:
        return 1 if input_list[0] == target else 0

    if len(input_list) == 2:
        s = 0
        s += (1 if input_list[0] == target else 0)
        s += (1 if input_list[1] == target else 0)
        s += (1 if input_list[0] + input_list[1] == target else 0)
        return s

    b = input_list[-1]
    exc_list = list(filter(lambda x: x <= target, input_list[:-1]))
    inc_list = list(filter(lambda x: x <= target - b, input_list[:-1]))
    return get_combinations(exc_list, target) + get_combinations(inc_list, target - b)


# Part 1
aa = get_combinations(data, 150)
print(f"combos = {aa}")


# Part 2
def get_combinations_size(input_list, target, list_size, target_list_size, verbose=False):
    if verbose:
        print(f"Target: {target}; List = {input_list}")
    if sum(input_list) < target:
        return 0

    if list_size > target_list_size:
        return 0

    if sum(input_list) == target:
        return 1 if list_size + len(input_list) == target_list_size else 0

    if len(input_list) == 1:
        return 1 if input_list[0] == target and list_size + 1 == target_list_size else 0

    if len(input_list) == 2:
        s = 0
        s += (1 if input_list[0] == target and list_size + 1 == target_list_size else 0)
        s += (1 if input_list[1] == target and list_size + 1 == target_list_size else 0)
        s += (1 if input_list[0] + input_list[1] == target and list_size + 2 == target_list_size else 0)
        return s

    b = input_list[-1]
    exc_list = list(filter(lambda x: x <= target, input_list[:-1]))
    inc_list = list(filter(lambda x: x <= target - b, input_list[:-1]))
    return get_combinations_size(exc_list, target, list_size, target_list_size, verbose) + \
           get_combinations_size(inc_list, target - b, list_size + 1, target_list_size, verbose)


aa = get_combinations_size(data, target=150, list_size=0, target_list_size=3)
print(f"combos = {aa}")

# 7: 433
# 6: 459
# 5: 180
# 4: 18
