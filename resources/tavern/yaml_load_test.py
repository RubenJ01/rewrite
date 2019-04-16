"""Test-load the YAML files so that syntax errors are caught."""

import yaml
from pathlib import Path

FAQ_FILE = Path('resources') / 'tavern' / 'faq.yaml'  # Tavern FAQ
RULES_FILE = Path('resources') / 'tavern' / 'rules.yaml'  # Tavern rules
RP_RULES_FILE = Path('resources') / 'tavern' / 'rp_rules.yaml'  # Tavern roleplaying rules


def test_faq():
    with open(FAQ_FILE, encoding='utf-8') as faq_file:
        yaml.safe_load(faq_file)


def test_rules():
    with open(RULES_FILE, encoding='utf-8') as rules_file:
        yaml.safe_load(rules_file)


def test_rp_rules():
    with open(RP_RULES_FILE, encoding='utf-8') as rp_rules_file:
        yaml.safe_load(rp_rules_file)
