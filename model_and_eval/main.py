from datasets import load_dataset
from utils import build_asin_2_product, parse_qa_pairs
from sample_user_trajectories import UserTrajectories
from sample_text_chunks import SampleTextChunks
from model import get_response
from eval_model import get_rouge_scores, get_bert_scores
import argparse
import os
import json
from tqdm import tqdm


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=str, default="out", help="directory to store datasets")
    parser.add_argument("--output-dir", type=str, default="out/generated_qa_pairs", help="directory to store generated QA pairs and evaluation metrics")
    parser.add_argument("--output-debug", action="store_true", help="whether to output model prompt and raw QA pairs")
    parser.add_argument("--n-examples", type=int, default=3, help="number of example products to use for generating QA pairs")
    args = parser.parse_args()
    os.makedirs(args.cache_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)

    # load dataset and build asin to product name dictionary
    dataset = load_dataset(
        "randomath/Amazon-combined", split="train", cache_dir=args.cache_dir
    )
    build_asin_2_product(dataset)

    # shuffle and select n examples
    dataset = dataset.shuffle()
    dataset = dataset.select(range(args.n_examples))

    # download user trajectories
    user_trajectories = UserTrajectories()
    user_trajectories.download(args.cache_dir)

    # initialize text chunker, predictions, and references
    textChunker = SampleTextChunks()
    preds = []
    refs = []

    for i, entry in tqdm(enumerate(dataset), desc="generating qa pairs", total=args.n_examples):
        # get similar products a user has interacted with
        user_trajectory = user_trajectories.sample_user_interactions(entry)
        user_trajectory = ",".join(user_trajectory[0]) if user_trajectory else ""
        # sample text chunks from review and description
        product_info = "\n".join(textChunker.sample(entry))
        # get openAI response with QA pairs
        qa_pair = get_response(
            entry["title"],
            product_info,
            user_trajectory,
            print_prompt=(
                os.path.join(args.output_dir, f"prompt_{i}.txt")
                if args.output_debug
                else ""
            ),
        )
        # append to predictions and references
        refs.append(entry["title"] + product_info + user_trajectory)
        preds.append(qa_pair)
        # output results
        if args.output_debug:
            with open(os.path.join(args.output_dir, f"raw_qa_pairs_{i}.txt"), "w") as f:
                f.write(qa_pair)
        with open(os.path.join(args.output_dir, f"qa_pairs_{i}.json"), "w") as f:
            json.dump(parse_qa_pairs(qa_pair), f, indent=4)
        # reset text chunker for next iteration
        textChunker.reset()

    # evaluate QA pairs
    print("evaluating QA pairs...")
    eval_dict = {
        "rouge": get_rouge_scores(preds, refs),
        "bert": get_bert_scores(preds, refs),
    }
    with open(os.path.join(args.output_dir, "eval.json"), "w") as f:
        json.dump(eval_dict, f, indent=4)


if __name__ == "__main__":
    main()
