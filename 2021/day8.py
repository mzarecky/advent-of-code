
def parse_data(s):
    temp = s.strip().split(' | ')
    return temp[0].split(' '), temp[1].split(' ')


def count_uniques(iter):
    def is_unique(s):
        return len(s) in (2, 3, 4, 7)  # 1, 7, 4, 8
    return sum(map(is_unique, iter))


with open("./2021/data/day8.txt") as f:
    d = f.readlines()
    data = list(map(parse_data, d))


displays = (
    'abcefg',  # 0
    'cf',  # 1
    'acdeg',  # 2
    'acdfg',  # 3
    'bcdf',  # 4
    'abdfg',  # 5
    'abdefg',  # 6
    'acf',  # 7
    'abcdefg',  # 8
    'abcdfg'   # 9
)

potentials = {
    2: 1,
    3: 7,
    4: 4,
    #5: [2, 3, 5],
    #6: [0, 6, 9],
    7: 8
}


def setup_mapper(display):
    output = {i: None for i in range(10)}
    unknowns = []
    for d in display:
        n = len(d)
        if n in potentials:
            output[potentials[n]] = d
        else:
            unknowns.append(d)
    return output, unknowns


def determine_unknowns(knowns, display):
    temp = set(display)
    if len(temp) == 5:
        if len(temp & set(knowns[1])) == 2:
            return 3
        elif len(temp & set(knowns[4])) == 3:
            return 5
        else:
            return 2
    else:
        if len(temp & set(knowns[1])) != 2:
            return 6
        elif len(temp & set(knowns[4])) == 4:
            return 9
        else:
            return 0


def reflect_dict(mapping):
    return {''.join(sorted(v)): k for k, v in mapping.items()}


def get_display(signals, outputs):
    knowns, unknowns = setup_mapper(signals)
    for display in unknowns:
        knowns[determine_unknowns(knowns, display)] = display

    rev = reflect_dict(knowns)
    aa = list(map(lambda x: rev[''.join(sorted(x))], outputs))
    return 1000 * aa[0] + 100 * aa[1] + 10 * aa[2] + aa[3]


# Part 1
print(sum(map(lambda x: count_uniques(x[1]), data)))

# Part 2
print(sum(map(lambda x: get_display(*x), data)))
