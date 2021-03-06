
import itertools
import collections


class IntegerComputer:
    def __init__(self, program, input_queue=[], feedback_mode=False, verbose=False):
        # self.program = program[:]
        self.program = collections.defaultdict(int, {x: program[x] for x in range(len(program))})
        self.current_pos = 0
        self.relative_pos = 0
        self.op_code = 0
        self.op_mode_1 = 0
        self.op_mode_2 = 0
        self.op_mode_3 = 0
        self.is_done = False
        self.verbose = verbose
        self.feedback_mode = feedback_mode
        self.output_code = 0
        self.input_queue = input_queue

        self.instructions = {
            1: self.__add,
            2: self.__mul,
            3: self.__in,
            4: self.__out,
            5: self.__jnz,
            6: self.__jz,
            7: self.__lt,
            8: self.__eq,
            9: self.__rel_base
        }

    def add_input(self, input_value):
        self.input_queue.append(input_value)

    def _decode_op_code(self, pos):
        op_code = self.program[pos]
        digits = [0, 0, 0, 0, 0]
        pos = len(digits) - 1
        while op_code > 0 and pos >= 0:
            digits[pos] = op_code % 10
            op_code //= 10
            pos -= 1
        self.op_code = digits[3] * 10 + digits[4]
        self.op_mode_1 = digits[2]
        self.op_mode_2 = digits[1]
        self.op_mode_3 = digits[0]

    def _get_parameter(self, pos, mode):
        """
        0 -> Positional Mode
        1 -> Immediate Mode
        2 -> Relative Mode
        """
        if mode == 0:
            return self.program[self.program[pos]]
        elif mode == 1:
            return self.program[pos]
        elif mode == 2:
            print(self.program[pos])
            return self.program[self.relative_pos + self.program[pos]]
        else:
            print(f"Unknown Mode: {mode}")
            raise ValueError

    def _get_input_position(self, pos, mode):
        if mode == 0:
            return self.program[pos]
        elif mode == 1:
            raise ValueError
        elif mode == 2:
            return self.relative_pos + self.program[pos]
        else:
            print(f"Bad Input Mode: {mode}")
            raise ValueError

    def __add(self):
        op1 = self._get_parameter(self.current_pos + 1, self.op_mode_1)
        op2 = self._get_parameter(self.current_pos + 2, self.op_mode_2)
        dest = self._get_input_position(self.current_pos + 3, self.op_mode_3)
        self.program[dest] = op1 + op2
        self.current_pos += 4

    def __mul(self):
        op1 = self._get_parameter(self.current_pos + 1, self.op_mode_1)
        op2 = self._get_parameter(self.current_pos + 2, self.op_mode_2)
        dest = self._get_input_position(self.current_pos + 3, self.op_mode_3)
        self.program[dest] = op1 * op2
        self.current_pos += 4

    def __in(self):
        dest = self._get_input_position(self.current_pos + 1, self.op_mode_1)
        self.program[dest] = self.input_queue.pop(0)
        self.current_pos += 2

    def __out(self):
        self.output_code = self._get_parameter(self.current_pos + 1, self.op_mode_1)
        self.current_pos += 2
        if self.verbose:
            print(f"output code = {self.output_code}")
        if self.feedback_mode:
            return self.output_code

    def __jnz(self):
        op1 = self._get_parameter(self.current_pos + 1, self.op_mode_1)
        op2 = self._get_parameter(self.current_pos + 2, self.op_mode_2)
        if op1 != 0:
            self.current_pos = op2
        else:
            self.current_pos += 3

    def __jz(self):
        op1 = self._get_parameter(self.current_pos + 1, self.op_mode_1)
        op2 = self._get_parameter(self.current_pos + 2, self.op_mode_2)
        if op1 == 0:
            self.current_pos = op2
        else:
            self.current_pos += 3

    def __lt(self):
        op1 = self._get_parameter(self.current_pos + 1, self.op_mode_1)
        op2 = self._get_parameter(self.current_pos + 2, self.op_mode_2)
        dest = self._get_input_position(self.current_pos + 3, self.op_mode_3)
        self.program[dest] = 1 if op1 < op2 else 0
        self.current_pos += 4

    def __eq(self):
        op1 = self._get_parameter(self.current_pos + 1, self.op_mode_1)
        op2 = self._get_parameter(self.current_pos + 2, self.op_mode_2)
        dest = self._get_input_position(self.current_pos + 3, self.op_mode_3)
        self.program[dest] = 1 if op1 == op2 else 0
        self.current_pos += 4

    def __rel_base(self):
        self.relative_pos += self._get_parameter(self.current_pos + 1, self.op_mode_1)
        if self.verbose:
            print(f"New relative position: {self.relative_pos}")
        self.current_pos += 2

    def run(self):
        while self.program[self.current_pos] != 99:
            self._decode_op_code(self.current_pos)

            if self.op_code in self.instructions:
                self.instructions[self.op_code]()
            else:
                print(f"Unknown op_code: {self.op_code}")
                raise ValueError

        return self.output_code


def get_program(file):
    with open(file) as f:
        return list(map(int, f.read().split(',')))


def get_program_from_input(ins: str):
    return list(map(int, ins.split(",")))


# Tests ----
my_program = get_program_from_input("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
aa = IntegerComputer(my_program, [])
aa.run()

my_program = get_program_from_input("1102,34915192,34915192,7,4,7,99,0")
aa = IntegerComputer(my_program, [])
aa.run()

my_program = get_program_from_input("104,1125899906842624,99")
aa = IntegerComputer(my_program, [])
aa.run()


# Part 1 ----
infile = "../data/data9.txt"
my_program = get_program(infile)
aa = IntegerComputer(my_program, [1])
aa.run()


# Part 2 ----
infile = "../data/data9.txt"
my_program = get_program(infile)
aa = IntegerComputer(my_program, [2])
aa.run()
