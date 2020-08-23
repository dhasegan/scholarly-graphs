import os
import csv
import re
import fire
import json

from bs4 import BeautifulSoup

def parse(filename, out_filename):
    data = None
    with open(filename) as f:
        data = f.read()
    soup = BeautifulSoup(data)

    trs = soup.findAll('tr')
    table = []
    for tr in trs:
        tds = tr.findAll('td')
        arr = []
        for td in tds:
            arr.append(td.text.replace('\n', ''))
        table.append(arr)

    with open(out_filename, 'w') as out:
        writer = csv.writer(out)
        for row in table:
            writer.writerow(row)

def join(input_dir, out_filename):
    files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

    items = []

    for filename in files:
        with open(filename) as f:
            for row in csv.DictReader(f):
                if 'name' in row and row['name']:
                    items.append(row['name'])

    items = sorted(list(set(items)))

    with open(out_filename, 'w') as out:
        out.write('name\n')
        for item in items:
            out.write(item + '\n')

def combine(filenames, out_filename):
    if type(filenames) == str:
        filenames = filenames.split(',')

    items = {}
    all_items = []

    for filename in filenames:
        items[filename] = []
        with open(filename) as f:
            for row in csv.DictReader(f):
                items[filename].append(row['name'])
                all_items.append(row['name'])

    all_items = sorted(list(set(all_items)))

    with open(out_filename, 'w') as out:
        out.write('name\n')
        for item in all_items:
            select = True
            for filename in filenames:
                if item not in items[filename]:
                    select = False
                    break
            if select:
                out.write(item + '\n')

if __name__ == '__main__':
    fire.Fire({
        'parse': parse,
        'join': join,
        'combine': combine
    })