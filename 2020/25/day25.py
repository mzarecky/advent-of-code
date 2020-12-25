
def transform(subject_number, num_loops):
    initial_value = 1
    for j in range(num_loops):
        initial_value = (initial_value * subject_number) % 20201227
    return initial_value


def find_loop_size(subject_number, card_public_key, door_public_key):
    card_found = None
    door_found = None
    current_loop = 0
    initial_value = 1
    while card_found is None or door_found is None:
        current_loop += 1
        initial_value = (initial_value * subject_number) % 20201227
        if initial_value == card_public_key:
            card_found = current_loop
        if initial_value == door_public_key:
            door_found = current_loop
    return card_found, door_found


# Part 1
card_public_key = 14788856
door_public_key = 19316454
card_loop_size, door_loop_size = find_loop_size(7, card_public_key, door_public_key)
print(transform(card_public_key, door_loop_size))
print(transform(door_public_key, card_loop_size))
