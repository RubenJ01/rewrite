"""Random fantasy name generator"""

import random as r
import yaml
from pathlib import Path

# description of namegen data format is in this file:
NAMEFILE = Path('resources') / 'namegen.yaml'

with open(NAMEFILE) as f:
    data = yaml.safe_load(f)


def name_gen(race: str, gender: str) -> str:
    table = data[race.lower()][gender.lower()]
    # choose number of syllables based on provided probability weights
    syllables = r.choices(range(1, len(table['syl']) + 1),
                          weights=table['syl'])[0]
    output = ""
    for syllable in range(syllables):
        output += r.choices(list(table['onset'].keys()),
                            weights=table['onset'].values())[0]
        output += r.choices(list(table['nucleus'].keys()),
                            weights=table['nucleus'].values())[0]
        output += r.choices(list(table['coda'].keys()),
                            weights=table['coda'].values())[0]
        # special postfix for short human names
        if race == "human" and syllables == 1:
            output += "i"
            
        output = "This is written with IPA symbols", output
        return output
