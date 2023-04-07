# with open('poems.org_page_list.txt', 'w') as f:
#     for i in range(696):
#         f.write(f'{i}\n')

# with open('poetry_foundation_page_list.txt', 'w') as f:
#     for i in range(2346):
#         f.write(f'{i}\n')

import json

with open('ids.json') as f:
    json_obj: dict = json.load(f)
    poem_ids = sorted([_id for page in json_obj.values() for _id in page])

    with open('poem_ids.txt', 'w') as f2:
        for _id in poem_ids:
            f2.write(f'{_id}\n')
