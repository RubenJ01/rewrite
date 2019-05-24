"""Pytest tests for srd_json.py"""

import srd_json as m


def test_collapse():
    test = {1: ['one', 'two'], 2: 'three'}
    output = m.collapse(test)
    assert type(output) == str
    assert all(x in output for x in ['one', 'two', 'three'])


def test_list_to_paragraphs():
    input = ['One.', 'Two.']
    output = m.list_to_paragraphs(input)
    assert output == 'One.\n\u2001Two.'


def test_all_info_lookups():
    lookups = (('spells', m.get_spell_info),
               ('conditions', m.get_condition_info),
               ('features', m.get_feature_info),
               ('languages', m.get_language_info),
               ('magic-schools', m.get_school_info),
               ('damage-types', m.get_damage_info),
               ('traits', m.get_trait_info),
               ('monsters', m.get_monster_info),
               ('equipment', m.get_equipment_info),
               ('classes', m.get_class_info))
    for resource, info_lookup in lookups:
        for item in m.srd.raw[resource]:
            info_lookup(item)


def test_srd_spell_search():
    for raw_spell in m.srd.raw['spells']:
        name = raw_spell['name'].lower()
        results = m.srd.search_spell(name)
        result_names = [result.name.lower() for result in results]
        assert name in result_names
    spells = m.srd.search('spells', 'name', 'healing word')
    assert len(spells) == 2
    spells = m.srd.search('spells', 'name', 'conjure')
    assert len(spells) == 6


def test_get_spell_info():
    for spell in m.srd.raw['spells']:
        info = m.get_spell_info(spell)
    spells = m.srd.search('spells', 'name', 'magic missile')
    info = m.get_spell_info(spells[0])
    assert info.name == 'Magic Missile'
    assert info.casting_range == '120 feet'
    assert info.duration == 'Instantaneous'
    assert info.casting_time == '1 action'

    spells = m.srd.search('spells', 'name', 'identify')
    info = m.get_spell_info(spells[0])
    assert info.subhead == '1st-level divination (ritual)'
