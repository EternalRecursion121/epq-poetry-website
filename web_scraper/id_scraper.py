import requests
import bs4 as bs
import re
import json
from threading import Thread
from time import sleep, time

def scrape():
    return [id_extract(i)for i in range(1, 2346)]

def get_remaining_numbers():
    nums = []
    with open('poetry_foundation_page_list.txt') as f:
        for line in f.readlines():
            try:
                nums.append(int(line))
            except ValueError:
                print("NOT NUMBER")
    return nums

def extract_thread():
    i=1
    while page_numbers:
        id_extract(page_numbers.pop(), i)
        i += 1

def id_extract(page_number, i=-1):
    global ids, bad
    print("STARTED", page_number)
    url = f'https://www.poetryfoundation.org/ajax/poems?page={page_number}&sort_by=recently_added'
    try:
        data = requests.get(url, timeout=30).json()
    except json.JSONDecodeError:
        print("JSON DECODE ERROR")
        bad.append(page_number)
        #sleep(5)
        return
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        if type(e) == requests.exceptions.ConnectionError:
            print("CONNECTION ERROR")
            #sleep(10)
        elif type(e) == requests.exceptions.ReadTimeout:
            print("READ TIMEOUT ERROR")
            #sleep(10)

        bad.append(page_number)
        return
    entries = data['Entries']
    if entries:
        print(f"Page {page_number} Working")
        ids[str(page_number)] = [entry['id'] for entry in entries]
    else:
        print("No Entries")
        bad.append(page_number)
        #sleep(10)
    sleep(0.25)
    print(f"{(i/length)*100:.3f}% Complete. ETA: {(((time()-start)/i)*(length-i))/60:.1f}m")
    

def extract_poem_info(poem_id):
    url = f"https://www.poetryfoundation.org/poems/{poem_id}"
    html = requests.get(url, timeout=30).text
    soup = bs.BeautifulSoup(html,'html.parser') #Beautiful Soup object

    title = soup.find_all('h1')[0].text
    poem = ''.join([div.text.encode("ascii", "ignore").decode() for div in soup.find_all('div', class_="o-poem")]).replace('\r', '\n')
    tags = ",".join(tag.text for tag in soup.find_all('a', href=re.compile('.*topics.*')))

    return title, poem, tags

bad = True

try:
    while bad:
        page_numbers = get_remaining_numbers()

        ids = {}
        # threads = [Thread(target=extract_thread) for i in range(1)]
        bad = []

        # for t in threads:
        #     t.start()
        #     sleep(4)

        # for t in threads:
        #     t.join()
        start = time()
        length = len(page_numbers)
        extract_thread()
        with open('poetry_foundation_page_list.txt', 'r') as f:
            x = f.readlines()
            with open('poetry_foundation_page_list.txt', 'w') as f:
                for line in x:
                    try:
                        if int(line) in bad:
                            f.write(line)
                    except ValueError:
                        print("VALUESEFRRROR")


        with open('ids.json') as f:
            json_obj: dict = json.load(f)
            old_length = len(json_obj)
            print(f"Old length: {old_length}")
            json_obj.update(ids)
            new_length = len(json_obj)
            print(f"New length: {new_length}")
            print(f"Added {new_length-old_length} poems")
            print(f"Collection {new_length/2345*100:.2f}% completed")

        with open('ids.json', 'w') as f:
            json.dump(json_obj, f)





except KeyboardInterrupt:
    print("Keyboard Interrupt")
    bad.extend(page_numbers)

with open('poetry_foundation_page_list.txt', 'r') as f:
    x = f.readlines()
    with open('poetry_foundation_page_list.txt', 'w') as f:
        for line in x:
            try:
                if int(line) in bad:
                    f.write(line)
            except ValueError:
                print("VALUESEFRRROR")


with open('ids.json') as f:
    json_obj: dict = json.load(f)
    old_length = len(json_obj)
    print(f"Old length: {old_length}")
    json_obj.update(ids)
    new_length = len(json_obj)
    print(f"New length: {new_length}")
    print(f"Added {new_length-old_length} pages")
    print(f"Collection {new_length/2345*100:.2f}% completed")
    page_numbers = list(set(map(str, range(1, 2346))) - set(json_obj.keys()))
    print("Page numbers: ", page_numbers)

with open('ids.json', 'w') as f:
    json.dump(json_obj, f)

bad = True
while bad:
    # threads = [Thread(target=extract_thread) for i in range(1)]
    bad = []
    # for t in threads:
    #     t.start()
    #     sleep(4)

    # for t in threads:
    #     t.join()
    start = time()
    print(page_numbers)
    length = len(page_numbers)
    extract_thread()
    with open('poetry_foundation_page_list.txt', 'r') as f:
        x = f.readlines()
        with open('poetry_foundation_page_list.txt', 'w') as f:
            for line in x:
                try:
                    if int(line) in bad:
                        f.write(line)
                except ValueError:
                    print("VALUESEFRRROR")


    with open('ids.json') as f:
        json_obj: dict = json.load(f)
        old_length = len(json_obj)
        print(f"Old length: {old_length}")
        json_obj.update(ids)
        new_length = len(json_obj)
        print(f"New length: {new_length}")
        print(f"Added {new_length-old_length} poems")
        print(f"Collection {new_length/2346*100:.2f}% completed")

    with open('ids.json', 'w') as f:
        json.dump(json_obj, f)



