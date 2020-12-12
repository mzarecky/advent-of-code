
import itertools


def convert_string(input_string):
    return "".join(map(lambda x: str(x[1]) + x[0], [(k, len(list(g))) for k, g in itertools.groupby(input_string)]))


def repeat_iter(input_string, reps):
    for i in range(reps):
        input_string = convert_string(input_string)
    return input_string


temp = repeat_iter('1321131112', 40)
print(f"Size: {len(temp)} of {temp}")

temp = repeat_iter('1321131112', 50)
print(f"Size: {len(temp)}")
