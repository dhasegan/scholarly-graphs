import csv
import time
import json
import random
import os
import fire

from scholarly import scholarly
from fp.fp import FreeProxy

def _sleep():
    wait_time = random.randint(1, 10)
    print('waiting...', wait_time)
    time.sleep(wait_time)

def _get_in(text, opts):
    while True:
        val = input(text)
        if val in opts:
            break
    return val

def serialize_coauthor(coauthor):
    return {
        'affiliation': coauthor.affiliation,
        'id': coauthor.id,
        'name': coauthor.name,
    }

def serialize_pub(pub, idx):
    try:
        if False: #idx == 0:
            _sleep()
            print('downloading pub {}'.format(idx))
            pub.fill()
    except Exception as err:
        pass
    return {
        'bib': pub.bib,
        'id_citations': pub.id_citations,
        'source': pub.source,
    }

def serialize_author(author):
    return {
        'affiliation': author.affiliation,
        'cites_per_year': author.cites_per_year,
        'citedby': author.citedby,
        'citedby5y': author.citedby5y,
        'coauthors': [serialize_coauthor(c) for c in author.coauthors],
        'email': author.email,
        'hindex': author.hindex,
        'hindex5y': author.hindex5y,
        'i10index': author.i10index,
        'i10index5y': author.i10index5y,
        'id': author.id,
        'interests': author.interests,
        'name': author.name,
        'publications': [serialize_pub(p, i) for i, p in enumerate(author.publications)],
        'url_picture': author.url_picture,
    }


def process_row(row, patterns=None):
    try:
        print('Processing Row', row['name'])
        val = _get_in('scan, next, or break s/n/b: ', ['s', 'b', 'n'])
        if val in ['b', 'n']:
            return val

        for name in row['name'].split(' & '):
            if name != row['name']:
                print('Processing', name)
            found_detail = None
            _sleep()
            for detail in scholarly.search_author(name):
                print(detail)
                if patterns:
                    for pattern in patterns:
                        for field in [detail.email, detail.affiliation]:
                            if field and pattern in field.lower():
                                found_detail = detail
                                break
                    if found_detail:
                        break
                val = _get_in('select, continue, next, or break s/c/n/b: ', ['s', 'c', 'n', 'b'])
                if val == 's':
                    found_detail = detail
                    break
                elif val == 'c':
                    continue
                elif val in ['b', 'n']:
                    return val

            if found_detail:
                _sleep()
                print('downloading...')
                details = found_detail.fill()
                row['details'] = serialize_author(details)
                print('done!')
                return 'd'

    except Exception as err:
        print(err)
        val = _get_in('next, or break, or retry n/b/r: ', ['n', 'b', 'r'])
        if val in ['n', 'b']:
            return val
        elif val == 'r':
            process_row(row, patterns)

    return 'n'

def run(input_path, output_dir, patterns=None, start_at=0, run_proxy=False):
    if run_proxy:
        proxy = FreeProxy(rand=True, timeout=1, country_id=['US', 'CA']).get()  
        scholarly.use_proxy(http=proxy, https=proxy)

    if type(patterns) == str:
        patterns = patterns.split(',')

    rows = []
    with open(input_path) as f:
        for row in csv.DictReader(f):
            rows.append(row)

    for row in rows[start_at:]:
        filename = os.path.join(output_dir, row['name'] + '.json')
        if os.path.isfile(filename):
            continue

        val = process_row(row, patterns)
        if val == 'n':
            continue
        elif val == 'b':
            break

        with open(filename, 'w') as out:
            out.write(json.dumps(row['details'], indent=4) + '\n')


if __name__ == '__main__':
    fire.Fire({
        'run': run
    })