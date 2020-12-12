
with open("./2015/2/input.txt") as f:
    a = f.readlines()
    a = [[int(y) for y in x.strip().split("x")] for x in a]


def get_paper_area(x):
    a, b, c = x[0] * x[1], x[0] * x[2], x[1] * x[2]
    slack = min(a, b, c)
    return 2 * (a + b + c) + slack


def get_ribbon_length(x):
    a, b, c = 2 * (x[0] + x[1]), 2 * (x[0] + x[2]), 2 * (x[1] + x[2])
    bow = x[0] * x[1] * x[2]
    return min(a, b, c) + bow


temp = sum(get_paper_area(x) for x in a)
print(f"Part 1 {temp}")

temp = sum(get_ribbon_length(x) for x in a)
print(f"Part 2 {temp}")
