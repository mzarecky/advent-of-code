
import re

with open('./2015/23/input.txt') as f:
    instruction_list = [re.split(r"[ ,]+", d.strip()) for d in f.readlines()]


class Computer:
    def __init__(self, instruction_list, reg_a=0, reg_b=0):
        self.instructions = instruction_list
        self.size = len(instruction_list)
        self.registers = {"a": reg_a, "b": reg_b}
        self.current_position = 0

        self.dispatch = {
            "hlf": self._hlf,
            "tpl": self._tpl,
            "inc": self._inc,
            "jmp": self._jmp,
            "jie": self._jie,
            "jio": self._jio
        }

    def _hlf(self, register):
        self.registers[register] //= 2
        self.current_position += 1

    def _tpl(self, register):
        self.registers[register] *= 3
        self.current_position += 1

    def _inc(self, register):
        self.registers[register] += 1
        self.current_position += 1

    def _jmp(self, offset):
        self.current_position += offset

    def _jie(self, register, offset):
        if self.registers[register] % 2 == 0:
            self.current_position += offset
        else:
            self.current_position += 1

    def _jio(self, register, offset):
        if self.registers[register] == 1:
            self.current_position += offset
        else:
            self.current_position += 1

    def run(self):
        self.current_position = 0
        while self.current_position < self.size:
            instruction = instruction_list[self.current_position][0]
            register = instruction_list[self.current_position][1]
            if instruction == "jie" or instruction == "jio":
                offset = int(instruction_list[self.current_position][2])
                self.dispatch[instruction](register, offset)
            elif instruction == "jmp":
                self.dispatch[instruction](int(register))
            else:
                self.dispatch[instruction](register)


# Part 1
c = Computer(instruction_list)
c.run()
print(f"a = {c.registers['a']}, b = {c.registers['b']}")

# Part 2
c = Computer(instruction_list, reg_a=1)
c.run()
print(f"a = {c.registers['a']}, b = {c.registers['b']}")
