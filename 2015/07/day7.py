
import collections
import re


with open("./2015/07/test1.txt") as f:
    data = [x.strip() for x in f.readlines()]



class CircuitBoard:
    def __init__(self):
        self.wires = collections.defaultdict(None)

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
