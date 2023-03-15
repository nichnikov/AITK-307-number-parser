import re
import os
import pandas as pd

df = pd.read_csv(os.path.join("data", "NUMERIC_FILTR.csv"), sep="\t")
tx_list = list(df["Text"])

date_patterns = re.compile(r'\d{2}\.\d{2}.\d{4}|\d{4}\.\d{2}.\d{2}|\d{4}\s{0,3}г|'
                           r'(?:янв\w+|фев\w+|мар\w+|апр\w+|мая\w+|июн\w+|июл\w+|авг\w+|сен\w+|окт\w+'
                           r'|ноя\w+|дек\w+)\s{0,3}\d{4}|\d\s{0,3}кв\w+\s+\d{4}|\d\s{0,3}кв.{0,3}\d{4}')

fsbu_patterns = re.compile(r'фсбу\s*\d+(?:\/|\-)\d+|\d+(?:\/|\-)\d+\s*фсбу')

nk_patterns = re.compile(r'(?:\bнк.{0,1}\b.+\bст|\bст.{0,1}\b.+\bнк|\bпп.{0,1}\b.+\bп[\.\s]{0,1}\b.+\bст.{0,1}\b.+\bнк|'
                         r'\bп[\.\s]{0,1}\b.+\bст.{0,1}\b.+\bнк)')

fz_patterns = re.compile(r'(?:\d+.{0,2}фз|фз.{0,2}\d+)')
kbk_patterns = re.compile(r'(?:\d+.{0,2}кбк|кбк.{0,2}\d+)')
forms_patterns = re.compile(r'(?:\d+.{0,2}форм\w+|форм\w+.{0,2}\d+|форм\w+.{0,2}\w+[-/\\\s+]\d+|\b\w+[-/\\\s+]\d+.{0,2}форм)')
knd_patterns = re.compile(r'(?:\d+.{0,2}кнд|кнд.{0,2}\d+)')
ndfl_patterns = re.compile(r'(?:\d.{0,2}ндфл|ндфл.{0,2}\d)')
npa_patterns = re.compile(r'\d+(?:[-/]\d+)+')
# письмо минфина № 03-03-06/1/67181

PATTERNS = nk_patterns
patterns_dict = {"DATES": (date_patterns, "дата_время"),
                 "FSBU": (fsbu_patterns, "фсбу_номер"),
                 "NK": (nk_patterns, "нк_статья"),
                 "FZ": (fz_patterns, "фз_номер"),
                 "KBK": (kbk_patterns, "кбк_номер"),
                 "FORMS": (forms_patterns, "форма_номер"),
                 "KND": (knd_patterns, "кнд_номер"),
                 "NDFL": (ndfl_patterns, "ндфл_номер"),
                 "NPA": (npa_patterns, "нпа_номер")

                 }

parsing_texts = []
for tx in tx_list:
    tx = str(tx).lower()
    d = {"text": tx}
    for i in patterns_dict:
        d[i] = re.findall(patterns_dict[i][0], tx)
        if d[i]:
            for pt in d[i]:
                print("ptrn:", pt, "mask:", patterns_dict[i][1], "text:", tx)
                tx = re.sub(pt, patterns_dict[i][1], str(tx))
    d["UNCNOWN_NUM"] = re.findall(r'\d+', tx)
    tx = re.sub(r'\d+', "цифра", str(tx))
    d["clear_text"] = tx
    parsing_texts.append(d)
"""
    if re.findall(npa_patterns, str(tx)):
        print(tx)
        print("dates:", re.findall(date_patterns, str(tx)))
        print("FSBU:", re.findall(fsbu_patterns, str(tx)))
        print("NK:", re.findall(nk_patterns, str(tx)))
        print("FZ:", re.findall(fz_patterns, str(tx)))
        print("KBK:", re.findall(kbk_patterns, str(tx)))
        print("FORMS:", re.findall(forms_patterns, str(tx)))
        print("KND:", re.findall(knd_patterns, str(tx)))
        print("NDFL:", re.findall(ndfl_patterns, str(tx)))
        print("NPA:", re.findall(npa_patterns, str(tx)))
tx = "в отчетности от 2024 года 2023 г 2021г от 6 сентября 2022 года от 8 августа 2012"
print(tx, re.findall(date_patterns, tx))"""

print(parsing_texts)
parsing_texts_df = pd.DataFrame(parsing_texts)
parsing_texts_df.to_csv("parsing_texts.csv", sep="\t", index=False)