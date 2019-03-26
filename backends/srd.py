"""Load D&D 5e Systems Reference Document information from JSON files provided by dnd5eapi.co"""

import json
import logging
from pathlib import Path

log = logging.getLogger('bot.' + __name__)

SRDPATH = Path('resources') / 'srd'

srd = {}  # import this name for access to the SRD

# map SRD resource type to raw JSON data, e.g. 'spells' to contents of 'resources/srd/5e-SRD-Spells.json'
for file in SRDPATH.iterdir():
    if file.name.endswith('.json'):
        resource = file.stem.replace('5e-SRD-', '').lower()
        log.debug(f'Loading SRD: {resource} from {file}')
        with open(file, encoding='utf-8') as handle:
            srd[resource] = json.load(handle)
