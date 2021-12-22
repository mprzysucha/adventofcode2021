scores = {1: 0, 2: 0}
# position = {1: 4, 2: 8}
position = {1: 2, 2: 7}
who_plays = 1

def calculate_new_position(turn, current_position):
     step = 9 * turn + 6
     current_position = (current_position + step - 1) % 10 + 1
     return current_position

turn = 0
while scores.get(1) < 1000 and scores.get(2) < 1000:
    current_score = scores.get(who_plays)
    new_position = calculate_new_position(turn, position.get(who_plays))
    position.update({who_plays : new_position})
    scores.update({who_plays : (current_score + new_position)})
    who_plays = who_plays % 2 + 1
    turn += 1

print(min(scores.get(1), scores.get(2)) * turn * 3)