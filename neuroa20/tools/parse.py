import os
import csv
import re
import fire
import json

from bs4 import BeautifulSoup

from neuroa20.libs.google_scholar import read_dirs, get_prof


def details_coauthors(
        input_dir,
        output_path, 
        list_filename_filter=None,
        min_links=2):

    scholars = read_dirs(input_dir)
    if list_filename_filter:
        profs = []
        with open(list_filename_filter) as f:
            for row in csv.DictReader(f):
                prof = get_prof(scholars, row['name'])
                if prof:
                    profs.append(prof)
        scholars = profs

    current_authors = {}
    coauthors = {}
    for scholar in scholars:
        current_authors[scholar['name']] = True
        for coauthor in scholar['coauthors']:
            name = coauthor['name']
            if name not in coauthors:
                coauthors[name] = { 'affiliation': coauthor['affiliation'], 'links': [] }
            if coauthor['affiliation'] != coauthors[name]['affiliation']:
                print("Different affiliations for {}: `{}` `{}` ".format(
                    name,
                    coauthor['affiliation'],
                    coauthors[name]['affiliation']))
            coauthors[name]['links'].append(scholar['name'])

    coauthors = sorted(
        [(k, v) for k,v in coauthors.items() if len(v['links']) >= min_links and k not in current_authors],
        key=lambda x:len(x[1]['links']),
        reverse=True)

    with open(output_path, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(['name', 'affiliation', 'links'])
        for name, details in coauthors:
            writer.writerow([name, details['affiliation'], '\t'.join(details['links'])])

if __name__ == '__main__':
    fire.Fire({
        'coauthors': details_coauthors
    })