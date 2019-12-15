
import collections
import os

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


class Droid:
    def __init__(self):
        self.pos = (0, 0)
        self.last_input = ''
        self.inputs = {"w": 1, "a": 3, "s": 2, "d": 4}
        self.field = collections.defaultdict(int)
        self.chr_field = {0: " ", 1: "#", 2: "o", 3: "."}
        self.oxygen_locations = set()
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def _get_char(self, pos):
        if pos == self.pos:
            return "D"
        elif pos == (0, 0):
            return "x"
        else:
            return self.chr_field[self.field[pos]]

    def _move(self):
        x, y = self.pos
        if self.last_input == "w":
            y += 1
            self.max_y = max(self.max_y, y)
        elif self.last_input == "a":
            x -= 1
            self.min_x = min(self.min_x, x)
        elif self.last_input == "s":
            y -= 1
            self.min_y = min(self.min_y, y)
        elif self.last_input == "d":
            x += 1
            self.max_x = max(self.max_x, x)
        self.pos = (x, y)
        self.field[(x, y)] = 3

    def _wall(self):
        x, y = self.pos
        if self.last_input == "w":
            y += 1
            self.max_y = max(self.max_y, y)
        elif self.last_input == "a":
            x -= 1
            self.min_x = min(self.min_x, x)
        elif self.last_input == "s":
            y -= 1
            self.min_y = min(self.min_y, y)
        elif self.last_input == "d":
            x += 1
            self.max_x = max(self.max_x, x)
        self.field[(x, y)] = 1

    def _oxygen(self):
        self._move()
        self.oxygen_locations.add(self.pos)
        self.field[self.pos] = 2

    def get_input(self):
        while True:
            print("Move Droid (w/a/s/d):")
            k = getch().decode('ascii')
            print(f"[{k}]")
            if k in self.inputs:
                self.last_input = k
                return self.inputs[k]
            elif k == "q":
                break
        raise SystemExit

    def get_input_old(self):
        while True:
            k = input("Move Droid (w/a/s/d): ")
            k = [x for x in k if x in self.inputs]
            if 'q' in k:
                break
            if len(k) > 0:
                self.last_input = k[0]
                return self.inputs[k[0]]
        raise KeyboardInterrupt

    def interpret_output(self, value):
        if value == 0:
            self._wall()
        elif value == 1:
            self._move()
        elif value == 2:
            self._oxygen()
        else:
            print(f"Unknown output code {value}")
            raise ValueError
        # self.draw()

    def draw(self):
        if os.name == "nt":
            os.system('cls')
        else:
            os.system("clear")
        x_shift, y_shift = self.min_x, self.min_y
        x_n, y_n = self.max_x - self.min_x + 1, self.max_y - self.min_y + 1
        print("+", "-" * x_n, "+")
        for y in reversed(range(y_n)):
            print("| ", end="")
            for x in range(x_n):
                print(self._get_char((x + x_shift, y + y_shift)), end="")
            print(" |")
        print("+", "-" * x_n, "+")


class IntegerComputer:
    def __init__(self, program, input_queue: Droid, verbose=False):
        self.program = collections.defaultdict(int, {x: program[x] for x in range(len(program))})
        self.current_pos = 0
        self.relative_pos = 0
        self.op_code = 0
        self.op_mode_1 = 0
        self.op_mode_2 = 0
        self.op_mode_3 = 0
        self.is_done = False
        self.verbose = verbose
        self.output_mode = 0
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

    def _update_output_mode(self):
        self.output_mode = (self.output_mode + 1) % 3

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
        """
        This instruction should access the robot's current state
        """
        dest = self._get_input_position(self.current_pos + 1, self.op_mode_1)
        self.input_queue.draw()
        self.program[dest] = self.input_queue.get_input()
        self.current_pos += 2

    def __out(self):
        """
        Program outputs two values, first one goes to painter, second goes to movement
        """
        self.output_code = self._get_parameter(self.current_pos + 1, self.op_mode_1)
        if self.verbose:
            print(f"output code = {self.output_code}")
        self.current_pos += 2

        self.input_queue.interpret_output(self.output_code)
        self._update_output_mode()

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


# Part 1 ----
def solution_1():
    infile = "../data/data15.txt"
    my_program = get_program(infile)
    hpc = Droid()
    aa = IntegerComputer(my_program, hpc, verbose=True)
    aa.run()


# Part 2 ----
def play_game(assist=True):
    infile = "../data/data15.txt"
    my_program = get_program(infile)
    hpc = ArcadeGame(assist=assist)
    ic = IntegerComputer(my_program, hpc)
    add_coins(ic)
    ic.run()
    print(f"-- Final Score: {hpc.score}")
    print(f"-- Final Score: {ic.input_queue.score}")
    return hpc.score


if __name__ == "__main__":
    solution_1()
