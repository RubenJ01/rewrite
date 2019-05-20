"""Load D&D 5e Systems Reference Document information from JSON files provided by dnd5eapi.com

Import the 'srd' name from this module for access to the SRD."""

import json
import logging
from collections import namedtuple
from functools import lru_cache
from pathlib import Path
from typing import List

log = logging.getLogger('bot.' + __name__)

SRDPATH = Path('resources') / 'srd'
NUM_ABBREVS = ('1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th')  # for spell levels

SpellInfo = namedtuple('SpellInfo',
                       'name subhead casting_time casting_range components duration description higher_levels page')

ConditionInfo = namedtuple('ConditionInfo',
                           'name description')

FeatureInfo = namedtuple('FeatureInfo',
                         'name featureclass level description')

LanguageInfo = namedtuple('LanguageInfo',
                          'name languagetype typicalspeakers')

SchoolInfo = namedtuple('SchoolInfo',
                        'name description')

DamageInfo = namedtuple('DamageInfo',
                        'name description')

TraitInfo = namedtuple('TraitInfo',
                       'name finalraces description')

MonsterInfo = namedtuple('MonsterInfo',
                         'name subhead attributes abilityscores features actions')

EquipmentInfo = namedtuple('EquipmentInfo',
                           'name context')

ClassInfo = namedtuple('ClassInfo',
                       'name hit_die proficiency equipment_text saving_throws')


def collapse(item) -> str:
    """Given a JSON-derived data structure, collapse all found strings into one.

    Use for text search of JSON objects."""
    result = ''
    if isinstance(item, str):
        return item
    elif isinstance(item, list):
        for subitem in item:
            result += '\n\n' + collapse(subitem)
        return result
    elif isinstance(item, dict):
        for subitem in item.values():
            result += '\n\n' + collapse(subitem)
        return result
    else:
        return ''


def list_to_paragraphs(items: list) -> str:
    """Convert a list of strings to a single string of paragraphs,
    with each paragraph after the first indented."""
    text = items[0]
    if len(items) > 1:  # if there is more than one paragraph of description, indent the subsequent ones
        for para in items[1:]:
            text += '\n\u2001' + para  # EM QUAD space for indent
    return text


def get_spell_info(spell: dict) -> SpellInfo:
    """Extract fields from a spell given in the dnd5eapi JSON schema.

    Returns a namedtuple containing string fields as they would be found in
    the Players' Handbook spell entry:
    name, subhead, casting_time, casting_range, components, duration, description, page"""
    name = spell['name']
    if spell['level'] == 0:
        # e.g. 'Evocation cantrip'
        subhead = spell['school']['name'] + ' cantrip'
    else:
        # e.g. '5th level necromancy (ritual)'
        subhead = NUM_ABBREVS[spell['level'] - 1] + '-level '
        subhead += spell['school']['name'].lower()
        if spell['ritual'] == 'yes':
            subhead += ' (ritual)'
    casting_time = spell['casting_time']
    casting_range = spell['range']
    components = ', '.join(spell['components'])
    if 'M' in components:
        components += ' (' + spell['material'] + ')'
    duration = spell['duration']
    description = list_to_paragraphs(spell['desc'])
    if 'higher_level' in spell:  # not all spells have a 'Higher levels:' section
        higher_levels = list_to_paragraphs(spell['higher_level'])
    else:
        higher_levels = None
    page = spell['page'].split()[-1]
    return SpellInfo(name, subhead, casting_time, casting_range, components, duration, description, higher_levels, page)


def get_condition_info(condition: dict) -> ConditionInfo:
    name = condition['name']
    description = condition['desc']
    description = '\n'.join(description)
    return ConditionInfo(name, description)


def get_feature_info(feature: dict) -> FeatureInfo:
    name = feature['name']
    featureclass = feature['class']['name']
    level = feature.get('level')  # may be None
    description = feature['desc']
    description = '\n'.join(description)
    return FeatureInfo(name, featureclass, level, description)


