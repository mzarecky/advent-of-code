
with open("./2015/8/input.txt") as f:
    data = f.readlines()
    data = [x.strip() for x in data]


def rep2mem(x):
    # no surrounding "
    x = x[1:-1]
    output = ""
    r = range(len(x))
    skip = 0
    for i in r:
        if skip > 0:
            skip -= 1
            continue
        if x[i] == "\\":
            if x[i+1] in ["\"", "\\"]:
                output += x[i+1]
                skip = 1
            elif x[i+1] == "x":
                output += chr(int(x[i+2:i+4], 16))
                skip = 3
        else:
            output += x[i]
    return output


def mem2rep(x):
    output = "\""
    for c in x:
        if c == "\"":
            output += "\\\""
        elif c == "\\":
            output += "\\\\"
        else:
            output += c
    output += "\""
    return output


def part1(x):
    print(sum(map(lambda y: len(y) - len(rep2mem(y)), x)))


def part2(x):
    print(sum(map(lambda y: len(mem2rep(y)) - len(y), x)))
