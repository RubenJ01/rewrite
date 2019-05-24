"""Functions used to run the encounter command."""
import csv
import random

MONSTERS_CSV = 'resources/csv/monsters.csv'

with open(MONSTERS_CSV, 'r', newline='') as f:
    monsters = list(csv.reader(f))


def calculate_xp(plevel: int, psize: int, difficulty: int) -> int:
    """Calculates the xp threshold for a given party.

    difficulty is in range 1-4 for easy, medium, difficult, and deadly."""
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
    xp = thresholds[plevel - 1][difficulty - 1]
    xp = (xp * psize)
    return xp


def encounter_gen(environment: str, xp: int):
    """Creates the encounter based on the xp threshold and the list of possible monsters"""
    if environment is not None:
        env_monsters = [m for m in monsters if m[1] == environment]  # filter monsters by requested environment

    else:
        env_monsters = monsters
    xp_monsters = 0
    xp_lower_limit = int(xp / 25)
    encountered_monsters = []
    while xp_monsters <= (xp - (3 * xp_lower_limit)):
        candidates = []
        for monster in env_monsters:
            if xp_lower_limit <= int(monster[4]) <= (xp - xp_monsters):
                candidates.append(monster)
        if not candidates:
            return encountered_monsters
        r = random.randint(0, (len(candidates) - 1))
        encountered_monsters.append(candidates[r])
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
    """Creates the message that will be sent to the user"""
    enc = f'Generated an encounter: \n'
    for m in encounter:
        enc += f"**{str(m[0].capitalize())}**, type: {str(m[2])}, XP value of: {str(m[4])} (MM pg. {m[3]}) \n"
    enc += f"XP threshold is: {xp}xp"
    return enc
