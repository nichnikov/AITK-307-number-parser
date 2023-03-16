import re
import os
import time
import pandas as pd

# рубли https://docs.google.com/spreadsheets/d/1uVllieSyjvu2ElubsFQTBGr_9RtHZVzFOEaGHjog0XU/edit#gid=0

df = pd.read_csv(os.path.join("data", "NUMERIC_FILTR.csv"), sep="\t")
tx_list = [re.sub(r'[^\d\w\s.,]', " ", str(tx)) for tx in list(df["Text"])]
print(tx_list)


date_patterns = re.compile(r'\d{2}\.\d{2}.\d{4}|\d{4}\.\d{2}.\d{2}|\d{4}\s{0,3}г|'
                           r'(?:янв\w+|фев\w+|мар\w+|апр\w+|мая\w+|июн\w+|июл\w+|авг\w+|сен\w+|окт\w+'
                           r'|ноя\w+|дек\w+)\s{0,3}\d{4}|\d\s{0,3}кв\w+\s+\d{4}|\d\s{0,3}кв.{0,3}\d{4}')

fsbu_patterns = re.compile(r'фсбу\s*\d+(?:\/|\-)\d+|\d+(?:\/|\-)\d+\s*фсбу')

nk_patterns = re.compile(r'(?:\bнк.{0,1}\b.+\bст|\bст.{0,1}\b.+\bнк|\bпп.{0,1}\b.+\bп[\.\s]{0,1}\b.+\bст.{0,1}\b.+\bнк|'
                         r'\bп[\.\s]{0,1}\b.+\bст.{0,1}\b.+\bнк)')

fz_patterns = re.compile(r'(?:\d+.{0,2}фз|фз.{0,2}\d+)')
kbk_patterns = re.compile(r'(?:\d+.{0,3}кбк|кбк.{0,3}\d+)')
forms_patterns = re.compile(
    r'(?:\d+.{0,2}\bформ\w+|\bформ\w+.{0,2}\d+|\bформ\w+.{0,2}\w+[-/\\\s+]\d+|\b\w+[-/\\\s+]\d+.{0,2}\bформ)')
knd_patterns = re.compile(r'(?:\d+.{0,2}кнд|кнд.{0,2}\d+)')
ndfl_patterns = re.compile(r'(?:\d\b.{0,2}ндфл|ндфл.{0,2}\d\b)')
npa_patterns = re.compile(r'\d+(?:[-/]\d+)+')
money_patterns = re.compile(r'(?:\d{1,10}(?:|[,.\s])\d{1,10})+(?:|\s+)(?:м[лнрдионад]{0,7}\b(?:|[\s.,])р[убляей]{0,7}\b|т[ысячи]{0,7}\b(?:|[\s.,])р[убляей]{0,7}\b|р[убляей]{0,7}\b(?:|[\s.,]))')


keys_df = pd.read_csv(os.path.join("data", "keywords.csv"), sep="\t")
keys_patterns = re.compile("|".join(list(keys_df["keys"])))

patterns_dict = {"DATES": (date_patterns, "genдата"),
                 "FSBU": (fsbu_patterns, "genфсбу"),
                 "NK": (nk_patterns, "genнкстатья"),
                 "FZ": (fz_patterns, "genфз"),
                 "KBK": (kbk_patterns, "genкбк"),
                 "FORMS": (forms_patterns, "genформа"),
                 "KND": (knd_patterns, "genкнд"),
                 "NDFL": (ndfl_patterns, "genндфл"),
                 "NPA": (npa_patterns, "genнпа"),
                 "MONEY": (money_patterns, "genденьги")
                 }


parsing_texts = []
for tx in tx_list:
    tx = str(tx).lower()
    d = {"text": tx}
    for i in patterns_dict:
        d[i] = [re.sub(r'[^\d\w\s,.]', "", t) for t in re.findall(patterns_dict[i][0], str(tx))]
        if d[i]:
            for pt in d[i]:
                tx = re.sub(pt, patterns_dict[i][1], str(tx))
    d["UNCNOWN_NUM"] = re.findall(r'(?:\w+[\/-]\d+|\d+[\/-]\w+|\d+)', tx)
    d["KEYS"] = re.findall(keys_patterns, tx)
    tx = re.sub(r'\d+', "цифра", str(tx))
    d["clear_text"] = tx
    parsing_texts.append(d)

print(parsing_texts)
parsing_texts_df = pd.DataFrame(parsing_texts)
print(parsing_texts_df)
parsing_texts_df.to_csv("parsing_texts.csv", sep="\t", index=False)
# parsing_texts_df.to_csv("parsing_texts.csv", index=False)
