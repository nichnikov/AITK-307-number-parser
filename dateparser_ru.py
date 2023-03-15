# https://pypi.org/project/rutimeparser/
import os
import pandas as pd
from rutimeparser import parse, get_last_clear_text

df = pd.read_csv(os.path.join("data", "NUMERIC_FILTR.csv"), sep="\t")
tx_list = list(df["Text"])
for tx in tx_list:
    print(tx)
    print(tx, parse(tx))