def get_language_info(language: dict) -> LanguageInfo:
    name = language['name']
    languagetype = language['type']
    speakers = language['typical_speakers']
    speakers = ', '.join(speakers)
    return LanguageInfo(name, languagetype, speakers)


def get_school_info(school: dict) -> SchoolInfo:
    name = school['name']
    description = school['desc']
    return SchoolInfo(name, description)


def get_damage_info(damage: dict) -> DamageInfo:
    name = damage['name']
    description = damage['desc']
    description = '\n'.join(description)
    return DamageInfo(name, description)


def get_trait_info(trait: dict) -> TraitInfo:
    name = trait['name']
    races = trait['races']
    finalraces = []
    for values in races:
        finalraces.append(values['name'])
    finalraces = ', '.join(finalraces)
    description = trait['desc']
    description = '\n'.join(description)
    return TraitInfo(name, finalraces, description)


def get_monster_info(monster: dict) -> MonsterInfo:
    # subheader for monster details
    name = monster['name']
    size = monster['size']
    monstertype = monster['type']
    alignment = monster['alignment']
    subhead = f'*{size} {monstertype}, {alignment}*'
    # monster attributes
    armor_class = monster['armor_class']
    hit_points = monster['hit_points']
    hit_dice = monster['hit_dice']
    speed = monster['speed']
    attributes = f'**Armor Class** {armor_class} \n'
    attributes += f'**Hit Points** {hit_points} ({hit_dice}) \n'
    attributes += f'**Speed** {speed} \n'
    # ability scores
    strength = monster['strength']
    dexterity = monster['dexterity']
    constitution = monster['constitution']
    intelligence = monster['intelligence']
    wisdom = monster['wisdom']
    charisma = monster['charisma']
    abilityscores = f'**STR** {strength} **DEX** {dexterity} **CON** {constitution} \n'
    abilityscores += f'**INT** {intelligence} **WIS** {wisdom} **CHA** {charisma}'
    # saving throws
    details = ''
    saving_throws = []
    for attr, text in (('strength_save', 'Strength'),
                       ('dexterity_save', 'Dexterity'),
                       ('constitution_save', 'Constitution'),
                       ('intelligence_save', 'Intelligence'),
                       ('wisdom_save', 'Wisdom'),
                       ('charisma_save', 'Charisma')):
        if attr in monster:
            saving_throws.append(f'{text} +{str(monster[attr])}')
    if len(saving_throws) > 0:
        saving_throws = ', '.join(saving_throws)
        details = f'**Saving Throws** {saving_throws} \n'
    # skills
    skills = []
    for attr, text in (('acrobatics', 'Acrobatics'),
                       ('animal_handling', 'Animal Handling'),
                       ('arcana', 'Arcana'),
                       ('athletics', 'Athletics'),
                       ('deception', 'Deception'),
                       ('history', 'History'),
                       ('insight', 'Insight'),
                       ('intimidation', 'Intimidation'),
                       ('investigation', 'Investigation'),
                       ('medicine', 'Medicine'),
                       ('nature', 'Nature'),
                       ('perception', 'Perception'),
                       ('performance', 'Performance'),
                       ('persuasion', 'Persuasion'),
                       ('religion', 'Religion'),
                       ('sleight_of_hand', 'Sleight of Hand'),
                       ('stealth', 'Stealth'),
                       ('survival', 'Survival')):
        if attr in monster:
            skills.append(f'{text} +{str(monster[attr])}')
    if len(skills) > 0:
        skills = ', '.join(skills)
        details += f'**Skills** {skills} \n'
    # vulnerabilities and stuff
    if len(monster["damage_vulnerabilities"]) > 0:
        damage_vulnerabilities = monster['damage_vulnerabilities']
        details += f'**Damage Vulnerabilities** {damage_vulnerabilities} \n'
    if len(monster["damage_resistances"]) > 0:
        damage_resistances = monster['damage_resistances']
        details += f'**Damage Resistances** {damage_resistances} \n'
    if len(monster["damage_immunities"]) > 0:
        damage_immunities = monster['damage_immunities']
        details += f'**Damage Immunities** {damage_immunities} \n'
    if len(monster["condition_immunities"]) > 0:
        condition_immunities = monster['condition_immunities']
        details += f'**Condition Immunities** {condition_immunities} \n'
    senses = monster['senses']
    details += f'**Senses** {senses} \n'
    languages = monster['languages']
    details += f'**Languages** {languages} \n'
    challenge = monster['challenge_rating']
    details += f'**Challenge** {str(challenge)}'
    attributes += details
    # features
    features = []
    if 'special_abilities' in monster:
        special_abilities = monster['special_abilities']
        for value in special_abilities:
            actionname = f"**{value['name']}**"
            features.append(actionname)
            desc = value['desc']
            features.append(desc)
        features = '\n'.join(features)
    actions = []
    if 'actions' in monster:
        all_actions = monster['actions']
        for value in all_actions:
            specialname = f"**{value['name']}**"
            actions.append(specialname)
            desc = value['desc']
            actions.append(desc)
        actions = '\n'.join(actions)
    if 'legendary_actions' in monster:
        legendary_actions = []
        legendaryactions = monster['legendary_actions']
        for value in legendaryactions:
            actionname = f"**{value['name']}**"
            legendary_actions.append(actionname)
            desc = value['desc']
            legendary_actions.append(desc)
        legendary_actions = '\n'.join(legendary_actions)
        actions += f'\n __Legendary Actions__ \n {legendary_actions}'
    return MonsterInfo(name, subhead, attributes, abilityscores, features, actions)


