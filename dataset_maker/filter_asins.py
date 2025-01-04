"""
This script filters out the ASINs from the Amazon dataset that are not present in the EPQA dataset.
It also counts the number of ASINs that are in both datasets.
"""

PATH_TO_ASIN2CATEGORY = '1-Amazon/2023/asin2category.json' # path to asin2category.json from Amazon dataset
PATH_TO_QA_ASINS = 'out/qa_asins' # output path from export_qa_asins.py
OUT_PATH = 'out/epqa_category.json' # output path for asin2category.json

# number of ASINS in each directory:
# epqa.pkl: 2980
# amazonqa_one.pkl: 105481
# amazonqa_multiple.pkl: 99064

import os
import pickle
import json

print('loading asin keys...')
with open('1-Amazon/2023/asin2category.json') as f:
    asin2category = json.load(f)

for file in os.listdir(PATH_TO_QA_ASINS):
    with open(os.path.join(PATH_TO_QA_ASINS, file), 'rb') as f:
        asins = pickle.load(f)
        asins &= asin2category.keys()
        print(f'new # of asins for {file}: {len(asins)}')

with open(os.path.join(PATH_TO_QA_ASINS, 'epqa.pkl'), 'rb') as f:
    asins = pickle.load(f)
    asins &= asin2category.keys()
    new_dict = {}
    for asin in asins:
        category = asin2category[asin].replace(' ', '_')
        if category in new_dict:
            new_dict[category].append(asin)
        else:
            new_dict[category] = [asin]
    with open(OUT_PATH, 'w') as f :
        json.dump(new_dict, f)
