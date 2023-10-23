from ast import literal_eval
import pandas as pd
from pathlib import Path
import numpy as np
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer


class Similarity_calculator():
    def __init__(self):

        self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        self.data_path = Path("updated_papers_dataset2.csv")
        self.dataset = pd.read_csv(self.data_path)

    def get_top(self,paragraph,k):

        para_embedding = list(self.model.encode(paragraph))

        scores = []

        for i in self.dataset.index:

            summary_embedding = literal_eval(self.dataset.iloc[i]["summary_embedding"])
            score = self.get_score(para_embedding,summary_embedding)

            scores.append(score)

        scores_arr = np.array(scores)
        top=scores_arr.argsort()[-k:][::-1]


        papers = [str(self.dataset.iloc[i]["paper"]) for i in top]
        summaries = [str(self.dataset.iloc[i]["summary"]) for i in top]
        abstract = [str(self.dataset.iloc[i]["abstract"]) for i in top]
        similarity_scores = [ round(scores[i],4) for i in top]

        return {
                "papers":papers,
                "scores":similarity_scores,
                "summaries":summaries,
                "abstracts": abstract
                }

    def get_score(self,emb1,emb2):
        score = np.dot(emb1,emb2)/(norm(emb1)*norm(emb2))

        return score