def get_equipment_info(equipment: dict) -> EquipmentInfo:
    name = equipment['name']
    context = ''
    # forming a proper subheader
    subhead = ''
    if 'category_range' in equipment:
        category_range = equipment['category_range']
        subhead += f'*{category_range}*'
    if 'equipment_category' in equipment:
        equipment_category = equipment['equipment_category']
        subhead += f' *{equipment_category}*'
    if 'gear_category' in equipment:
        gear_category = equipment['gear_category']
        subhead += f' *{gear_category}*'
    if 'vehicle_category' in equipment:
        vehicle_category = equipment['vehicle_category']
        subhead += f' *{vehicle_category}*'
    subhead += '\n'
    context += subhead
    # forming the description
    description = ''
    if 'cost' in equipment:
        cost = f"**Cost** {equipment['cost']['quantity']} {equipment['cost']['unit']} \n"
        description += cost
    if 'damage' in equipment:
        damage = f"**Damage** {equipment['damage']['dice_count']}d{equipment['damage']['dice_value']}"
        damage += f"{equipment['damage']['damage_type']['name']} \n"
        description += damage
    if 'range' in equipment:
        if equipment['range']['normal'] > 0:
            equipmentrange = f"**Range** {equipment['range']['normal']} feet "
        else:
            equipmentrange = f"**Range** {equipment['range']['long']} feet "
    if 'throw_range' in equipment:
        throw_range = f"({equipment['throw_range']['normal']}/{equipment['throw_range']['long']})"
        equipmentrange += throw_range
        description += equipmentrange
    if 'speed' in equipment:
        speed = f"**Speed** {equipment['speed']['quantity']} {equipment['speed']['unit']} \n"
        description += speed
    if 'desc' in equipment:
        desc = f"**Description** \n {''.join(equipment['desc'])} \n"
        description += desc
    if 'armor_class' in equipment:
        armor_class = f"**AC** {equipment['armor_class']['base']}"
        if equipment['armor_class']['dex_bonus']:
            armor_class += f"+ dex modifier"
        armor_class += '\n'
        context += armor_class
    if 'stealth_disadvantage' in equipment:
        if equipment['stealth_disadvantage']:
            disadv = f"This item gives you a disadvantage on stealth checks.\n"
            context += disadv
    context += description
    return EquipmentInfo(name, context)


