"""exports set of ASINS from QA datasets"""

AMAZON_QA_PATH_ONE_ANSWER = '2-AmazonQA/Original/OneAnswer' # path to amazonqa dataset (single answer)
AMAZON_QA_PATH_MULTIPLE_ANSWER = '2-AmazonQA/Original/MultipleAnswers' # path to amazonqa dataset (multiple answer)
EPQA_PATH = '3-CPQA/ePQA' # path to ePQA dataset
OUT_PATH = 'out/qa_asins' # directory to output all asins

import os
import ast
from tqdm import tqdm
import pickle

# Dump AmazonQA

def num_files(path: str) -> int:
    """get number of files in path"""
    return len([file for file in os.listdir(path)])

def dump_asins_amazonqa(in_path, out_path):
    """dump unique asins in amazonqa dataset"""
    asins = set()
    for file in tqdm(os.listdir(in_path), total=num_files(in_path)):
        with open(os.path.join(in_path, file)) as f:
            for l in f:
                asins.add(ast.literal_eval(l)['asin'])
    print(f'number of asins: {len(asins)}')
    with open(out_path, 'wb') as f:
        pickle.dump(asins, f)

dump_asins_amazonqa(AMAZON_QA_PATH_ONE_ANSWER, os.path.join(OUT_PATH, 'amazonqa_one.pkl'))
dump_asins_amazonqa(AMAZON_QA_PATH_MULTIPLE_ANSWER, os.path.join(OUT_PATH, 'amazonqa_multiple.pkl'))

# Dump EPQA

import pandas as pd

asins = set()

for file in os.listdir(EPQA_PATH):
    df = pd.read_csv(os.path.join(EPQA_PATH, file))
    asins |= set(df['ASIN'])

print(f'number of asins: {len(asins)}')
with open(os.path.join(OUT_PATH, 'epqa.pkl'), 'wb') as f:
    pickle.dump(asins, f)
