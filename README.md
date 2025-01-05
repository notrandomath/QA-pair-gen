# Amazon QA Monorepo

A chatbot for customer service QA pair generation

## Installation
To install run `pip install -r requirements.txt`

## Model + Evaluation

All source code is found in `model_and_eval/` folder

To run:
- install requirements.txt
- create a `.env` file with the following:
```
OPENAI_API_KEY=<your_api_key>
```
- run `python model_and_eval/main.py`

Arguments:

- `--cache-dir`: directory to store datasets
- `--output-dir`: directory to store generated QA pairs and evaluation metrics
- `--output-debug`: whether to output model prompt and raw QA pairs
- `--n-examples`: number of example products to use for generating QA pairs

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
5. `get_user_trajectories.py`: creates a json file with user_ids as keys and a list of ASINs interacted by the user as values

At the top of each file is a set of constants that define that paths used by the script. You will need to ensure proper datasets are downloaded and that the paths exist. 

## Relevant Citations:
[Amazon Reviews 2023](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023)
```
@article{hou2024bridging,
  title={Bridging Language and Items for Retrieval and Recommendation},
  author={Hou, Yupeng and Li, Jiacheng and He, Zhankui and Yan, An and Chen, Xiusi and McAuley, Julian},
  journal={arXiv preprint arXiv:2403.03952},
  year={2024}
}
```
[Amazon QA](https://cseweb.ucsd.edu/~jmcauley/datasets/amazon/qa/)
```
Modeling ambiguity, subjectivity, and diverging viewpoints in opinion question answering systems
Mengting Wan, Julian McAuley
International Conference on Data Mining (ICDM), 2016

Addressing complex and subjective product-related queries with customer reviews
Julian McAuley, Alex Yang
World Wide Web (WWW), 2016
```
[ePQA](https://github.com/amazon-science/contextual-product-qa)
```
@article{shen2023xpqa,
  title={xPQA: Cross-Lingual Product Question Answering across 12 Languages},
  author={Shen, Xiaoyu and Asai, Akari and Byrne, Bill and de Gispert, Adri{\`a}},
  journal={arXiv preprint arXiv:2305.09249},
  year={2023}
}
```
[ROUGE](https://github.com/pltrdy/rouge)
```
@inproceedings{lin-2004-rouge,
    title = "{ROUGE}: A Package for Automatic Evaluation of Summaries",
    author = "Lin, Chin-Yew",
    booktitle = "Text Summarization Branches Out",
    month = jul,
    year = "2004",
    address = "Barcelona, Spain",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W04-1013",
    pages = "74--81",
}
```
[BERTScore](https://github.com/Tiiiger/bert_score)
```
@inproceedings{bert-score,
  title={BERTScore: Evaluating Text Generation with BERT},
  author={Tianyi Zhang* and Varsha Kishore* and Felix Wu* and Kilian Q. Weinberger and Yoav Artzi},
  booktitle={International Conference on Learning Representations},
  year={2020},
  url={https://openreview.net/forum?id=SkeHuCVFDr}
}
```