from collections import deque
from functools import lru_cache

from util import get_data, submit, timing

DAY = 22


@timing
def part1(p1_deck, p2_deck):
    p1_deck = deque(p1_deck)
    p2_deck = deque(p2_deck)
    while len(p1_deck) > 0 and len(p2_deck) > 0:
        p1_card, p2_card = p1_deck.popleft(), p2_deck.popleft()
        if p1_card > p2_card:
            p1_deck.extend([p1_card, p2_card])
        else:
            p2_deck.extend([p2_card, p1_card])
    return sum((i + 1) * x for i, x in enumerate(reversed(p1_deck + p2_deck)))


#@lru_cache(maxsize=10**8)
@timing
def part2(p1_deck, p2_deck):
    return part2_rec(p1_deck, p2_deck, is_root=True)


#@lru_cache(maxsize=10**7)
def part2_rec(p1_deck, p2_deck, is_root=False):
    if not is_root:
        # the player with the largest number will eventually win
        #   or we will "loop" so if one has the highest card they win
        if max(p1_deck) > max(p2_deck):
            return True
    seen = set()
    while len(p1_deck) > 0 and len(p2_deck) > 0:
        if (p1_deck, p2_deck) in seen:
            #print("cycular")
            return True
        seen.add((p1_deck, p2_deck))
        #print(seen)
        p1_card, p2_card = p1_deck[0], p2_deck[0]
        p1_deck = p1_deck[1:]
        p2_deck = p2_deck[1:]
        if p1_card <= len(p1_deck) and p2_card <= len(p2_deck):
            p1_won_round = part2_rec(p1_deck[:p1_card], p2_deck[:p2_card])
        else:
            p1_won_round = p1_card > p2_card
        if p1_won_round:
            p1_deck = p1_deck + (p1_card, p2_card)
        else:
            p2_deck = p2_deck + (p2_card, p1_card)
    if is_root:
        return sum(
            (i + 1) * x for i, x in enumerate(reversed(p1_deck + p2_deck)))
    else:
        return len(p1_deck) > 0


if __name__ == "__main__":
    data = get_data(DAY)
    split = data.index([])
    p1_deck = tuple(x[0] for x in data[1:split])
    p2_deck = tuple(x[0] for x in data[split + 2:])

    res = part1(p1_deck, p2_deck)
    print(res)
    #submit(DAY, 1, res)

    res = part2(p1_deck, p2_deck)
    print(res)
    #submit(DAY, 2, res)
    # 30964 is too low