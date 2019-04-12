"""Pytest tests for srd_json.py"""

from srd_json import collapse, list_to_paragraphs, get_spell_info, get_equipment_info, srd


def test_collapse():
    test = {1: ['one', 'two'], 2: 'three'}
    output = collapse(test)
    assert type(output) == str
    assert all(x in output for x in ['one', 'two', 'three'])


def test_list_to_paragraphs():
    input = ['One.', 'Two.']
    output = list_to_paragraphs(input)
    assert output == 'One.\n\u2001Two.'


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
    spells = srd.search('spells', 'name', 'magic missile')
    info = get_spell_info(spells[0])
    assert info.name == 'Magic Missile'
    assert info.casting_range == '120 feet'
    assert info.duration == 'Instantaneous'
    assert info.casting_time == '1 action'

    spells = srd.search('spells', 'name', 'identify')
    info = get_spell_info(spells[0])
    assert info.subhead == '1st-level divination (ritual)'

