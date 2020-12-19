
import itertools
import collections


def read_input_file(infile):
    with open(infile) as f:
        data = [d.strip() for d in f.readlines()]
        break_index = data.index("")
        messages = data[break_index+1:]
        rules = dict()
        depends = dict()
        known_rules = dict()  #collections.defaultdict(None)
        for rule_str in data[:break_index]:
            rule_number, rule_code = rule_str.split(": ", 1)
            rule_number = int(rule_number)
            if rule_code.count("\"") > 0:
                rules[rule_number] = [rule_code[1]]
                known_rules[rule_number] = [rule_code[1]]
                depends[rule_number] = None
            elif rule_code.count("|") > 0:
                left, right = rule_code.split(" | ", 1)
                left = [int(i) for i in left.split(" ")]
                right = [int(j) for j in right.split(" ")]
                depends[rule_number] = set(left) | set(right)
                rules[rule_number] = [left, right]
            else:
                left = [int(i) for i in rule_code.split(" ")]
                depends[rule_number] = set(left)
                rules[rule_number] = [left]
    return messages, rules, known_rules, depends


def find_next_rule(depends, known_rules):
    kn = set(known_rules.keys())
    return list(filter(lambda x: x[0] not in kn and x[1] <= kn, depends.items()))


def _zip(zipped_list, known_rules):
    temp = list(zipped_list)
    # print(temp)
    return "".join(map(lambda x: known_rules[x[1]][x[0]], temp))


def _make(known_rules, rule_list):
    index_prod = list( itertools.product(*map(lambda x: range(len(known_rules[x])), rule_list)) )
    # print(index_prod)
    return list( map(lambda x: _zip(zip(x, rule_list), known_rules), index_prod) )


def make_rule(rules, known_rules, rule_number):
    temp = []
    for x in rules[rule_number]:
        temp += _make(known_rules, x)
        # temp = list(map(lambda x: _make(known_rules, x), rules[rule_number]))
    known_rules[rule_number] = temp


# Part 1
messages, rules, known_rules, depends = read_input_file("./2020/19/input.txt")
next_rules = find_next_rule(depends, known_rules)
while len(next_rules) > 0:
    for r, s in next_rules:
        print(f"Processing rules for rule {r} depending on {s}")
        make_rule(rules, known_rules, r)
    next_rules = find_next_rule(depends, known_rules)


rule_0_match = sum(map(lambda m: m in known_rules[0], messages))
print(f"Messages matching rule 0: {rule_0_match}")


# Part 2
# We have already precomputed all possible combinations of rules 42 and 31 (128 each) (each of 8 characters)
# New rule 0 is equivalent to: for some integers M,N > 0
# anyN(RULE_42) + anyM(RULE_42) + anyM(RULE_31)
RULE_42 = known_rules[42]
RULE_31 = known_rules[31]


def check_message(message, left_rule, right_rule, size=8):
    sub_message = list(map(lambda x: message[size*x:size*x+size], range(len(message)//size)))
    use_left = True
    left_valid = 0
    right_valid = 0
    n = len(sub_message)
    for m in sub_message:
        if use_left:
            if m in left_rule:
                left_valid += 1
            else:
                use_left = False
                if m in right_rule:
                    right_valid += 1
        else:
            if m in right_rule:
                right_valid += 1
    # print(left_valid, right_valid, n)
    return 0 < right_valid < left_valid and left_valid + right_valid == n


rule_0_match = list(map(lambda x: check_message(x, RULE_42, RULE_31, 8), messages))
print(f"Messages matching rule 0: {sum(rule_0_match)}")
