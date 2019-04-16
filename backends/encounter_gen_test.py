"""Pytests for encounter_gen.py"""

import random


def test_calculate_xp():
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
    plevel = 4
    psize = 6
    difficulty = 1
    xp = thresholds[(plevel - 1)][(difficulty - 1)]
    xp = (xp * psize)
    assert xp == 750
    plevel = 18
    psize = 4
    difficulty = 3
    xp = thresholds[(plevel - 1)][(difficulty - 1)]
    xp = (xp * psize)
    assert xp == 25200


def test_encounter_gen():
    encounteredMonsters = []
    possiblemonsters = [['aboleth', 'water', 'aberration', '13', '5900'],
                        ['chuul', 'water', 'aberration', '40', '1100'], ['sea hag', 'water', 'fey', '179', '450']]
    monsterCounter = 0
    xp = 500
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
    assert encounteredMonsters == [['sea hag', 'water', 'fey', '179', '450']]
