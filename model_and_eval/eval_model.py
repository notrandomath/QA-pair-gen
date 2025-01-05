from evaluate import load

bertscore = load("bertscore")
rouge = load("rouge")


def get_rouge_scores(preds: list[str], refs: list[str]) -> dict:
    return rouge.compute(
        predictions=preds,
        references=refs,
    )


def get_bert_scores(preds: list[str], refs: list[str]) -> dict:
    return bertscore.compute(
        predictions=preds, references=refs, model_type="distilbert-base-uncased"
    )
