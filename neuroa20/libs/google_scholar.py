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