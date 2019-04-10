# Download or update the D&D 5e SRD JSON files from https://github.com/adrpadua/5e-database
# This script may be called from the scripts directory or the root directory of the bot

import os
import sys
import zipfile

from pathlib import Path
import urllib.request

ZIP_URL = 'https://github.com/adrpadua/5e-database/archive/master.zip'

# check if we have a resources directory
bot_root = Path(os.getcwd())
if not (bot_root / 'resources').exists():
    bot_root = bot_root.parent
if not (bot_root / 'resources').exists():
    print("Couldn't locate resources directory.")
    sys.exit(1)

# show the target directory and get confirmation
target = bot_root / 'resources' / 'srd'
filename = target / ZIP_URL.split('/')[-1]
print(f'Will download D&D 5e SRD JSON to {filename}')
if filename.exists():
    print('Target already exists, delete it and run again.')
    sys.exit(1)
ask = ''
while ask.lower() not in ('y', 'n'):
    ask = input("Continue? [y/n] ")

if ask.lower() == 'n':
    sys.exit(0)

# create directory, download and extract, and delete zip
target.mkdir(exist_ok=True)
print('Downloading...')
urllib.request.urlretrieve(ZIP_URL, filename)
print('Downloaded.\nExtracting...')
with zipfile.ZipFile(filename) as zipf:
    for zipinfo in zipf.infolist():
        if not zipinfo.filename.endswith('.json'):
            continue
        out_filename = zipinfo.filename.split('/')[1]
        with open(target/out_filename, 'w+b') as out_file:
            out_file.write(zipf.read(zipinfo.filename))
        print(f'Wrote {out_filename}')
(target / filename).unlink()
print(f'Removed {target / filename}')
