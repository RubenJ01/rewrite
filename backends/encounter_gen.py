"""Functions used to run the encounter command."""
import csv
import random


def calculate_xp(plevel, difficulty, psize):
    plevel = int(plevel)
    difficulty = int(difficulty)
    psize = int(psize)
    thresholds = [
        [25, 50, 75, 100],
        [50, 100, 150, 200],
        [75, 150, 225, 400],
        [125, 250, 375, 500],
        [250, 500, 750, 1100],
        [300, 600, 900, 1400],
        [350, 750, 1100, 1700],
        [450, 900, 1400, 2100],
        [550, 1100, 1600, 2400],
        [600, 1200, 1900, 2800],
        [800, 1600, 2400, 3600],
        [1000, 2000, 3000, 4500],
        [1100, 2200, 3400, 5100],
        [1250, 2500, 3800, 5700],
        [1400, 2800, 4300, 6400],
        [1600, 3200, 4800, 7200],
        [2000, 3900, 5900, 8800],
        [2100, 4200, 6300, 9500],
        [2400, 4900, 7300, 10900],
        [2800, 5700, 8500, 12700]
    ]
    xp = thresholds[(plevel - 1)][(difficulty - 1)]
    xp = (xp * psize)
    return xp


def load_monsters():
    monsterFile = open('resources/csv/monsters.csv', 'r', newline='')
    monsterReader = csv.reader(monsterFile)
    monsterData = list(monsterReader)
    return monsterData


def create_monster_list(monsterdata, environment):
    possibleMonsters = []
    for m in monsterdata:
        if str(environment) in m[1]:
            possibleMonsters.append(m)
    return possibleMonsters


def encounter_gen(possiblemonsters, xp):
    encounteredMonsters = []
    monsterCounter = 0
    xpMonsters = 0
    xpLowerLimit = int(xp / 25)
    while xpMonsters < (xp - (3 * xpLowerLimit)):
        possibleMonsters = []
        for m in possiblemonsters:
            if xpLowerLimit < int(m[4]) < (xp - xpMonsters):
                possibleMonsters.append(m)
        if not possibleMonsters:
            return encounteredMonsters
        r = random.randint(0, (len(possibleMonsters) - 1))
        encounteredMonsters.append(possibleMonsters[r])
        monsterCounter = len(encounteredMonsters)
        xpMonsters = 0
        for exp in encounteredMonsters:
            xpMonsters += int(exp[4])
        if monsterCounter == 2:
            xpMonsters = int(xpMonsters * 1.5)
        if 3 <= monsterCounter <= 6:
            xpMonsters = xpMonsters * 2
        if 7 <= monsterCounter <= 10:
            xpMonsters = int(xpMonsters * 2.5)
    return encounteredMonsters


def final_encounter(encounter, xp):
    enc = f'Generated an encounter: \n'
    for m in encounter:
        enc += f"**{str(m[0].capitalize())}**, type: {str(m[2])}, XP value of: {str(m[4])} (MM pg. {m[3]}) \n"
    enc += f"XP threshold is: {xp}xp"
    return enc
