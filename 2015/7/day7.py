
import collections
import re


def parse_input(x):
    """
    y AND ae -> ag
    hv OR hu -> hw
    1674 -> b
    NOT ac -> ad
    dd RSHIFT 1 -> dw
    u LSHIFT 1 -> ao
    """
    a = x.split(" -> ")
    target = a[1]
    left = a[0].split(" ")
    if left[0] == "NOT":
        func = left[0]
        p1 = left[1]
        p2 = None
        v1 = p1.isalpha()
        v2 = False
    elif len(left) == 1:
        func = "INPUT"
        p1 = left[0]
        p2 = None
        v1 = p1.isalpha()
        v2 = False
    else:
        func = left[1]
        p1 = left[0]
        p2 = left[2]
        v1 = p1.isalpha()
        v2 = p2.isalpha()
    return {
        "target": target,
        "func": func,
        "p1": p1,
        "p2": p2,
        "v1": v1,
        "v2": v2
    }


def get_wires(circuit_list):
    my_set = set()
    for c in circuit_list:
        my_set.add(c["target"])
        if c["v1"]:
            my_set.add(c["p1"])
        if c["v2"]:
            my_set.add(c["p2"])
    return my_set


def order_circuits(circuit_list):
    pass


with open("./2015/7/test1.txt") as f:
    data = f.readlines()
    data = [parse_input(x.strip()) for x in data]