def get_class_info(classinfo: dict) -> ClassInfo:
    name = classinfo['name']
    hit_die = classinfo['hit_die']
    skillproficiencies = []
    amount = classinfo['proficiency_choices'][0]['choose']
    for value in classinfo['proficiency_choices'][0]['from']:
        skillproficiencies.append(str(value['name'])[7:])
    proficiency = f"You are proficient with the following items, in addition to any proficiencies provided by your " \
                  f"race or background: \n "
    proficiency += f"**Skills:** choose {amount} from {', '.join(skillproficiencies)}. \n"
    equipmentproficiencies = []
    for value in classinfo['proficiencies']:
        equipmentproficiencies.append(value['name'])
    proficiency += f"**Equipment:** {', '.join(equipmentproficiencies)}."
    with open('resources/srd/5e-SRD-StartingEquipment.json') as f:
        data = json.load(f)
    for entry in data:
        if entry['class']['name'] == name:
            start_equip = []
            for equip in entry['starting_equipment']:
                start_equip.append(equip['item']['name'])
            equipment_text = f"-{', '.join(start_equip)} \n"
            first_choice = []
            for equip in entry['choice_1'][0]['from']:
                first_choice.append(equip['item']['name'])
            firstsecond_choice = []
            for equip in entry['choice_1'][1]['from']:
                firstsecond_choice.append(equip['item']['name'])
            amount = entry['choice_1'][0]['choose']
            amount_two = entry['choice_1'][1]['choose']
            equipment_text += f"-(a) Choose {amount} from: {', '.join(first_choice)} or (b) choose {amount_two} " \
                              f"from {', '.join(firstsecond_choice)}. \n"
            second_choice = []
            for equip in entry['choice_2'][0]['from']:
                second_choice.append(equip['item']['name'])
            secondsecond_choice = []
            for equip in entry['choice_2'][1]['from']:
                secondsecond_choice.append(equip['item']['name'])
            amount = entry['choice_2'][0]['choose']
            amount_two = entry['choice_2'][1]['choose']
            equipment_text += f"-(a) Choose {amount} from: {', '.join(second_choice)} or (b) choose {amount_two} " \
                              f"from {', '.join(secondsecond_choice)}. \n"
            if entry['choices_to_make'] > 2:
                if len(entry['choice_3']) > 1:
                    third_choice = []
                    for equip in entry['choice_3'][0]['from']:
                        third_choice.append(equip['item']['name'])
                    thirdthird_choice = []
                    for equip in entry['choice_3'][1]['from']:
                        thirdthird_choice.append(equip['item']['name'])
                    amount = entry['choice_3'][0]['choose']
                    amount_two = entry['choice_3'][1]['choose']
                    equipment_text += f"-(a) Choose {amount} from: {', '.join(third_choice)} or (b) choose " \
                                      f" {amount_two} from {', '.join(thirdthird_choice)}. \n"
                else:
                    third_choice = []
                    for equip in entry['choice_3'][0]['from']:
                        third_choice.append(equip['item']['name'])
                    amount = entry['choice_3'][0]['choose']
                    equipment_text += f"-Choose {amount} from: {', '.join(third_choice)} \n"
                if entry['choices_to_make'] > 3:
                    if len(entry['choice_4']) > 1:
                        fourth_choice = []
                        for equip in entry['choice_4'][0]['from']:
                            fourth_choice.append(equip['item']['name'])
                        fourthfourth_choice = []
                        for equip in entry['choice_4'][1]['from']:
                            fourthfourth_choice.append(equip['item']['name'])
                        amount = entry['choice_4'][0]['choose']
                        amount_two = entry['choice_4'][1]['choose']
                        equipment_text += f"-(a) Choose {amount} from: {', '.join(fourth_choice)} or (b) choose " \
                                          f"{amount_two}from {', '.join(fourthfourth_choice)}. \n"
                    else:
                        fourth_choice = []
                        for equip in entry['choice_4'][0]['from']:
                            fourth_choice.append(equip['item']['name'])
                        amount = entry['choice_4'][0]['choose']
                        equipment_text += f"-Choose {amount} from: {', '.join(fourth_choice)} \n"
                    if entry['choices_to_make'] > 4:
                        if len(entry['choice_5']) > 1:
                            fifth_choice = []
                            for equip in entry['choice_5'][0]['from']:
                                fifth_choice.append(equip['item']['name'])
                                fifthfifth_choice = []
                            for equip in entry['choice_5'][1]['from']:
                                fifthfifth_choice.append(equip['item']['name'])
                            amount = entry['choice_5'][0]['choose']
                            amount_two = entry['choice_5'][1]['choose']
                            equipment_text += f"-(a) Choose {amount} from: {', '.join(fifth_choice)} or (b) choose " \
                                              f"{amount_two}from {', '.join(fifth_choice)}. \n"
                        else:
                            fifth_choice = []
                            for equip in entry['choice_5'][0]['from']:
                                fifth_choice.append(equip['item']['name'])
                            amount = entry['choice_5'][0]['choose']
                            equipment_text += f"-Choose {amount} from: {', '.join(fifth_choice)} \n"
    saving_throws = []
    for throw in classinfo['saving_throws']:
        saving_throws.append(throw['name'])
    saving_throws = ', '.join(saving_throws)
    return ClassInfo(name, hit_die, proficiency, equipment_text, saving_throws)


