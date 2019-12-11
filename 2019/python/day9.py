
import itertools
import collections


class IntegerComputer:
    def __init__(self, program, input_queue=[], feedback_mode=False):
        # self.program = program[:]
        self.program = collections.defaultdict(int, {x: program[x] for x in range(len(program))})
        self.current_pos = 0
        self.relative_pos = 0
        self.op_code = 0
        self.op_mode_1 = 0
        self.op_mode_2 = 0
        self.op_mode_3 = 0
        self.is_done = False
        self.feedback_mode = feedback_mode
        self.output_code = 0
        self.input_queue = input_queue

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

    def _get_op1(self, pos):
        if self.op_mode_1 == 0:
            return self.program[self.program[pos + 1]]
        elif self.op_mode_1 == 1:
            return self.program[pos + 1]
        elif self.op_mode_1 == 2:
            print(self.program[pos+1])
            return self.program[self.relative_pos + self.program[pos + 1]]
        else:
            raise ValueError

    def _get_op2(self, pos):
        if self.op_mode_2 == 0:
            return self.program[self.program[pos + 2]]
        elif self.op_mode_2 == 1:
            return self.program[pos + 2]
        elif self.op_mode_2 == 2:
            print(self.program[pos+2])
            return self.program[self.relative_pos + self.program[pos + 2]]
        else:
            raise ValueError

    def run(self):
        while self.current_pos < len(self.program):
            self._decode_op_code(self.current_pos)
            print("code: ", self.program[self.current_pos], ",", self.program[self.current_pos + 1], ",",
                  self.program[self.current_pos + 2], ",", self.program[self.current_pos + 3])
            if self.op_code == 1 or self.op_code == 2:
                op1 = self._get_op1(self.current_pos)
                op2 = self._get_op2(self.current_pos)
                dest = self.program[self.current_pos + 3]
                if self.op_code == 1:
                    self.program[dest] = op1 + op2 if self.op_code == 1 else op1 * op2
                else:
                    self.program[dest] = op1 * op2
                self.current_pos += 4
            elif self.op_code == 3:
                op1 = self._get_op1(self.current_pos)
                self.program[op1] = self.input_queue.pop(0)
                # self.program[self.program[self.current_pos + 1]] = self.input_queue.pop(0)
                self.current_pos += 2
            elif self.op_code == 4:
                op1 = self._get_op1(self.current_pos)
                self.output_code = op1
                self.current_pos += 2
                print("output code =", self.output_code)
                if self.feedback_mode:
                    return self.output_code
            elif self.op_code == 5 or self.op_code == 6:
                op1 = self._get_op1(self.current_pos)
                op2 = self._get_op2(self.current_pos)
                if (self.op_code == 5 and op1 != 0) or (self.op_code == 6 and op1 == 0):
                    self.current_pos = op2
                else:
                    self.current_pos += 3
            elif self.op_code == 7:
                op1 = self._get_op1(self.current_pos)
                op2 = self._get_op2(self.current_pos)
                self.program[self.program[self.current_pos + 3]] = 1 if op1 < op2 else 0
                self.current_pos += 4
            elif self.op_code == 8:
                op1 = self._get_op1(self.current_pos)
                op2 = self._get_op2(self.current_pos)
                self.program[self.program[self.current_pos + 3]] = 1 if op1 == op2 else 0
                self.current_pos += 4
            elif self.op_code == 9:
                op1 = self._get_op1(self.current_pos)
                self.relative_pos += op1
                print("relative position:", self.relative_pos)
                self.current_pos += 2
            elif self.op_code == 99:
                self.is_done = True
                break
            else:
                print("unknown op_code")
                break
        return self.output_code


def get_program(file):
    with open(file) as f:
        return list(map(int, f.read().split(',')))


def get_program_from_input(ins: str):
    return list(map(int, ins.split(",")))


# Part 1 ----
my_program = get_program_from_input("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
aa = IntegerComputer(my_program, [])
aa.run()

my_program = get_program_from_input("1102,34915192,34915192,7,4,7,99,0")
aa = IntegerComputer(my_program, [])
aa.run()

my_program = get_program_from_input("104,1125899906842624,99")
aa = IntegerComputer(my_program, [])
aa.run()

infile = "../data/data9.txt"
my_program = get_program(infile)
aa = IntegerComputer(my_program, [1])
aa.run()


# Part 2 ----
def run_through_amplifier_loop(program, amplifier, input_id=0):
    programs = [IntegerComputer(program, [x], feedback_mode=True) for x in amplifier]
    programs[0].add_input(input_id)
    while not programs[-1].is_done:
        for pc in range(len(amplifier)):
            input_id = programs[pc].run()
            programs[(pc+1) % 5].add_input(input_id)
    return input_id


def thrust_maximizer_with_amplifier_loop(program, amplifier, input_id=0):
    n = len(amplifier)
    best_thrust = run_through_amplifier_loop(program, amplifier, input_id)
    for c in itertools.permutations(amplifier, n):
        thrust = run_through_amplifier_loop(program, c, input_id)
        best_thrust = max(best_thrust, thrust)
    return best_thrust


my_program = get_program_from_input("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
print(run_through_amplifier_loop(my_program, [9, 8, 7, 6, 5]))  # 139629729

my_program = get_program_from_input("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")
print(run_through_amplifier_loop(my_program, [9, 7, 8, 5, 6]))  # 18216

infile ='../data/data7.txt'
my_program = get_program(infile)
print(thrust_maximizer_with_amplifier_loop(my_program, [9, 7, 8, 5, 6], 0))
