"""Pytest tests for srd_json.py"""

from srd_json import *


def test_collapse():
    test = {1: ['one', 'two'], 2: 'three'}
    output = collapse(test)
    assert type(output) == str
    assert all(x in output for x in ['one', 'two', 'three'])


def test_list_to_paragraphs():
    input = ['One.', 'Two.']
    output = list_to_paragraphs(input)
    assert output == 'One.\n\u2001Two.'


def test_all_info_lookups():
    lookups = (('spells', get_spell_info),
               ('conditions', get_condition_info),
               ('features', get_feature_info),
               ('languages', get_language_info),
               ('magic-schools', get_school_info),
               ('damage-types', get_damage_info),
               ('traits', get_trait_info),
               ('monsters', get_monster_info),
               ('equipment', get_equipment_info),
               ('classes', get_class_info))
    for resource, info_lookup in lookups:
        for item in srd.raw[resource]:
            info_lookup(item)


def test_srd_spell_search():
    for raw_spell in srd.raw['spells']:
        name = raw_spell['name'].lower()
        results = srd.search_spell(name)
        result_names = [result.name.lower() for result in results]
        assert name in result_names
    spells = srd.search('spells', 'name', 'healing word')
    assert len(spells) == 2
    spells = srd.search('spells', 'name', 'conjure')
    assert len(spells) == 6


def test_get_spell_info():
    for spell in srd.raw['spells']:
        info = get_spell_info(spell)
    spells = srd.search('spells', 'name', 'magic missile')
    info = get_spell_info(spells[0])
    assert info.name == 'Magic Missile'
    assert info.casting_range == '120 feet'
    assert info.duration == 'Instantaneous'
    assert info.casting_time == '1 action'

    spells = srd.search('spells', 'name', 'identify')
    info = get_spell_info(spells[0])
    assert info.subhead == '1st-level divination (ritual)'
