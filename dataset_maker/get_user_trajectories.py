"""
This script reads the combined.json file and creates a user2asin.json file that maps user ids to the ASINs they have interacted with. 
It also prints the number of users that have interacted with 2, 3, 4, and 5 or more products.
"""

COMBINED_PATH = 'out/epqa_plus_review_and_meta/combined.json' # output path from combine.py
OUT_PATH = 'out/user2asin.json' # output path for user2asin.json

import json
from combine import safe_get

user2asin = {}

print('loading json...')
with open(COMBINED_PATH) as f:
    data = json.load(f)

for entry in data:
    for review in entry['reviews']:
        safe_get(user2asin, review['user_id'], list).append(review['parent_asin'])

def get_num_with_n_product_interactions(n: int) -> int:
    num_items = 0
    for user, val in user2asin.items():
        if len(val) >= n:
            num_items += 1
    return num_items

print(f'total: {len(user2asin)}')
print(f'>=2 products: {get_num_with_n_product_interactions(2)}')
print(f'>=3 products: {get_num_with_n_product_interactions(3)}')
print(f'>=4 products: {get_num_with_n_product_interactions(4)}')
print(f'>=5 products: {get_num_with_n_product_interactions(5)}')

print('dumping json file...')
with open(OUT_PATH, 'w') as f:
    json.dump(user2asin, f)
