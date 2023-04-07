#import urllib.request #This won't be used as the tables are dynamically loaded.
import bs4 as bs
import re
import requests

import aiohttp
import asyncio


total_pages     = 10
links_per_page  = 20

pages = {}

async def id_extract(page_number):
    print("STARTED")
    url = f'https://www.poetryfoundation.org/ajax/poems?page={page_number}&sort_by=recently_added'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:   
                #data = json.loads(await response.read())
                data = await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                print(await response.read())
                print("DON'T GOT THE DATA")
                await asyncio.sleep(2)
                try:
                    async with session.get(url) as response:
                        data = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    print("DON'T GOT THE DATA", page_number)
                    return []
            print("GOT THE DATA")
    try:
        entries = data['Entries']
    except ValueError:
        print("DFJHSKFJDSKFJKSJDFKJSF")
        return []
    if entries:
        pages[page_number] = "Working"
    else:
        pages[page_number] = "Not Working"
    return [entry['id'] for entry in entries]

async def scrape():
    tasks = []
    for i in range(1, 2318):
        tasks.append(id_extract(i))
    for i in range(2318//50 + 1):
         await asyncio.gather(*tasks[i*50:(i+1)*50])

    #print(await asyncio.gather(*tasks))
    
    

def extract_poem_info(poem_id):
    url = f"https://www.poetryfoundation.org/poems/{poem_id}"
    html = requests.get(url).text
    soup = bs.BeautifulSoup(html,'html.parser') #Beautiful Soup object

    title = soup.find_all('h1')[0].text
    poem = ''.join([div.text.encode("ascii", "ignore").decode() for div in soup.find_all('div', class_="o-poem")]).replace('\r', '\n')
    tags = ",".join(tag.text for tag in soup.find_all('a', href=re.compile('.*topics.*')))

    return title, poem, tags

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(scrape())
print(extract_poem_info(33486))

