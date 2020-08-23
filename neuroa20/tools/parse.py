import os
import csv
import re
import fire
import json

from bs4 import BeautifulSoup


def details_coauthors(input_dir, output_path, min_links=2):
    files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    current_authors = {}
    coauthors = {}
    for file in files:
        filename = os.path.join(input_dir, file)
        with open(filename) as f:
            row = json.load(f)
            current_authors[row['name']] = True
            for coauthor in row['coauthors']:
                name = coauthor['name']
                if name not in coauthors:
                    coauthors[name] = { 'affiliation': coauthor['affiliation'], 'links': [] }
                if coauthor['affiliation'] != coauthors[name]['affiliation']:
                    raise "Different affiliations {} {} ".format(coauthor['affiliation'], coauthors[name]['affiliation'])
                coauthors[name]['links'].append(row['name'])

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