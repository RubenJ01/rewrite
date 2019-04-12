"""Load D&D 5e Systems Reference Document information from JSON files provided by dnd5eapi.co

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
                         'name subhead attributes abilityscores details features actions')

EquipmentInfo = namedtuple('EquipmentInfo',
                           'name context')


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
    level = feature['level']
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
    attributes += f'**Speed** {speed} '
    # ability scores
    strength = monster['strength']
    dexterity = monster['dexterity']
    constitution = monster['constitution']
    intelligence = monster['intelligence']
    wisdom = monster['wisdom']
    charisma = monster['charisma']
    abilityscores = f'**STR** {strength} \n **DEX** {dexterity} \n **CON** {constitution} \n'
    abilityscores += f'**INT** {intelligence} \n **WIS** {wisdom} \n **CHA** {charisma}'
    # saving throws
    details = ''
    saving_throws = []
    if 'constitution_save' in monster:
        con_save = f"Constitution +{str(monster['constitution_save'])}"
        saving_throws.append(con_save)
    if 'intelligence_save' in monster:
        int_save = f"Intelligence +{str(monster['intelligence_save'])}"
        saving_throws.append(int_save)
    if 'wisdom_save' in monster:
        wis_save = f"Wisdom +{str(monster['wisdom_save'])}"
        saving_throws.append(wis_save)
    if 'strength_save' in monster:
        str_save = f"Strength +{str(monster['strength_save'])}"
        saving_throws.append(str_save)
    if 'charisma_save' in monster:
        cha_save = f"Charisma +{str(monster['charisma_save'])}"
        saving_throws.append(cha_save)
    if 'dexterity_save' in monster:
        dex_save = f"Dexterity +{str(monster['dexterity_save'])}"
        saving_throws.append(dex_save)
    if len(saving_throws) > 0:
        saving_throws = ', '.join(saving_throws)
        details = f'**Saving Throws** {saving_throws} \n'
    # skills
    skills = []
    if 'acrobatics' in monster:
        acrobatics = f"Acrobatics +{str(monster['acrobatics'])}"
        skills.append(acrobatics)
    if 'animal_handling' in monster:
        animal_handling = f"Animal Handling +{str(monster['animal_handling'])}"
        skills.append(animal_handling)
    if 'acrobatics' in monster:
        acrobatics = f"Acrobatics +{str(monster['acrobatics'])}"
        skills.append(acrobatics)
    if 'arcana' in monster:
        arcana = f"Arcana +{str(monster['arcana'])}"
        skills.append(arcana)
    if 'athletics' in monster:
        athletics = f"Athletics +{str(monster['athletics'])}"
        skills.append(athletics)
    if 'deception' in monster:
        deception = f"Deception +{str(monster['deception'])}"
        skills.append(deception)
    if 'history' in monster:
        history = f"History +{str(monster['history'])}"
        skills.append(history)
    if 'insight' in monster:
        insight = f"Insight +{str(monster['insight'])}"
        skills.append(insight)
    if 'intimidation' in monster:
        intimidation = f"Intimidation +{str(monster['intimidation'])}"
        skills.append(intimidation)
    if 'investigation' in monster:
        investigation = f"Investigation +{str(monster['investigation'])}"
        skills.append(investigation)
    if 'medicine' in monster:
        medicine = f"Medicine +{str(monster['medicine'])}"
        skills.append(medicine)
    if 'nature' in monster:
        nature = f"Nature +{str(monster['nature'])}"
        skills.append(nature)
    if 'perception' in monster:
        perception = f"Perception +{str(monster['perception'])}"
        skills.append(perception)
    if 'performance' in monster:
        performance = f"Performance +{str(monster['performance'])}"
        skills.append(performance)
    if 'persuasion' in monster:
        persuasion = f"Persuasion +{str(monster['persuasion'])}"
        skills.append(persuasion)
    if 'religion' in monster:
        religion = f"Religion +{str(monster['religion'])}"
        skills.append(religion)
    if 'sleight_of_hand' in monster:
        sleight_of_hand = f"Sleight of Hand +{str(monster['sleight_of_hand'])}"
        skills.append(sleight_of_hand)
    if 'stealth' in monster:
        stealth = f"Stealth +{str(monster['stealth'])}"
        skills.append(stealth)
    if 'survival' in monster:
        survival = f"Survival +{str(monster['survival'])}"
        skills.append(survival)
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
    # features
    features = []
    special_abilities = monster['special_abilities']
    for value in special_abilities:
        actionname = f"**{value['name']}**"
        features.append(actionname)
        desc = value['desc']
        features.append(desc)
    features = '\n'.join(features)
    actions = []
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
            name = f"**{value['name']}**"
            legendary_actions.append(name)
            desc = value['desc']
            legendary_actions.append(desc)
            legendary_actions = '\n'.join(legendary_actions)
            actions += f'\n __Legendary Actions__ \n {legendary_actions}'
    return MonsterInfo(name, subhead, attributes, abilityscores, details, features, actions)


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
        damage += f"{ equipment['damage']['damage_type']['name']} \n"
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
        desc = f"**Description** \n {''.join(equipment['desc'])}"
        description += desc
    context += description
    return EquipmentInfo(name, context)


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


srd = __SRD(SRDPATH)  # for export: for access to the SRD
