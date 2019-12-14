
import collections
import os


class ArcadeGame:
    def __init__(self, assist=False):
        """
        0: Empty
        1: Wall, indestructible
        2: Block, broken by ball
        3: Horizontal Paddle, indestructible
        4: Ball, moves diagonally and bounces
        """
        self.screen = collections.defaultdict(int)
        self.pos = (0, 0)
        self.ball = (0, 0)
        self.sc_x1 = 0
        self.sc_y1 = 0
        self.valid_tiles = {0: " ", 1: "X", 2: "q", 3: "M", 4: "@"}
        self.joystick = {
            0: {"state": "_"},
            -1: {"state": "/"},
            1: {"state": "\\"}
        }
        self.joystick_pos = (0, 0)  # Placeholder
        self.score = 0
        self.instructions = {
            0: self._set_x,
            1: self._set_y,
            2: self._set_tile
        }
        self.assist = assist

    def _set_x(self, x):
        self.sc_x1 = max(self.sc_x1, x)
        self.pos = (x, self.pos[1])

    def _set_y(self, y):
        self.sc_y1 = max(self.sc_y1, y)
        self.pos = (self.pos[0], y)

    def _set_tile(self, tile):
        if self.pos == (-1, 0):
            self.score = tile
        else:
            self.screen[self.pos] = tile
            if tile == 3:
                self.joystick_pos = self.pos

    def _find_ball(self):
        pos = [x for x in self.screen.items() if x[1] == 4]
        return pos[0][0]

    def get_input(self):
        px, py = self.joystick_pos
        cmd = input("\nJoy Input (a/s/d): ")
        cmd = cmd[0] if len(cmd) > 0 else ""

        if cmd == "a":
            self.joystick_pos = (px - 1, py)
            return -1
        elif cmd == "s" or cmd == "":
            return 0
        elif cmd == "d":
            self.joystick_pos = (px + 1, py)
            return 1
        else:
            raise ValueError

    def do(self, input_code, value):
        if input_code not in self.instructions:
            print(f"Unknown input value: {input_code}")
            raise ValueError
        self.instructions[input_code](value)

    def draw_screen(self):
        os.system('clear')
        ball_x, ball_y = self._find_ball()
        print(f"\nScore: {self.score}; JXY = {self.joystick_pos[0]},{self.joystick_pos[1]}")
        for y in range(self.sc_y1+1):
            for x in range(self.sc_x1+1):
                if self.assist and abs(x - ball_x) == abs(y - ball_y) and abs(x - ball_x) > 0 and self.screen[(x, y)] == 0:
                    print(".", end="")
                else:
                    print(self.valid_tiles[self.screen[(x, y)]], end="")
            print()


class IntegerComputer:
    def __init__(self, program, input_queue: ArcadeGame, verbose=False):
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
        self.input_queue.draw_screen()
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

        self.input_queue.do(self.output_mode, self.output_code)
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


def add_coins(ic: IntegerComputer, amt=2):
    ic.program[0] = amt


# Part 1 ----
def solution_1():
    infile = "../data/data13.txt"
    my_program = get_program(infile)
    hpc = ArcadeGame()
    aa = IntegerComputer(my_program, hpc, verbose=True)
    aa.run()
    print(len([hpc.screen[x] for x in hpc.screen if hpc.screen[x] == 2]))  # 205
    hpc.draw_screen()


# Part 2 ----
def play_game(assist=True):
    infile = "../data/data13.txt"
    my_program = get_program(infile)
    hpc = ArcadeGame(assist=assist)
    ic = IntegerComputer(my_program, hpc)
    add_coins(ic)
    ic.run()
    print(f"-- Final Score: {hpc.score}")
    print(f"-- Final Score: {ic.input_queue.score}")
    return hpc.score


if __name__ == "__main__":
    # Added assist mode because I suck at breakball
    play_game()
