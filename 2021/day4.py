
import functools
import re

with open("./2021/data/day4.txt") as f:
    called_nums = list(map(lambda x: int(x), f.readline().strip().split(',')))
    data = [d.strip() for d in f.readlines()]
    n = len(data) // 6
    boards = list(map(lambda x: re.split(r' +', ' '.join(data[6*x:6*(x+1)]).strip()), range(n)))


class BingoBoard:
    def __init__(self, board: list):
        self.board_size = 5
        self.board = list(map(lambda x: int(x), board))
        self.marks = [False for _ in self.board]
        self.search_order = (
            [0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24],
            [0, 5, 10, 15, 20], [1, 6, 11, 16, 21], [2, 7, 12, 17, 22], [3, 8, 13, 18, 23], [4, 9, 14, 19, 24]
        )
        #    [0, 6, 12, 18, 24], [4, 8, 12, 16, 20]

    def mark_board(self, value):
        if value in self.board:
            self.marks[self.board.index(value)] = True

    def sum_unmarked(self):
        return sum(map(lambda x: (not x[0]) * x[1], zip(self.marks, self.board)))

    def check_winner(self):
        for so in self.search_order:
            if all(map(lambda x: self.marks[x], so)):
                return True
        return False


# Part 1 / 2
all_boards = [BingoBoard(b) for b in boards]
winner_found = [False for _ in boards]
for ball in called_nums:
    print(f"Called ball {ball}")
    for i, b in enumerate(all_boards):
        if winner_found[i]:
            continue
        b.mark_board(ball)
        is_winner = b.check_winner()
        if is_winner:
            winner_found[i] = True
            print(f"-- Board {i} wins")
            print(f"-- Winning ball: {ball}")
            print(f"-- Unmarked sum: {b.sum_unmarked()}")
            print(f"-- Winning value: {b.sum_unmarked() * ball}")
    if all(winner_found):
        break
