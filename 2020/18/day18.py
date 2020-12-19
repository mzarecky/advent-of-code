
import re

with open("./2020/18/input.txt") as f:
    data = [d.strip() for d in f.readlines()]


def tokenize(input_string, tokens="()+*", digits="0123456789", whitespace=" $"):
    input_string
    output = []

    for s in input_string:
        if s in whitespace:
            continue
        elif s in tokens:
            output += [s]
        elif s in digits:
            output += [int(s)]

    return output


def find_matching_parens(input_list):
    l_paren = []
    matching_paren = []
    for pos, s in enumerate(input_list):
        if s == "(":
            l_paren.append(pos)
        if s == ")":
            c = l_paren.pop()
            matching_paren.append((c, pos))
    return matching_paren


def simple_eval(input_list):
    temp = input_list.copy()
    while len(temp) >= 3:
        if temp[1] == "+":
            s = temp[0] + temp[2]
        elif temp[1] == "*":
            s = temp[0] * temp[2]
        temp = [s] + temp[3:]
    return temp[0]


def simplify(input_list):
    cp = input_list.copy()
    parens = find_matching_parens(cp)
    while len(parens) > 0:
        p1, p2 = parens.pop(0)
        temp = simple_eval(cp[p1+1:p2])
        cp = cp[:p1] + [temp] + cp[p2+1:]
        parens = find_matching_parens(cp)
    return simple_eval(cp)


# Tests
aa = tokenize("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
simplify(aa)

aa = tokenize("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
simplify(aa)

# Part 1
temp = sum(map(lambda x: simplify(tokenize(x)), data))
print(f"Sum of values: {temp}")


# Part 2
def advanced_eval(input_list):
    temp = input_list.copy()
    while "+" in temp:
        pos = temp.index("+")
        s = temp[pos-1] + temp[pos+1]
        temp = temp[:pos-1] + [s] + temp[pos+2:]
    while "*" in temp:
        pos = temp.index("*")
        s = temp[pos-1] * temp[pos+1]
        temp = temp[:pos-1] + [s] + temp[pos+2:]
    return temp[0]


def simplify2(input_list):
    cp = input_list.copy()
    parens = find_matching_parens(cp)
    while len(parens) > 0:
        p1, p2 = parens.pop(0)
        temp = advanced_eval(cp[p1+1:p2])
        cp = cp[:p1] + [temp] + cp[p2+1:]
        parens = find_matching_parens(cp)
    return advanced_eval(cp)


# Tests
advanced_eval([1, "+", 2, "*", 3, "+", 4, "*", 5, "+", 6])
advanced_eval([6, "+", 9, "*", 8, "+", 6])

temp = sum(map(lambda x: simplify2(tokenize(x)), data))
print(f"Sum of values: {temp}")
