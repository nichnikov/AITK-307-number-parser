import os
import operator
import pandas as pd
from itertools import groupby

df = pd.read_csv(os.path.join("data", "synonyms.csv"), sep="\t")
L = [(a, d) for a, d in zip(df["asc"], df["dsc"])]


def group_gen(l: []):
    """генератор"""
    it = groupby(sorted(l, key=lambda x: x[1]), operator.itemgetter(1))
    for k, v in it:
        yield k, [x[0] for x in v]


grp_data = {k: v for k, v in group_gen(L)}
print(grp_data)