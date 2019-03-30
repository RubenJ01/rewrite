"""Tests for srd_json.py"""

from srd_json import collapse, list_to_paragraphs, get_spell_info, srd

def test_spell_search():
    for raw_spell in srd.raw['spells']:
        name = raw_spell['name'].lower()
        results = srd.search_spell(name)
        result_names = [result.name.lower() for result in results]
        if name not in result_names:
            print(name, result_names)
        assert name in result_names
