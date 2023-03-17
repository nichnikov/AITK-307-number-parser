import os
import fasttext
import pandas as pd
from my_parser import parser
from sklearn.metrics.pairwise import cosine_distances
from texts_processing import TextsTokenizer


tokenizer = TextsTokenizer()

syns_df = pd.read_csv(os.path.join("data", "synonyms.csv"), sep="\t")
quries_df = pd.read_csv(os.path.join("data", "queries_mistakes.csv"), sep="\t")

ft_models = fasttext.load_model(os.path.join("models", "bss_cbow_lem.bin"))

L = [(a, d) for a, d in zip(syns_df["asc"], syns_df["dsc"])]
tokenizer.add_synonyms(L)

parsing_texts = []
for tx1, tx2 in zip(list(quries_df["Query"]), list(quries_df["Etalon"])):
    dct_tx1 = parser(tx1)
    dct_tx2 = parser(tx2)
    lm_tx1 = tokenizer([dct_tx1["clear_text"]])
    lm_tx2 = tokenizer([dct_tx2["clear_text"]])
    dct_tx1["lem_text"] = " ".join(lm_tx1[0])
    dct_tx2["lem_text"] = " ".join(lm_tx2[0])
    print("text1:", tx1, "text2:", tx2)
    print("lem text1:", " ".join(lm_tx1[0]), "lem text2:", " ".join(lm_tx2[0]))
    v1 = ft_models.get_sentence_vector(" ".join(lm_tx1[0]))
    v2 = ft_models.get_sentence_vector(" ".join(lm_tx2[0]))
    score = cosine_distances([v1, v2])
    print(score[0][1])
    parsing_texts.append(dct_tx1)
    parsing_texts.append(dct_tx2)

parsing_texts_df = pd.DataFrame(parsing_texts)
parsing_texts_df.to_csv(os.path.join("data", "parsing_data.csv"), sep="\t")