
def parse_input(x):
    temp = x.split(" ")
    return temp[0], int(temp[1])


with open("./2020/8/input.txt") as f:
    data = f.readlines()
    instruction_list = [parse_input(d.strip()) for d in data]
    visited_list = [False for d in data]


class HGC(object):
    def __init__(self, instructions):
        self.accumulator = 0
        self.instructions = instructions
        self.times_visited = [0 for x in instructions]
        self.pos = 0

    def _nop(self, value):
        self.times_visited[self.pos] += 1
        self.pos += 1

    def _acc(self, value):
        self.times_visited[self.pos] += 1
        self.accumulator += value
        self.pos += 1

    def _jmp(self, value):
        self.times_visited[self.pos] += 1
        self.pos += value

    def boot(self):
        while self.times_visited[self.pos] == 0:
            command, value = self.instructions[self.pos]
            if command == "nop":
                self._nop(value)
                yield self.accumulator
            elif command == "jmp":
                self._jmp(value)
                yield self.accumulator
            elif command == "acc":
                self._acc(value)
                yield self.accumulator
            else:
                raise StopIteration

    def run(self):
        while 0 <= self.pos < len(self.times_visited) and self.times_visited[self.pos] == 0:
            command, value = self.instructions[self.pos]
            if command == "nop":
                self._nop(value)
            elif command == "jmp":
                self._jmp(value)
            elif command == "acc":
                self._acc(value)
            else:
                raise ValueError


# Part 1
aa = HGC(instruction_list)
aa.run()
print(f"Accumulator Value: {aa.accumulator}")


# Part 2
# There are only ~70 nop commands.  Just test them all
for pos, e in filter(lambda x: x[1][0] == 'nop', enumerate(instruction_list)):
    print(f"========== {pos} ==========")
    copy_list = instruction_list.copy()
    copy_list[pos] = ('jmp', e[1])
    aa = HGC(copy_list)
    aa.run()
    print(f"-- visited {sum(aa.times_visited)} : {aa.accumulator} : {aa.pos}")
    print()
    if aa.pos >= 611:
        break

# There are only ~70 jmp commands.  Just test them all
for pos, e in filter(lambda x: x[1][0] == 'jmp', enumerate(instruction_list)):
    print(f"========== {pos} ==========")
    copy_list = instruction_list.copy()
    copy_list[pos] = ('nop', e[1])
    aa = HGC(copy_list)
    aa.run()
    print(f"-- visited {sum(aa.times_visited)} : {aa.accumulator} : {aa.pos}")
    print()
    if aa.pos >= 611:
        break

print(f"Accumulator value: {aa.accumulator}")
