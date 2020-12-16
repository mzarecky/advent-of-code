
import collections


class NumberGame:
    def __init__(self):
        self.times_spoken = collections.defaultdict(int)
        self.turn1 = collections.defaultdict(int)
        self.turn2 = collections.defaultdict(int)
        self.current_turn = 0
        self.last_spoken = -1

    def speak(self, number):
        self.current_turn += 1
        self.last_spoken = number
        self.times_spoken[number] += 1
        self.turn1[number], self.turn2[number] = self.current_turn, self.turn1[number]
        # print(f"Turn {self.current_turn}:  {number}")

    def determine_next(self):
        if self.times_spoken[self.last_spoken] == 1:
            return 0
        else:
            return self.turn1[self.last_spoken] - self.turn2[self.last_spoken]


def play_game(starting_numbers, limit):
    aa = NumberGame()
    for j in starting_numbers:
        aa.speak(j)

    while aa.current_turn < limit:
        n = aa.determine_next()
        aa.speak(n)

    return aa.last_spoken


# Part 1
temp = play_game([20, 9, 11, 0, 1, 2], 2020)
print(temp)

# Part 2
temp = play_game([20, 9, 11, 0, 1, 2], 30000000)
print(temp)
