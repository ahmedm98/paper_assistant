import pandas as pd
from pathlib import Path
from tqdm import tqdm

from backend.utils import Similarity_calculator


def evaluate_method(data_path):
    """Evaluate the current method of computing paper similarity:
    For every paper's abstract, retrieve the top 3 most similar papers.
    Note that the abstracts have been omitted from the text
    used to create the summaries.
    If the original paper of the abstract appears in the recommended
    3 papers then this counts as
    a correct prediction. If not, then it is false prediction.

    :param data_path: the path to the dataset
    :type data_path: str

    :returns: the accuracy score based on the provided dataset
    :rtype: float
    """

    data = pd.read_csv(Path(data_path))
    sim_calc = Similarity_calculator(data_path)
    predictions = []
    with tqdm(total=len(data)) as progress:
        for i in data.index:
            abstract = str(data.iloc[i]["abstract"])
            top_papers = sim_calc.get_top(paragraph=abstract, k=3)
            if data.iloc[i]["paper"] in top_papers["papers"]:
                predictions.append(1)
            else:
                predictions.append(0)
            progress.update()

    return round(sum(predictions) / len(predictions), 4)


if __name__ == "__main__":
    score = evaluate_method("backend/updated_papers_dataset2.csv")

    print(f"The current method has an accuracy of {score}.")
