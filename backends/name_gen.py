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
        for onset in range(0,table['syllable_structures'].keys()):
            output += r.choices(list(table['onset'].keys()),
                                weights=table['onset'].values())[0]
        
        for vowel in range(0,table['vowels'].keys()):
            output += r.choices(list(table['nucleus'].keys()),
                                weights=table['nucleus'].values())[0]
            output += r.choices(list(table['length'].keys()),
                                weights=table['length'].values())[0]
                
                for tone in range(0,tabel['vowels'].keys()):
                    output += r.choices(list(tabel['tones'].keys()),
                                        weights=table[tones].values())[0]
            
            
        
        for coda in range(0,table['syllable_structures'].values()):
            output += r.choices(list(table['coda'].keys()),
                                weights=table['coda'].values())[0]
        # special postfix for short human names
        if race == "human" and syllables =< 2:
            output += "i"
            
        output = "This is written with IPA symbols", output+ " ,search IPA(International Phonetic Alphabet) from more information"
        return output
