
with open('./2020/22/input.txt') as f:
    data = [d.strip() for d in f.readlines()]
    i = data.index("")
    player_1 = [int(_) for _ in data[1:i]]
    player_2 = [int(_) for _ in data[i+2:]]


def play_game(deck1, deck2):
    d1 = deck1.copy()
    d2 = deck2.copy()

    while d1 and d2:
        c1 = d1.pop(0)
        c2 = d2.pop(0)
        if c1 > c2:
            d1 += [c1, c2]
        else:
            d2 += [c2, c1]

    n = len(d1) + len(d2)
    if d1:
        s = sum(map(lambda x: x[0]*x[1], zip(d1, range(n, 0, -1))))
    else:
        s = sum(map(lambda x: x[0]*x[1], zip(d2, range(n, 0, -1))))
    return s


# Part 1
score = play_game(player_1, player_2)
print(f"Score: {score}")


# Part 2
def play_recursive_game(deck1, deck2, verbose=True):
    def play(deck1, deck2):
        prior_decks_1 = set()
        prior_decks_2 = set()

        def check_prior_state(a, b):
            s1 = str(a)
            s2 = str(b)
            if s1 in prior_decks_1 and s2 in prior_decks_2:
                return True
            else:
                prior_decks_1.add(s1)
                prior_decks_2.add(s2)
                return False

        d1 = deck1.copy()
        d2 = deck2.copy()

        # Draw cards
        while d1 and d2:
            if verbose:
                print(f"Player 1's deck: {d1}")
                print(f"Player 2's deck: {d2}")

            prior_seen = check_prior_state(d1, d2)
            if prior_seen:
                print("!!! This deck combination has been seen before !!!")
                return 1, d1, d2

            c1 = d1.pop(0)
            c2 = d2.pop(0)
            if verbose:
                print(f"Player 1 plays: {c1}")
                print(f"Player 2 plays: {c2}")

            if c1 <= len(d1) and c2 <= len(d2):
                # recurse
                n1 = d1[0:c1].copy()
                n2 = d2[0:c2].copy()
                if verbose:
                    print("... playing a sub-game ...")
                winner, o1, o2 = play(n1, n2)
                if verbose:
                    print(f"... player {winner} wins sub-game")
                if winner == 1:
                    d1 += [c1, c2]
                else:
                    d2 += [c2, c1]
            else:
                if c1 > c2:
                    if verbose:
                        print("    Player 1 wins round")
                    d1 += [c1, c2]
                else:
                    if verbose:
                        print("    Player 2 wins round")
                    d2 += [c2, c1]

        if d1:
            if verbose:
                print("Player 2 wins game")
            return 1, d1, d2
        else:
            if verbose:
                print("Player 2 wins game")
            return 2, d1, d2

    winner, o1, o2 = play(deck1, deck2)
    print(winner)
    print(o1)
    print(o2)
    return winner, o1, o2


# player_1 = [9, 2, 6, 3, 1]
# player_2 = [5, 8, 4, 7, 10]

winner, o1, o2 = play_recursive_game(player_1, player_2)

if winner == 1:
    n = len(o1)
    s = sum(map(lambda x: x[0]*x[1], zip(o1, range(n, 0, -1))))
else:
    n = len(o2)
    s = sum(map(lambda x: x[0] * x[1], zip(o2, range(n, 0, -1))))

print(f"Winning Score: {s}")

