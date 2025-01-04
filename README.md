# Amazon QA Monorepo

## Amazon-Combined Dataset Maker
[Link to huggingface datasets](https://huggingface.co/datasets/randomath/Amazon-combined)

All source code is found in `dataset_maker/` folder

Relevant datasets needed:
- [1: Amazon](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023) (only need to download asin2category.json)
- [2: AmazonQA](https://cseweb.ucsd.edu/~jmcauley/datasets/amazon/qa/) (for single and multi-answer QA)
- [6: ePQA](https://github.com/amazon-science/contextual-product-qa)

Order of execution:
1. `export_qa_asins.py`: export the set of ASINs in QA datasets (2, 6)
2. `filter_asins.py`: filter out QA dataset ASINs not present in Amazon Dataset (1)
3. `download_datasets.py`: stream data from (1) and export rows with matching ASINs, takes the longest to run (~10 hours)
4. `combine.py`: combines all data into a single json and uploads to huggingface datasets
5. `get_user_trajectories.py`: gets user

At the top of each file is a set of constants that define that paths used by the script. You will need to ensure proper folders are downloaded and that the paths exist. 