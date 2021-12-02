
import json
import re

with open('./2015/12/input.txt') as f:
    input_data = f.readline()

data = json.loads(input_data)

# Lazy Part 1 ----
m = re.findall(r'([-]?\d+)', input_data)
temp = sum(map(lambda x: int(x), m))
print(f"Sum of numbers: {temp}")


# Part 2 ----
def find_values(input_structure, ignore_red_values=False, verbose=False):
    if isinstance(input_structure, list):
        if verbose:
            print(f"list: {input_structure}")
        return sum(map(lambda x: find_values(x, ignore_red_values, verbose), input_structure))
    elif isinstance(input_structure, dict):
        if verbose:
            print(f"dict: {input_structure}")
        any_red = any(map(lambda x: x == 'red', input_structure.values()))
        if ignore_red_values and any_red:
            return 0
        return sum(map(lambda x: find_values(x, ignore_red_values, verbose), input_structure.values()))
    elif isinstance(input_structure, int):
        if verbose:
            print(f"    int: {input_structure}")
        return input_structure
    else:
        if verbose:
            print(f"    string: {input_structure}")
        return 0


temp = find_values(data)
print(f"Sum of values including red: {temp}")
temp = find_values(data, ignore_red_values=True)
print(f"Sum of values including red: {temp}")
