from time import time

class GameState:

    __p1_pos = 0
    __p2_pos = 0
    __p1_score = 0
    __p2_score = 0
    __rolls = 0
    __move = 0

    def __init__(self, p1_pos, p2_pos):
        self.__p1_pos = p1_pos
        self.__p2_pos = p2_pos

    def p1_pos(self):
        return self.__p1_pos

    def p2_pos(self):
        return self.__p2_pos

    def p1_move(self, step):
        self.__p1_pos = ((self.__p1_pos + step - 1) % 10) + 1
        self.__p1_score += self.__p1_pos

    def p2_move(self, step):
        self.__p2_pos = ((self.__p2_pos + step - 1) % 10) + 1
        self.__p2_score += self.__p2_pos

    def p1_score(self):
        return self.__p1_score

    def p2_score(self):
        return self.__p2_score

    def roll(self, num):
        self.__move += num
        self.__rolls += 1
        if self.__rolls == 3:
            self.p1_move(self.__move)
            self.__move = 0
        if self.__rolls == 6:
            self.p2_move(self.__move)
            self.__move = 0
            self.__rolls = 0

    def clone(self):
        new_gs = GameState(self.p1_pos(), self.p2_pos())
        new_gs.__p1_score = self.__p1_score
        new_gs.__p2_score = self.__p2_score
        new_gs.__rolls = self.__rolls
        new_gs.__move = self.__move
        return new_gs

    def __str__(self):
        return ''.join(["GameState[",
            ','.join([
                ':'.join(["p1_pos", str(self.__p1_pos)]),
                ':'.join(["p2_pos", str(self.__p2_pos)]),
                ':'.join(["p1_score", str(self.__p1_score)]),
                ':'.join(["p2_score", str(self.__p2_score)]),
                ':'.join(["rolls", str(self.__rolls)]),
                ':'.join(["move", str(self.__move)])]
            ), "]"])

    def __hash__(self):
        return hash((self.__p1_pos, self.__p2_pos, self.__p1_score, self.__p2_score, self.__rolls, self.__move))

    def __eq__(self, other):
        return self.__p1_pos == other.__p1_pos and self.__p2_pos == other.__p2_pos and \
               self.__p1_score == other.__p1_score and self.__p2_score == other.__p2_score and \
               self.__rolls == other.__rolls and self.__move == other.__move

cache = {}
cache_hit = 0
cache_miss = 0
def roll(gs:GameState, num, p1_wins, p2_wins, level = 1):
    global cache_hit, cache_miss

    gs.roll(num)
    if gs.p1_score() >= 21:
        return (p1_wins + 1, p2_wins)
    if gs.p2_score() >= 21:
        return (p1_wins, p2_wins + 1)

    if gs in cache:
        cache_hit += 1
        return cache.get(gs)
    cache_miss += 1

    (p1_wins_1, p2_wins_1) = roll(gs.clone(), 1, p1_wins, p2_wins, level + 1)
    (p1_wins_2, p2_wins_2) = roll(gs.clone(), 2, p1_wins, p2_wins, level + 1)
    (p1_wins_3, p2_wins_3) = roll(gs.clone(), 3, p1_wins, p2_wins, level + 1)
    res = (p1_wins_1 + p1_wins_2 + p1_wins_3, p2_wins_1 + p2_wins_2 + p2_wins_3)
    cache.update({gs : res})

    return res

game_states = [
    GameState(4, 8),
    GameState(2, 7)
]

for gs in game_states:
    cache.clear() # cache could be reused
    start = time()
    (p1_wins_1, p2_wins_1) = roll(gs.clone(), 1, 0, 0)
    (p1_wins_2, p2_wins_2) = roll(gs.clone(), 2, 0, 0)
    (p1_wins_3, p2_wins_3) = roll(gs.clone(), 3, 0, 0)

    print(p1_wins_1 + p1_wins_2 + p1_wins_3)
    print(p2_wins_1 + p2_wins_2 + p2_wins_3)

    stop = time()

    print("time:", (stop - start))
    print("cache hit:", cache_hit)
    print("cache miss:", cache_miss)
