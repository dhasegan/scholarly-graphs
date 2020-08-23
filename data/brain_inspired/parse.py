import os
import csv
import re
import fire
import json

from bs4 import BeautifulSoup

def brain_inspired(input_dir, output_path):
    files = [f for f in os.listdir(input_dir) if f.endswith('.html')]

    def _extract_name(title):
        return re.search('BI [0-9]+ (.*): .+', title).group(1)

    items = []

    for filename in files:
        data = None
        with open(filename) as f:
            data = f.read()
        soup = BeautifulSoup(data)

        articles = soup.findAll('article', attrs={'class': 'podcast'})

        for article in articles:
            id = int(article.attrs['id'][5:])
            title = article.find('h2', attrs={'class': 'entry-title'}).text 
            link = article.find('h2', attrs={'class': 'entry-title'}).find('a').attrs['href']
            text = article.findAll('p')[-1].text 
            name = _extract_name(title)
            items.append([id, link, name, title, text])

    items = sorted(items, key=lambda x:x[0], reverse=True)

    with open(output_path, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(['id', 'link', 'name', 'title', 'text'])
        for item in items:
            writer.writerow(item)

if __name__ == '__main__':
    fire.Fire({
        'brain_inspired': brain_inspired
    })