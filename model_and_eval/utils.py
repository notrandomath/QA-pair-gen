from datasets import Dataset
from tqdm import tqdm

asin2product_dict = {}

def build_asin_2_product(dataset: Dataset) -> None:
    """builds asin to product name dictionary"""
    for entry in tqdm(
        dataset, total=len(dataset), desc="building asin2product dictionary"
    ):
        asin2product_dict[entry["asin"]] = entry["title"]


def asin2product(asin: str) -> str:
    """gets product name from asin"""
    return asin2product_dict[asin]


def parse_qa_pairs(qa_pairs: str) -> list[tuple[str, str]]:
    """parses qa pairs from generated text"""
    return [
        {"question": pair.split("|")[0], "answer": pair.split("|")[1]}
        for pair in qa_pairs.split("\n\n")
    ]
