import requests
import bs4 as bs
import json
import asyncio

TOTAL_PAGES = 631

def get_remaining_numbers():
    nums = []
    with open('poetsorg_page_list.txt') as f:
        for line in f.readlines():
            try:
                nums.append(int(line))
            except ValueError:
                print("NOT NUMBER")
    return nums

def extract_row(row):
    html = bs.BeautifulSoup(row['body'], features="lxml").findAll('span')
    poem = '\n'.join(map(lambda x:x.get_text(), html))
    author = bs.BeautifulSoup(row['field_author'], features="lxml").get_text()
    return {'title': row['title'],
            'poem': poem,
            'author' : author,
            'date_published': row['field_date_published'],
            'link': "https://poets.org" + row['view_node']}

async def extract_page(page):
    global bad
    print(page)
    try:
        rows = requests.get(f"https://api.poets.org/api/poems?page={page}").json()['rows']
        return [extract_row(row) for row in rows]
    except json.decoder.JSONDecodeError:
        print(f"JSON Decode Error- Page {page}")
        bad.append(page)
        return []

async def extraction_worker():
    global pages, poems
    while pages:
        poems.extend(await extract_page(pages.pop()))

async def main():
    pages = get_remaining_numbers()
    poems = []
    bad = []
    workers = [extraction_worker() for i in range(5)]
    await asyncio.gather(*workers)
    with open('poetsorg_poems.json', 'w') as f:
        json.dump(poems, f)
    with open('pages.txt', 'r') as f:
        x = f.readlines()
    with open('pages.txt', 'w') as f:
        for line in x:
            try:
                if int(line) in bad:
                    f.write(line)
            except ValueError:
                print("VALUESEFRRROR")

if __name__=='__main__':
    asyncio.run(main())