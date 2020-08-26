import csv
import time
import json
import random
import os
import fire

from neuroa20.libs.google_scholar import read_dirs, get_prof, save_scholar
from neuroa20.libs.user_input import _get_in

def find(profs_list_filename, google_scholar_dir):
    scholars = read_dirs(google_scholar_dir)

    profs = []
    with open(profs_list_filename) as f:
        for row in csv.DictReader(f):
            profs.append(row['name'])

    missing_names = list(set([p for p in profs if get_prof(scholars, p) == None]))
    print("Missing {} names".format(len(missing_names)))

    for prof_name in missing_names:
        print("===== Handling {} =====".format(prof_name))
        first_name = prof_name.split(' ')[0]
        last_name = prof_name.split(' ')[-1]
        found = None
        for scholar in scholars:
            if last_name in scholar['name']:
                c = _get_in('Is `{}` the correct name of `{}`? y/n/b: '.format(scholar['name'], prof_name), ['y', 'n', 'b'])
                if c == 'y':
                    found = scholar
                    break
                elif c == 'n':
                    continue
                elif c == 'b':
                    break
        if found:
            if 'alternate_names' not in found:
                found['alternate_names'] = []
            found['alternate_names'].append(prof_name)
            save_scholar(found, google_scholar_dir)


if __name__ == '__main__':
    fire.Fire({
        'find': find
    })