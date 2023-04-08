import requests
import bs4 as bs
import json
from time import sleep

TOTAL_PAGES = 696

def extract_row(row):
    html = bs.BeautifulSoup(row['body'], features="lxml").findAll('span')
    poem = '\n'.join(map(lambda x:x.get_text(), html))
    author = bs.BeautifulSoup(row['field_author'], features="lxml").get_text()
    return {'title': row['title'],
            'poem': poem,
            'author' : author,
            'date_published': row['field_date_published'],
            'link': "https://poets.org" + row['view_node']}

def extract_page(page):
    print(page)
    sleep(1)
    try:
        rows = requests.get(f"https://api.poets.org/api/poems?page={page}").json()['rows']
        return [extract_row(row) for row in rows]
    except json.decoder.JSONDecodeError:
        print(f"JSON Decode Error- Page {page}")
        return []


def main():
    with open('poetsorg_poems.json', 'w') as f:
        poems = [poem for page in [extract_page(i) for i in range(TOTAL_PAGES)] for poem in page]
        json.dump(poems, f)

if __name__=='__main__':
    main()

    


