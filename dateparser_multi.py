# https://www.tutorialspoint.com/How-to-extract-date-from-text-using-Python-regular-expression
# https://stackoverflow.com/questions/4709652/python-regex-to-match-dates
# https://dateparser.readthedocs.io/en/latest/

import os
import pandas as pd
from dateparser import search

df = pd.read_csv(os.path.join("data", "NUMERIC_FILTR.csv"), sep="\t")
tx_list = list(df["Text"])
print(tx_list)
for tx in tx_list:
    print(tx, search.search_dates(tx, languages=["ru"]))