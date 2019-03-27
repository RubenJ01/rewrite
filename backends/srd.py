"""Load D&D 5e Systems Reference Document information from JSON files provided by dnd5eapi.co"""

import json
import logging
from functools import lru_cache
from pathlib import Path
from time import perf_counter_ns

log = logging.getLogger('bot.' + __name__)

SRDPATH = Path('resources') / 'srd'


def collapse(item) -> str:
    """Given a JSON-derived data structure, collapse all found strings into one."""
    result = ''
    if isinstance(item, str):
        return item
    elif isinstance(item, list):
        for subitem in item:
            result += collapse(subitem)
        return result
    elif isinstance(item, dict):
        for subitem in item.values():
            result += collapse(subitem)
        return result
    else:
        return ''


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
    def search(self, resource: str, attr: str, request: str) -> (list, bool):
        """Do a text search of one attribute of one SRD resource.
        Returns a list of results (empty if none) and a flag indicating whether or not the search
        was truncated.
        Example:
            search('spells', 'name', 'missile')
        will search the spells resource for a spell with 'missile' in the 'name' attribute.
        Repeated identical searches will be cached by decorator."""
        log.debug(f'Searching \'{resource}\'->\'{attr}\' for \'{request}\'...')
        start_time = perf_counter_ns()
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
        results, truncated = [], False
        for item in target:
            search_text = collapse(item[attr]).lower()
            if request in search_text.lower():
                results.append(item)
                # stop matchy searches before they get too long
                if len(results) > 5:
                    truncated = True
                    break
        end_time = perf_counter_ns()
        elapsed_ms = (end_time - start_time) / 1_000_000
        log.debug(f'Finished search in {elapsed_ms}ms')
        return results, truncated


srd = __SRD(SRDPATH)  # for export: for access to the SRD
