import pandas as pd
import numpy as np

def load_data(path: str) -> pd.DataFrame:
    if path.endswith(".tsv"):
        return pd.read_csv(path, sep="\t")
    return pd.read_csv(path)