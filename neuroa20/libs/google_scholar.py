import os
import json

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

def save_scholar(scholar, scholar_dir):
    filename = scholar['name'].replace('/', '_') + '.json'
    with open(os.path.join(scholar_dir, filename), 'w') as out:
        out.write(json.dumps(scholar, indent=4) + '\n')
    

def get_prof(scholars, prof_name):
    for s in scholars:
        names = [s['name']] + (s['alternate_names'] if 'alternate_names' in s else [])
        if prof_name in names:
            return s
    return None