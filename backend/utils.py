import pandas as pd
from pathlib import Path


class PaperDatabase:
    def __init__(self, data_path="updated_papers_dataset2.csv"):
        self.data_path = Path(data_path)
        self.dataset = pd.read_csv(self.data_path)

    def get_names(self):
        names = [str(paper["paper"]) for _, paper in self.dataset.iterrows()]
        return names
