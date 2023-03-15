import re
import os
import pandas as pd

df = pd.read_csv(os.path.join("data", "NUMERIC_FILTR.csv"), sep="\t")
tx_list = list(df["Text"])

date_patterns = re.compile(r'\d{2}\.\d{2}.\d{4}|\d{4}\.\d{2}.\d{2}|\d{4}\s{0,3}г|'
                           r'(?:янв\w+|фев\w+|мар\w+|апр\w+|мая\w+|июн\w+|июл\w+|авг\w+|сен\w+|окт\w+'
                           r'|ноя\w+|дек\w+)\s{0,3}\d{4}|\d\s{0,3}кв\w+\s+\d{4}|\d\s{0,3}кв.{0,3}\d{4}', re.I)

fsbu_patterns = re.compile(r'фсбу\s*\d+(?:\/|\-)\d+|\d+(?:\/|\-)\d+\s*фсбу', re.I)

nk_patterns = re.compile(r'(?:\bнк.{0,1}\b.+\bст|\bст.{0,1}\b.+\bнк|\bпп.{0,1}\b.+\bп.{0,1}\b.+\bст.{0,1}\b.+\bнк|'
                         r'\bп.{0,1}\b.+\bст.{0,1}\b.+\bнк)', re.I)

fz_patterns = re.compile(r'(?:\d+.{0,2}фз|фз.{0,2}\d+)', re.I)
kbk_patterns = re.compile(r'(?:\d+.{0,2}кбк|кбк.{0,2}\d+)', re.I)
forms_patterns = re.compile(r'(?:\d+.{0,2}форм\w+|форм\w+.{0,2}\d+)', re.I)
knd_patterns = re.compile(r'(?:\d+.{0,2}кнд|кнд.{0,2}\d+)', re.I)
ndfl_patterns = re.compile(r'(?:\d.{0,2}ндфл|ндфл.{0,2}\d)', re.I)
npa_patterns = re.compile(r'\d+(?:[-/]\d+)+', re.I)
# письмо минфина № 03-03-06/1/67181

PATTERNS = nk_patterns

for tx in tx_list:
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
    # if re.findall(PATTERNS, str(tx)):
    #   print(tx, re.findall(PATTERNS, str(tx)))

tx = "в отчетности от 2024 года 2023 г 2021г от 6 сентября 2022 года от 8 августа 2012"
print(tx, re.findall(date_patterns, tx))
