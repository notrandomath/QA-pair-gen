"""file for combining all the datasets, saving to json, and pushing to huggingface"""

SPLIT_PATH = 'out/epqa_plus_review_and_meta/split' # path from download_dataset.py
EPQA_PATH = '3-CPQA/ePQA' # path to ePQA dataset
OUTPUT_PATH = 'out/epqa_plus_review_and_meta/combined.json' # path to save combined dataset

import os
import json
import pandas as pd
from typing import Any, Callable
from datasets import Dataset

def safe_get(cur_dict: dict, key: Any, factory: Callable[..., Any]):
    """
    mimics defaultdict behavior without creating new class
    doesn't work on primitives
    """
    if key not in cur_dict:
        cur_dict[key] = factory()
    return cur_dict[key]

if __name__ == '__main__':
    combined_dict = dict()

    # iterate through meta
    for file in os.listdir(SPLIT_PATH):
        with open(os.path.join(SPLIT_PATH, file)) as f:
            print(f'processing {file}...')
            amazon_json = json.load(f)
            if file.startswith('raw_meta'):
                for asin, meta_list in amazon_json.items():
                    # never more than one item in the list for meta
                    safe_get(combined_dict, asin, dict).update(meta_list[0])
            if file.startswith('raw_review'):
                for asin, reviews in amazon_json.items():
                    safe_get(combined_dict, asin, dict)['reviews'] = reviews

    for asin in combined_dict:
        if 'reviews' not in combined_dict[asin]:
            del combined_dict[asin]

    print(len(combined_dict.keys()))

    for file in os.listdir(EPQA_PATH):
        df = pd.read_csv(os.path.join(EPQA_PATH, file))
        df = df.fillna("")
        for row in df.itertuples():
            if row.ASIN in combined_dict:
                qs_dict = safe_get(combined_dict[row.ASIN], 'qa_pairs', dict)
                answers = safe_get(qs_dict, row.question, list)
                answers.append({"answer": row.answer, "candidate": row.candidate, "label": row.label})

    final_dataset = []
    for asin, vals in combined_dict.items():
        for question in vals['qa_pairs']:
            vals['qa_pairs'][question] = {'question': question, 'answers': vals['qa_pairs'][question]}
        vals['qa_pairs'] = list(vals['qa_pairs'].values())
        final_dataset.append(vals | {'asin': asin})

    print('dumping json...')
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(final_dataset, f)

    dataset = Dataset.from_list(final_dataset)
    dataset.push_to_hub('randomath/Amazon-combined')
