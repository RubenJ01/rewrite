"""Functions used to run the encounter command."""
import csv
import random

MONSTERS_CSV = 'resources/csv/monsters.csv'


def calculate_xp(plevel, difficulty, psize):
    """Calculates the xp threshold for a given party"""
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
    """Loads all the monsters from the monsters.csv file"""
    with open(MONSTERS_CSV, 'r', newline='') as f:
        return list(csv.reader(f))


def create_monster_list(monsterdata, environment, check):
    """Creates a list of possible monsters in a certain evironment"""
    possible_monsters = []
    if check == 0:
        for m in monsterdata:
            if str(environment) in m[1]:
                possible_monsters.append(m)
    if check == 1:
        """Runs the program without the environment option"""
        for m in monsterdata:
            possible_monsters.append(m)
    return possible_monsters


def encounter_gen(possiblemonsters, xp):
    """Creates the encounter based on the xp threshold and the list of possible monsters"""
    encountered_monsters = []
    xp_monsters = 0
    xp_lower_limit = int(xp / 25)
    while xp_monsters < (xp - (3 * xp_lower_limit)):
        possible_monsters = []
        for m in possiblemonsters:
            if xp_lower_limit < int(m[4]) < (xp - xp_monsters):
                possible_monsters.append(m)
        if not possible_monsters:
            return encountered_monsters
        r = random.randint(0, (len(possible_monsters) - 1))
        encountered_monsters.append(possible_monsters[r])
        monster_counter = len(encountered_monsters)
        xp_monsters = 0
        for exp in encountered_monsters:
            xp_monsters += int(exp[4])
        if monster_counter == 2:
            xp_monsters = int(xp_monsters * 1.5)
        if 3 <= monster_counter <= 6:
            xp_monsters = xp_monsters * 2
        if 7 <= monster_counter <= 10:
            xp_monsters = int(xp_monsters * 2.5)
    return encountered_monsters


def final_encounter(encounter, xp):
    """Creates the message that will be send to the user"""
    enc = f'Generated an encounter: \n'
    for m in encounter:
        enc += f"**{str(m[0].capitalize())}**, type: {str(m[2])}, XP value of: {str(m[4])} (MM pg. {m[3]}) \n"
    enc += f"XP threshold is: {xp}xp"
    return enc
