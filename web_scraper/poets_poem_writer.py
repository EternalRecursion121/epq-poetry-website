import json
import requests
import bs4 as bs
import multiprocessing
import signal
from tqdm import tqdm


def extract_poem_info(url):
    try:
        response = requests.get(url)
        html = response.content
        soup = bs.BeautifulSoup(html, features="lxml")

        poem_div = soup.find('div', {'class': 'poem__body'})

        for br in poem_div.find_all(['br']):
            br.replace_with('\n')

        poem_lines = []
        for p in poem_div.find_all('p'):
            poem_lines.append(p.get_text(separator='\n', strip=True))
        
        poem_body = "\n\n".join(poem_lines)

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
            'themes': themes,
            'occasions': occasions,
            'forms': forms
        }
    except Exception as e:
        print(f"Error processing URL: {url}\nError: {e}")
        return None


def process_poem(poem):
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
        with open('poetsog_poems_unique.json', 'r') as f:
            unique_poems = json.load(f)

        poems, start_index = load_progress()
        bad_poems = []

        if poems is None:
            poems = unique_poems

        with multiprocessing.Pool(multiprocessing.cpu_count(), initializer=init_worker) as pool:
            for i, result in enumerate(tqdm(pool.imap(process_poem, poems[start_index:]), total=len(poems), initial=start_index), start=start_index):
                if result is None:
                    bad_poems.append(poems[i])
                else:
                    print("WORKED", poems[i]['title'])
                    poems[i] = result

    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        print(f"Saving progress at i = {i} ({poems[i]['title']})")
        save_progress(poems, i)

        json.dump(poems, f)
    
    # with open('bad_poems.json', 'w') as f:
    #     json.dump(bad_poems, f)

if __name__ == '__main__':
    main()