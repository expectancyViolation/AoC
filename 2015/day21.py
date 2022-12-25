import re
from dataclasses import replace
from itertools import combinations

from util import *
import pandas as pd
from io import StringIO

DAY = 21
YEAR = 2015

counts = {
    "Weapons": [1],
    "Armor": [0, 1],
    "Rings": [*range(3)]
}


def parse_shop(shop_file):
    with open(shop_file, "r") as f:
        categories = f.read().split("\n\n")
    res = []
    for category in categories:
        category = re.sub("(\ )+", "\t", category)
        df = pd.read_csv(StringIO(category), sep="\t")
        c = counts[df.columns[0].strip(":")]
        res.append((df, c))
    return res


def gen_poss_equipments(shop, ind=0):
    if ind >= len(shop):
        yield 0, 0, 0
        return
    df, c = shop[ind]
    for i in c:
        for bought in combinations(df.iterrows(), i):
            for dmg, armor, cost in gen_poss_equipments(shop, ind + 1):
                new_cost = cost + sum(item['Cost'] for _, item in bought)
                new_dmg = dmg + sum(item['Damage'] for _, item in bought)
                new_armor = armor + sum(item['Armor'] for _, item in bought)
                yield new_dmg, new_armor, new_cost


@dataclass(frozen=True)
class Entity:
    hp: int
    dmg: int
    armor: int

    def attack(self, entity: "Entity"):
        dmg = self.dmg - entity.armor
        new_hp = max(0, entity.hp - dmg)
        return replace(entity, hp=new_hp)

    def wins_against(self, entity: "Entity"):
        me = self
        while True:
            dmg_occured = False
            entity_new = self.attack(entity)
            dmg_occured |= entity_new.hp != entity.hp
            entity = entity_new
            if entity.hp == 0:
                return True
            me_new = entity.attack(me)
            dmg_occured |= me_new.hp != me.hp
            me = me_new
            if me.hp == 0:
                return False
            if not dmg_occured:
                return False


def solve(data):
    shop = parse_shop(shop_file="21_shop.txt")
    hp_line, dmg_line, armor_line = data
    boss = Entity(hp=hp_line[-1], dmg=dmg_line[-1], armor=armor_line[-1])
    best = inf
    worst = 0
    for dmg, armor, cost in gen_poss_equipments(shop):
        me = Entity(hp=100, dmg=dmg, armor=armor)
        if me.wins_against(boss):
            best = min(cost, best)
        else:
            worst = max(cost, worst)
    return best, worst


if __name__ == "__main__":
    data = get_data(DAY, year=YEAR)
    print(data)
    part1, part2 = solve(data)
    print(part1)
    # submit(DAY, 1, part1, year=YEAR)
    # res = part2(data)
    print(part2)
    submit(DAY, 2, part2, year=YEAR)
