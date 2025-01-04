"""
Since tha amazon dataset has hundreds of GB of data, instead of saving it locally,
streams the dataset and only keeps the data that is relevant to the EPQA dataset.
"""

FILTERED_CATEGORIES = 'out/epqa_category.json' # path to epqa_category.json from filter_asins.py
OUTPUT_DIR = 'out/epqa_plus_review_and_meta/split' # output directory for dataset split on category

from datasets import load_dataset
import json
from tqdm import tqdm
import os

repo_id = 'McAuley-Lab/Amazon-Reviews-2023'
subfolder_review = 'raw/review_categories'
subfolder_meta = 'raw/meta_categories'

review_prefix = 'raw_review_'
meta_prefix = 'raw_meta_'

with open(FILTERED_CATEGORIES) as f:
    category2asin = json.load(f)

def add_to_dataset(prefix, category, asins):
    output_path = os.path.join(OUTPUT_DIR, f'{prefix}{category}.json')
    if os.path.exists(output_path):
        print(f'folder already exists: {output_path}')
        return
    output = dict()
    dataset = load_dataset(repo_id, prefix+category, streaming=True)
    for val in tqdm(dataset['full'], desc=category):
        asin = val['parent_asin']
        if asin in asins:
            if asin in output:
                output[asin].append(val)
            else:
                output[asin] = [val]
    with open(output_path, 'w') as f:
        json.dump(output, f)

n = len(category2asin.keys())
i = 1

for category, asins in category2asin.items():
    print(f'{i} / {n} categories')
    add_to_dataset(review_prefix, category, asins)
    add_to_dataset(meta_prefix, category, asins)
    i += 1
