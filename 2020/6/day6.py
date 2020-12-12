
import functools

with open("./2020/6/input.txt") as f:
    output = []
    temp = []
    data = f.readlines()
    data = [d.strip() for d in data]
    for d in data:
        if d != "":
            temp += [d]
        else:
            output += [temp]
            temp = []


# Part 1
question_sum = sum(map(lambda x: len(set(''.join(x))), output))
print(f"Part 1: {question_sum}")


# Part 2
def find_consensus(input_list):
    responses = list(map(lambda x: set(x), input_list))
    s = functools.reduce(lambda a, b: a & b, responses)
    return len(s)


question_sum = sum(map(lambda x: find_consensus(x), output))
print(f"Part 2: {question_sum}")