class __SRD:
    """Contains the imported SRD data and methods to search it."""
    def __init__(self, data_path: Path):
        self.raw = {}  # will contain data from all JSON files
        # map SRD resource type to raw JSON data, e.g. 'spells' to contents of 'resources/srd/5e-SRD-Spells.json'
        for file in data_path.iterdir():
            if file.name.endswith('.json'):
                resource = file.stem.replace('5e-SRD-', '').lower()
                log.debug(f'Loading SRD: {resource} from {file}')
                with open(file, encoding='utf-8') as handle:
                    self.raw[resource] = json.load(handle)

    @lru_cache(maxsize=1024)
    def search(self, resource: str, attr: str, request: str) -> list:
        """Do a text search of one attribute of one SRD resource.

        Returns a list of results (empty if none)

        Example:
            search('spells', 'name', 'Missile')
        will search the 'spells' resource for spells with 'missile' in the 'name' attribute.

        Repeated identical searches will be cached by decorator."""
        request = request.lower()
        # check if the request makes sense
        try:
            target = self.raw[resource]
        except ValueError:
            log.debug(f'Invalid search: resource \'{resource}\' not found.')
            return []
        if attr not in target[0]:
            log.debug(f'Invalid search: \'{resource}\' does not have attribute \'{attr}\'')
            return []
        # do the search
        results = []
        for item in target:
            search_text = collapse(item[attr]).lower()
            if request in search_text:
                results.append(item)
        return results

    def search_condition(self, request: str) -> List[ConditionInfo]:
        results = self.search('conditions', 'name', request)
        return [get_condition_info(result) for result in results]

    def search_spell(self, request: str) -> List[SpellInfo]:
        results = self.search('spells', 'name', request)
        return [get_spell_info(result) for result in results]

    def search_feature(self, request: str) -> List['FeatureInfo']:
        results = self.search('features', 'name', request)
        return [get_feature_info(result) for result in results]

    def search_language(self, request: str) -> List['LanguageInfo']:
        results = self.search('languages', 'name', request)
        return [get_language_info(result) for result in results]

    def search_school(self, request: str) -> List['SchoolInfo']:
        results = self.search('magic-schools', 'name', request)
        return [get_school_info(result) for result in results]

    def search_damage(self, request: str) -> List['DamageInfo']:
        results = self.search('damage-types', 'name', request)
        return [get_damage_info(result) for result in results]

    def search_trait(self, request: str) -> List['TraitInfo']:
        results = self.search('traits', 'name', request)
        return [get_trait_info(result) for result in results]

    def search_monster(self, request: str) -> List['MonsterInfo']:
        results = self.search('monsters', 'name', request)
        return [get_monster_info(result) for result in results]

    def search_equipment(self, request: str) -> List['EquipmentInfo']:
        results = self.search('equipment', 'name', request)
        return [get_equipment_info(result) for result in results]

    def search_class(self, request: str) -> List['ClassInfo']:
        results = self.search('classes', 'name', request)
        return [get_class_info(result) for result in results]


srd = __SRD(SRDPATH)  # for export: for access to the SRD
