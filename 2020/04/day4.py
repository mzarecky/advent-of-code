
import functools


def parse_string(x):
    x = x.strip()
    temp = x.split(" ")
    temp = map(lambda y: y.split(":"), temp)
    return {a: b for a, b in temp}


with open("./2020/4/input.txt") as f:
    data = f.readlines()
    data = [d.strip() for d in data]
    s = ""
    output = []
    for d in data:
        if d != "":
            s += " " + d
        else:
            print(s)
            output += [parse_string(s)]
            s = ""
    print(s)
    output += [parse_string(s)]


def is_valid(d):
    req_set = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    in_set = set(d.keys())
    req_set.issubset(in_set)
    return req_set.issubset(in_set)  # req_set == req_set & in_set


def is_byr(x):
    return '1920' <= x <= '2002'


def is_iyr(x):
    return '2010' <= x <= '2020'


def is_eyr(x):
    return '2020' <= x <= '2030'


def is_hgt(x):
    if x.endswith("cm"):
        return 150 <= int(x[0:-2]) <= 193
    elif x.endswith("in"):
        return 59 <= int(x[0:-2]) <= 76
    else:
        return False


def is_hcl(x):
    if x.startswith("#") and len(x) == 7:
        for c in x[1:]:
            if c not in '0123456789abcdef':
                return False
        return True
    else:
        return False


def is_ecl(x):
    return x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def is_pid(x):
    return len(x) == 9 and set(x).issubset(set('0123456789'))


def is_valid2(x):
    if is_valid(x):
        return is_byr(x['byr']) and is_iyr(x['iyr']) and is_eyr(x['eyr']) and is_hgt(x['hgt']) and is_hcl(x['hcl']) \
               and is_ecl(x['ecl']) and is_pid(x['pid'])
    else:
        return False


print(sum(map(is_valid, output)))
print(sum(map(is_valid2, output)))
