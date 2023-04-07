import requests
import bs4 as bs
import re
import multiprocessing
import sys
import time

import json
from tqdm import tqdm

# Reformats the string into readable text.
def pretty_text(text):
    final = (((text).replace(u'\xa0', u' ')).replace(u'\r ',u'\n'))
    return final

def parse(url):
    sys.stdout.write("+")  # Testing
    sys.stdout.flush()
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = bs.BeautifulSoup(response.content, 'html.parser')

        # Data Extraction from the url.
        poem = (pretty_text(soup.find_all('div', class_="o-poem")[0].text))
        if poem.strip() == "":
            raise IndexError

        title = soup.find_all('h1')[0].text

        poet = soup.find_all('a', href=re.compile('.*poets/.*'))[0].text

        tags = soup.find_all('a', href=re.compile('.*topics.*'))
        tags = [tag.text for tag in tags]
        tags = ",".join(tags)

        return {
            "title": title,
            "poem": poem,
            "poet": poet,
            "tags": tags
        }

    except IndexError:
        article_content = soup.find('article', class_="o-article")
        if article_content:
            article_content.find('div', class_="o-article__content")
            if article_content.find('img'):
                return "img"
        
        return None

    except Exception as e:
        print(e)
        return None

def fetch_poem(poem_id):
    url = "https://www.poetryfoundation.org/poems/" + poem_id
    return (poem_id, parse(url))

def fetch_poems_concurrently(poem_ids, num_workers=None):
    # Use the number of available CPU cores if num_workers is not provided
    num_workers = num_workers or multiprocessing.cpu_count()
    remaining_poem_ids = set(poem_ids)
    invalid = 0

    try:
        fetched_poems = {}
        with multiprocessing.Pool(processes=num_workers) as pool:
            for (poem_id, result) in tqdm(pool.imap_unordered(fetch_poem, poem_ids), total=len(poem_ids), unit="poem", smoothing=0.1):
                if result is not None and result != "img":
                    fetched_poems[poem_id] = result
                    remaining_poem_ids.remove(poem_id)
                    print("VVVVVVV")
                else:
                    if result == "img":
                        remaining_poem_ids.remove(poem_id)
                        print("img", poem_id)
                    else:
                        invalid += 1
                        print("IIIIIIII")
                    
    except KeyboardInterrupt:
        print("\nInterrupted. Saving progress...")


    return fetched_poems, sorted(remaining_poem_ids), invalid

def main():
    with open('remaining_poem_ids.txt') as f:
        poem_ids = f.read().splitlines()

    fetched_poems = {}
    with open('poetry_foundation_poems.json', 'r') as f:
        fetched_poems = json.load(f)

    saved_poems_before = len(fetched_poems)
    new_fetched_poems, remaining_poem_ids, invalid = fetch_poems_concurrently(poem_ids)

    fetched_poems.update(new_fetched_poems)
    saved_poems_after = len(fetched_poems)

    with open('poetry_foundation_poems.json', 'w') as f:
        json.dump(fetched_poems, f)

    with open('remaining_poem_ids.txt', 'w') as f:
        f.write('\n'.join(remaining_poem_ids))

    print("Saved fetched poems to 'poetry_foundation_poems.json'")
    print("Saved remaining poem IDs to 'remaining_poem_ids.txt'")

    # Display progress information
    valid_poems_saved = saved_poems_after
    saved_poems_percentage = (valid_poems_saved / (valid_poems_saved + len(remaining_poem_ids))) * 100
    new_poems_saved = saved_poems_after - saved_poems_before

    print(f"Total poems saved: {valid_poems_saved}")
    print(f"Percentage of total poems saved: {saved_poems_percentage:.2f}%")
    print(f"New poems saved this iteration: {new_poems_saved}")
    print(f"Invalid poems this iteration: {invalid}")

    


    # url_file_names = load(total_pages, total_batches)
    # print(url_file_names)
    # for file_name in url_file_names:

    #     print("START: "+file_name)

    #     urls = np.loadtxt(file_name, dtype="str")
    #     print(urls.size)
    #     urls = np.unique(urls) #Deleting the repeated url links.
    #     print(urls.size)

    #     # Multiprocessing the extractions.
    #     i=0
    #     while(i<urls.size):
    #         timenow = time.time()
    #         p = Pool()
    #         data = 0
    #         if(i+200<urls.size):
    #             data = p.map(parse,urls[i:i+200])
    #         else:
    #             data = p.map(parse,urls[i:urls.size])
    #         print()
    #         print("Should terminate now, took",time.time()-timenow)
    #         p.terminate()
    #         p.join()

    #         print("DONE: "+file_name + str(i) +"-"+str(i+200))
    #         dataF = pd.DataFrame(columns=["Title","Poem","Poet","Tags"], index=list(range(1,200+1)))

    #         for row,rowNo in zip(data,list(range(total_poems))):
    #             dataF.iloc[rowNo] = [row[0],row[1],row[2],row[3]]
    #         dataF = dataF.dropna()
    #         dataF.to_csv("PoetryFoundationData"+file_name[len("PoetryFoundationUrls"):]+ str(i) +"-"+str(i+200)+".csv")
    #         i=i+200



if __name__ == '__main__':
    main()
