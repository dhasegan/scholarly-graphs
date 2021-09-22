import os
import json
from deepdiff import DeepDiff

from neuroa20.libs.user_input import _get_in

def read_dirs(dirs):
    if type(dirs) == str:
        dirs = dirs.split(',')

    files = [os.path.join(input_dir, file) for input_dir in dirs for file in os.listdir(input_dir)]

    rows = []
    for filename in files:
        with open(filename) as f:
            row = json.load(f)
            rows.append(row)

    return rows

def save_scholar(scholar, scholar_dir, alternate_name=None):
    filename = scholar['name'].replace('/', '_') + '.json'
    filepath = os.path.join(scholar_dir, filename)

    if os.path.isfile(filepath):
        current_scholar = None
        with open(filepath) as f:
            current_scholar = json.load(f)
        ddiff = DeepDiff(current_scholar, json.loads(json.dumps(scholar)))
        if ddiff != {}:
            if len(ddiff) == 1 and len(ddiff['dictionary_item_removed']) == 1 and \
                    ddiff['dictionary_item_removed'][0] == "root['alternate_names']":
                scholar = current_scholar
            else:
                print("There are differences that will be rewritten when saving.")
                print(ddiff)
                v = _get_in('Keep original (o)? Write new (n) or Exit (e)? o/n/x: ', ['o', 'n', 'x'])
                if v == 'o':
                    scholar = current_scholar
                if v == 'x':
                    exit()

    if alternate_name and alternate_name != scholar['name']:
        if 'alternate_names' not in scholar:
            scholar['alternate_names'] = []
        scholar['alternate_names'].append(alternate_name)

    with open(filepath, 'w') as out:
        out.write(json.dumps(scholar, indent=4) + '\n')
    

def get_prof(scholars, prof_name):
    for s in scholars:
        names = [s['name']] + (s['alternate_names'] if 'alternate_names' in s else [])
        if prof_name in names:
            return s
    return None