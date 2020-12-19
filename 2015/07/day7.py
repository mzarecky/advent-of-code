
import collections
import re
import functools


def read_input(input_string):
    reg_set = r"^(\w+) -> (\w+)$"
    reg_not = r"^(NOT) (\w+) -> (\w+)$"
    reg_gate = r"^(\w+) (AND|OR|LSHIFT|RSHIFT) (\w+) -> (\w+)$"
    if m := re.match(reg_set, input_string):
        temp = m.groups()
        r = set(list(filter(lambda x: x.isalpha(), [temp[0]])))
        return {"target": temp[-1], "command": "SET", "in1": temp[0], "in2": None, "requires": r}
    elif m := re.match(reg_not, input_string):
        temp = m.groups()
        r = set(list(filter(lambda x: x.isalpha(), [temp[1]])))
        return {"target": temp[-1], "command": temp[0], "in1": temp[1], "in2": None, "requires": r}
    elif m := re.match(reg_gate, input_string):
        temp = m.groups()
        r = set(list(filter(lambda x: x.isalpha(), [temp[0], temp[2]])))
        return {"target": temp[-1], "command": temp[1], "in1": temp[0], "in2": temp[2], "requires": r}
    return None


with open("./2015/07/input.txt") as f:
    data = [read_input(x.strip()) for x in f.readlines()]


class CircuitBoard:
    def __init__(self, connections):
        self.connections = connections.copy()
        self.wires = set()
        self.set_wires()
        self.wire_values = collections.defaultdict(None)

    def _set(self, in1, value):
        self.wires[in1] = value

    def _and(self, in1, in2, target):
        self.wires[target] = self._to16(in1 & in2)

    def _or(self, in1, in2, target):
        self.wires[target] = self._to16(in1 | in2)

    def _lshift(self, in1, in2, target):
        self.wires[target] = self._to16(in1 << in2)

    def _rshift(self, in1, in2, target):
        self.wires[target] = self._to16(in1 >> in2)

    def _not(self, in1, target):
        self.wires[target] = self._to16(~in1)

    def _to16(self, value):
        return value & 65535

    def set_wires(self):
        targets = set(map(lambda x: x["target"], self.connections))
        reqs = functools.reduce(lambda x, y: x | y, map(lambda z: z["requires"], self.connections))
        self.wires = reqs | targets

    def set_wire_values(self):
        pass


aa = CircuitBoard(data)


