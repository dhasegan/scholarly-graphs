import csv
import time
import json
import random
import os
import fire

from neuroa20.libs.google_scholar import read_dirs

def _add_link(links, a1, a2):
    if a1 not in links:
        links[a1] = []
    if a2 not in links[a1]:
        links[a1].append(a2)
    return links

def _get_person_filter_authors(links, person_filter, person_filter_count):
    authors = []

    if person_filter != None:
        authors.append(person_filter)

        if person_filter_count > 0:
            for coauth in links[person_filter]:
                authors.extend(_get_person_filter_authors(links, coauth, person_filter_count - 1))

            authors = list(set(authors))

    return authors

def create_table(
        google_scholar_dir,
        out_filename,
        email_filter=False,
        person_filter=None,
        person_filter_count=1):
    items = read_dirs(google_scholar_dir)

    emails = {}
    links = {}

    for item in items:
        n1 = item['name']
        emails[n1] = item['email']
        for coauthor in item['coauthors']:
            n2 = coauthor['name']
            links = _add_link(links, n1, n2)
            links = _add_link(links, n2, n1)

    person_filter_authors = _get_person_filter_authors(links, person_filter, person_filter_count)

    table = []
    _get_email = lambda x: emails[x].split('.')[-1] if x in emails else '-'
    for a1, a1_co in links.items():
        for a2 in a1_co:
            if (not email_filter or (_get_email(a1) != '-' and _get_email(a2) != '-')) and \
               (not person_filter_authors or (a1 in person_filter_authors and a2 in person_filter_authors)) and \
               a1 < a2:
                    table.append([a1, _get_email(a1), a2, _get_email(a2)])

    with open(out_filename, 'w') as out:
        writer = csv.writer(out, delimiter='\t')
        writer.writerow(['source', 'sourceTitle', 'target', 'targetTitle'])
        for row in table:
            writer.writerow(row)

if __name__ == '__main__':
    fire.Fire({
        'create_table': create_table
    })