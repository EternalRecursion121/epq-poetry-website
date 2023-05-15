import json
import requests
import bs4 as bs
import multiprocessing
import signal
from tqdm import tqdm
import regex


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

def process_poem(poem):
    if not (poem['poem'] and (poem.get('themes') or poem.get('occasions') or poem.get('forms'))):
        info = extract_poem_info(poem['link'])
        if info is not None:
            poem.update(extract_poem_info(poem['link']))
            return poem
    return None


def save_progress(poems, current_index):
    with open('poetsorg_poems_progress.json', 'w') as f:
        json.dump({'poems': poems, 'current_index': current_index}, f)

def load_progress():
    try:
        with open('poetsorg_poems_progress.json', 'r') as f:
            progress = json.load(f)
            return progress['poems'], progress['current_index']
    except FileNotFoundError:
        return None, 0

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def main():
    try:
        with open('poetsorg_poems_unique.json', 'r') as f:
            unique_poems = json.load(f)

        poems, start_index = load_progress()
        bad_poems = []

        if poems is None:
            poems = unique_poems

        with multiprocessing.Pool(multiprocessing.cpu_count(), initializer=init_worker) as pool:
            for i, result in enumerate(tqdm(pool.imap(process_poem, poems[start_index:]), total=len(poems[start_index:]), initial=start_index), start=start_index):
                if result is None:
                    bad_poems.append(poems[i])
                else:
                    print("WORKED", poems[i]['title'])
                    poems[i] = result

    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        print(f"Saving progress at i = {i} ({poems[i]['title']})")
        save_progress(poems, i)

    with open('poetsorg_poems_complete.json', 'w') as f:
        json.dump(poems, f)
    
    with open('bad_poems.json', 'w') as f:
        json.dump(bad_poems, f)

if __name__ == '__main__':
    # main()
    print(extract_poem_info('https://poets.org/poem/ol-tunes')['poem'])