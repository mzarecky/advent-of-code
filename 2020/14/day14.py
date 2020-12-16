
import collections
import itertools


class BitmaskSystem:
    def __init__(self):
        self.mask = ""
        self.x_mask = 0
        self.x_bits = {}
        self.write_mask = 0
        self.mem = collections.defaultdict(int)

    def read_mask(self, m):
        self.mask = m
        temp = filter(lambda x: x[1] == "X", enumerate(m))
        self.x_mask = sum(map(lambda x: 2**(35-x[0]), temp))
        temp = filter(lambda x: x[1] == "1", enumerate(m))
        self.write_mask = sum(map(lambda x: 2 ** (35 - x[0]), temp))

    def decode_mask(self, m):
        self.mask = m
        temp = list(filter(lambda x: x[1] == "X", enumerate(m)))
        self.x_mask = sum(map(lambda x: 2 ** (35 - x[0]), temp))
        self.x_bits = list(map(lambda x: (2**(35-x[0]), 0), temp))
        temp = filter(lambda x: x[1] == "1", enumerate(m))
        self.write_mask = sum(map(lambda x: 2 ** (35 - x[0]), temp))

    def write_memory(self, address, value):
        a = (address,)
        self.mem[a] = self.write_mask + (value & self.x_mask)

    def decode_memory(self, address, value):
        a = address - (self.x_mask & address)  # Zero out x
        a = a | self.write_mask
        for j in itertools.product(*self.x_bits):
            temp = a + sum(j)
            self.mem[(temp,)] = value

    def sum_of_memory(self):
        return sum(self.mem.values())

    def read_input(self, input_string):
        """
        mask = 1X11X010X000X0X101X00100011X10100111
        mem[40278] = 36774405
        """
        temp = input_string.split(" = ")
        if temp[0] == "mask":
            self.read_mask(temp[1])
        else:
            val = int(temp[1])
            addr = int(temp[0][4:-1])
            self.write_memory(addr, val)

    def decode_input(self, input_string):
        """
        mask = 1X11X010X000X0X101X00100011X10100111
        mem[40278] = 36774405
        """
        temp = input_string.split(" = ")
        if temp[0] == "mask":
            self.decode_mask(temp[1])
        else:
            val = int(temp[1])
            addr = int(temp[0][4:-1])
            self.decode_memory(addr, val)


# Tests ----
aa = BitmaskSystem()
aa.decode_mask("000000000000000000000000000000X1001X")
aa.decode_memory(42, 100)
aa.decode_mask("00000000000000000000000000000000X0XX")
aa.decode_memory(26, 1)
print(f"Sum of memory: {aa.sum_of_memory()}")

aa.read_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
aa.write_memory(8, 11)


# Data ----
with open("./2020/14/input.txt") as f:
    data = f.readlines()
    data = [d.strip() for d in data]


# Part 1 ----
aa = BitmaskSystem()
for d in data:
    aa.read_input(d)

print(f"Sum of memory: {aa.sum_of_memory()}")


# Part 2 ----
aa = BitmaskSystem()
for d in data:
    aa.decode_input(d)

print(f"Sum of memory: {aa.sum_of_memory()}")
