"""Functions to load the npc generator"""

import random


def generate_appearance():
    with open('resources/npcgen/appearance.txt', 'r', encoding='utf-8') as f:
        strings = f.readlines()
    generated_appearance = random.choice(strings)
    return generated_appearance


def generate_history():
    with open('resources/npcgen/history.txt', 'r', encoding='utf-8') as f:
        strings = f.readlines()
    generated_history = random.choice(strings)
    return generated_history


def generate_talent():
    with open('resources/npcgen/talent.txt', 'r', encoding='utf-8') as f:
        strings = f.readlines()
    generated_talent = random.choice(strings)
    return generated_talent


def generate_mannerism():
    with open('resources/npcgen/mannerism.txt', 'r', encoding='utf-8') as f:
        strings = f.readlines()
    generated_mannerism = random.choice(strings)
    return generated_mannerism


def generate_interaction():
    with open('resources/npcgen/interaction.txt', 'r', encoding='utf-8') as f:
        strings = f.readlines()
    generated_interaction = random.choice(strings)
    return generated_interaction


def generate_ideal():
    with open('resources/ideals.txt', 'r', encoding='utf-8') as f:
        strings = f.readlines()
    generated_ideal = random.choice(strings)
    return generated_ideal


def generate_bond():
    with open('resources/bonds.txt', 'r', encoding='utf-8') as f:
        strings = f.readlines()
    generated_bond = random.choice(strings)
    return generated_bond


def generate_flaw():
    with open('resources/flaws.txt', 'r', encoding='utf-8') as f:
        strings = f.readlines()
    generated_flaw = random.choice(strings)
    return generated_flaw


def final_output():
    appearance = generate_appearance()
    bond = generate_bond()
    flaw = generate_flaw()
    history = generate_history()
    ideal = generate_ideal()
    interaction = generate_interaction()
    mannerism = generate_mannerism()
    talent = generate_talent()
    desc = f"**History:** {history}  **Appearance:** {appearance}  **Talent:** {talent}  **Mannerism:** " \
           f"{mannerism}  **Interaction with others:** {interaction}  **Ideal:** {ideal}  **Bond:** {bond} " \
           f"**Flaw or secret:** {flaw} "
    return desc
