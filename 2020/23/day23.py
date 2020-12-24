



class CupGame:
    def __init__(self, input_data):
        self.cups = input_data.copy()
        self.size = len(input_data)
        self.current_cup_index = 0
        self.picked_up = list()
        self.current_move = 0

    def find_next_cup(self, current_cup):
        candidate = current_cup
        for _ in range(5):
            candidate -= 1
            if candidate < 1:
                candidate = self.size
            if candidate not in self.picked_up:
                return candidate
        return candidate

    def move(self, verbose=False):
        self.current_move += 1
        if verbose:
            print(f"-- move {self.current_move} --")
        current_cup = self.cups[self.current_cup_index]
        next_ind = (1 + self.current_cup_index) % self.size
        if verbose:
            print(self.cups)
            print(f"current cup: {current_cup}")
        if self.current_cup_index < self.size - 3:
            a = self.cups.pop(next_ind)
            b = self.cups.pop(next_ind)
            c = self.cups.pop(next_ind)
        elif self.current_cup_index == self.size - 3:
            a = self.cups.pop(next_ind)
            b = self.cups.pop(next_ind)
            c = self.cups.pop(0)
        elif self.current_cup_index == self.size - 2:
            a = self.cups.pop(next_ind)
            b = self.cups.pop(0)
            c = self.cups.pop(0)
        elif self.current_cup_index == self.size - 1:
            a = self.cups.pop(0)
            b = self.cups.pop(0)
            c = self.cups.pop(0)

        self.picked_up = [a, b, c]
        next_cup = self.find_next_cup(current_cup)
        next_cup_index = self.cups.index(next_cup)
        if verbose:
            print(f"picked up: {self.picked_up}")
            print(f"destination: {next_cup}\n")

        self.cups = self.cups[0:next_cup_index+1] + self.picked_up + self.cups[next_cup_index+1:]

        # Make sure indices align now
        new_ind = self.cups.index(current_cup)
        if new_ind > self.current_cup_index:
            j = new_ind - self.current_cup_index
            self.cups = self.cups[j:] + self.cups[0:j]
        if new_ind < self.current_cup_index:
            j = self.current_cup_index - new_ind
            self.cups = self.cups[-j:] + self.cups[0:-j]
        self.current_cup_index = next_ind


class Cup:
    def __init__(self, cup_value):
        self.cup_value = cup_value
        self.next_cup = None

    def __repr__(self):
        if self.next_cup is not None:
            return f"{str(self.cup_value)} -> {str(self.next_cup.cup_value)}"
        else:
            return f"{str(self.cup_value)} -> None"

    def __str__(self):
        if self.next_cup is not None:
            return f"{str(self.cup_value)} -> {str(self.next_cup.cup_value)}"
        else:
            return f"{str(self.cup_value)} -> None"

    def set_next(self, new_cup):
        self.next_cup = new_cup

    def unlink_next(self):
        val = self.next_cup.cup_value
        new_next_cup = self.next_cup.next_cup
        self.next_cup.next_cup = None
        self.next_cup = new_next_cup
        return val

    def link_next(self, new_cup):
        old_cup = self.next_cup
        self.next_cup = new_cup
        new_cup.next_cup = old_cup


def make_cups(cup_value_list):
    n = len(cup_value_list)
    cup_map = list(map(lambda x: Cup(x), range(n+1)))
    # Connect cups
    for c, n in zip(cup_value_list[0:n-1], cup_value_list[1:n]):
        cup_map[c].set_next(cup_map[n])
    cup_map[cup_value_list[-1]].set_next(cup_map[cup_value_list[0]])

    return cup_map


def find_destination_cup(current_cup, max_cup, cup_map):
    c = current_cup - 1
    while cup_map[c].next_cup is None:
        c -= 1
        if c < 1:
            c = max_cup
    return c


def play_cup_game(cup_value_list, num_moves=100):
    cup_map = make_cups(cup_value_list)
    current_cup = cup_value_list[0]
    max_cup = len(cup_value_list)

    for m in range(num_moves):
        # print(f"-- move {m+1} --")
        # print(f"Current Cup: {current_cup}")
        pick1 = cup_map[current_cup].unlink_next()
        pick2 = cup_map[current_cup].unlink_next()
        pick3 = cup_map[current_cup].unlink_next()
        # print(f"Picked up: {pick1}, {pick2}, {pick3}")

        # choose next value
        dest_cup = find_destination_cup(current_cup, max_cup, cup_map)
        # print(f"Destination: {dest_cup}")
        cup_map[dest_cup].link_next(cup_map[pick3])
        cup_map[dest_cup].link_next(cup_map[pick2])
        cup_map[dest_cup].link_next(cup_map[pick1])

        # Update current cup
        current_cup = cup_map[current_cup].next_cup.cup_value

    return cup_map


# Inputs
data = list(map(lambda x: int(x), "394618527"))
test_data = list(map(lambda x: int(x), "389125467"))


# Part 1 -- slice and dice
CG = CupGame(data)
for _ in range(100):
    CG.move()

i = CG.cups.index(1)
temp = CG.cups[i+1:] + CG.cups[0:i]
print(*temp, sep="")


# Part 2 -- linked list with index
# game_result = play_cup_game(test_data, 100)  # Validated test case

data2 = data + list(range(10, 1000001))
game_result = play_cup_game(data2, 10000000)

n1 = game_result[1].next_cup.cup_value
n2 = game_result[n1].next_cup.cup_value
print(f"{n1} * {n2} = {n1*n2}")
