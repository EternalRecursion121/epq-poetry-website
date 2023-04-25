import requests
import bs4 as bs
import json
from tqdm import tqdm
import multiprocessing
import signal
import regex

TOTAL_PAGES = 703

cache = set()

def extract_poem_info(url):
    if url in cache:
        return None
    cache.add(url)
    try:
        response = requests.get(url)
        html = response.content.decode('utf-8').replace('</p>', '\n\n</p>').encode('utf-8')
        soup = bs.BeautifulSoup(html, features="lxml")



        poem_div = soup.find('div', {'class': 'poem__body'})

        for br in poem_div.find_all('br'):
            br.replace_with('\n')

        poem_body = poem_div.get_text().rstrip()

        if not poem_body.strip():
            return None

        tag_div = soup.find('div', {'class': 'poet--aside__tags'})

        themes = []
        occasions = []
        forms = []

        for tag in tag_div.find_all('div', {'class': 'poet--aside__tag'}):
            title = tag.find('div', {'class': 'poet--aside__tag-title'}).get_text(strip=True)
            tag_names = [a.get_text(strip=True) for a in tag.find_all('a')]

            if title == 'Themes':
                themes = tag_names
            elif title == 'Occasions':
                occasions = tag_names
            elif title == 'Forms':
                forms = tag_names
        
        return {
            'poem': poem_body,
            'themes': [theme for theme in themes if theme != 'audio' and theme != 'public domain'],
            'occasions': occasions,
            'forms': forms
        }
    except Exception as e:
        print(f"Error processing URL: {url}\nError: {e}")
        return None

def extract_row(row):
    html = bs.BeautifulSoup(row['body'], features="lxml").findAll('span')
    title = row['title']
    if "audio only" in title.lower():
        return None
    author = bs.BeautifulSoup(row['field_author'], features="lxml").get_text()
    url = "https://poets.org" + row['view_node']

    poem_info = extract_poem_info(url)
    if poem_info:
        return {'title': title,
                'author' : author,
                'date_published': row['field_date_published'],
                'link': url, 
                **poem_info}
    
    return None
        

def extract_page(page):
    poems = []
    bad = []
    try:
        rows = requests.get(f"https://api.poets.org/api/poems?page={page}").json()['rows']
        for row in rows:
            poem = extract_row(row)
            if poem:
                poems.append(poem)
            else:
                bad.append(row)
        return poems, bad
    except json.decoder.JSONDecodeError:
        print(f"JSON Decode Error- Page {page}")
        return [], []
    
def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def main():
    good_poems = []
    bad_poems = []
    last_completed_page = -1

    try:
        with multiprocessing.Pool(initializer=init_worker) as pool:
            for i, result in enumerate(tqdm(pool.imap(extract_page, range(TOTAL_PAGES)), total=TOTAL_PAGES)):
                good_poems.extend(result[0])
                bad_poems.extend(result[1])
                last_completed_page = i

            print("POEMS FOUND: ", len(good_poems))
            print("BAD POEMS: ", len(bad_poems))
            print("SAVING...")


    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        print(f"Saving progress at page = {last_completed_page}")

    with open('poetsorg_poems.json', 'w') as f:
        json.dump(good_poems, f)

    with open('bad_poems.json', 'w') as f:
        json.dump(bad_poems, f)

if __name__=='__main__':
    main()

    


