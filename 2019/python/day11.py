
import collections


class HullPainterRobot:
    def __init__(self):
        """
        0: Black, Left 90*
        1: White, Right 90*
        """
        self.panel_colors = collections.defaultdict(int)
        self.painted_panels = collections.defaultdict(int)
        self.pos = (0, 0)
        self.dir = (0, 1)
        self.valid_colors = [0, 1]
        self.rotate = {
            0: {(0, 1): (-1, 0),
                (1, 0): (0, 1),
                (0, -1): (1, 0),
                (-1, 0): (0, -1)},
            1: {(0, 1): (1, 0),
                (1, 0): (0, -1),
                (0, -1): (-1, 0),
                (-1, 0): (0, 1)}
        }

    def move(self, input_code):
        """
        The robot turns and then moves forward one panel
        """
        if input_code not in self.rotate:
            print(f"Unknown input value: {input_code}")
            raise ValueError
        self.dir = self.rotate[input_code][self.dir]
        self.pos = (self.pos[0]+self.dir[0], self.pos[1]+self.dir[1])

    def paint(self, input_code):
        if input_code not in self.valid_colors:
            print(f"Unknown input value: {input_code}")
            raise ValueError
        self.panel_colors[self.pos] = input_code
        self.painted_panels[self.pos] += 1

    def get_color(self):
        return self.panel_colors[self.pos]


class IntegerComputer:
    def __init__(self, program, input_queue: HullPainterRobot, verbose=False):
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
        self.output_mode = (self.output_mode + 1) % 2

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
        """
        This instruction should access the robot's current state
        """
        dest = self._get_input_position(self.current_pos + 1, self.op_mode_1)
        self.program[dest] = self.input_queue.get_color()
        self.current_pos += 2

    def __out(self):
        """
        Program outputs two values, first one goes to painter, second goes to movement
        """
        self.output_code = self._get_parameter(self.current_pos + 1, self.op_mode_1)
        if self.verbose:
            print(f"output code = {self.output_code}")
        self.current_pos += 2
        if self.output_mode == 0:
            self.input_queue.paint(self.output_code)
        else:
            self.input_queue.move(self.output_code)
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
infile = "../data/data11.txt"
my_program = get_program(infile)
hpc = HullPainterRobot()
aa = IntegerComputer(my_program, hpc, verbose=True)
aa.run()
print(len(hpc.painted_panels))


# Part 2 ----
infile = "../data/data11.txt"
my_program = get_program(infile)
hpc = HullPainterRobot()
hpc.panel_colors[hpc.pos] = 1  # Set starting tile to white
aa = IntegerComputer(my_program, hpc, verbose=True)
aa.run()

# Copy this to test out writing a draw function
bb = hpc.panel_colors.copy()


def print_hull_painting(pc: collections.defaultdict):
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    for j in pc.keys():
        min_x, min_y, max_x, max_y = min(min_x, j[0]), min(min_y, j[1]), max(max_x, j[0]), max(max_y, j[1])
    x_range, y_range = max_x - min_x + 1, max_y - min_y + 1
    x_shift, y_shift = -1 * min_x, -1 * min_y
    print(f"x: [{min_x}, {max_x}]; y: [{min_y}, {max_y}]")
    print(f"x_range: {x_range}; y_range: {y_range}")
    print(f"x_shift: {x_shift}; y_shift: {y_shift}")
    color_map = {0: " ", 1: "*"}
    data = [[color_map[0] for x in range(x_range)] for y in range(y_range)]

    # Put colors in data
    for j in pc.keys():
        data[y_shift + j[1]][x_shift + j[0]] = color_map[pc[j]]

    print("----- Image -----")
    for j in reversed(range(y_range)):
        print("".join(data[j]))
    print("----- End Image -----")


print_hull_painting(bb)
