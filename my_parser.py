import re
import os
import time
import pandas as pd


# рубли https://docs.google.com/spreadsheets/d/1uVllieSyjvu2ElubsFQTBGr_9RtHZVzFOEaGHjog0XU/edit#gid=0

class TextParser:
    def __init__(self, patterns):
        self.patterns = patterns

    def text_parser(self, tx) -> {}:
        """функция парсит входящий текст, извлекая из него паттерны из patterns"""
        tx = str(tx).lower()
        d = {"text": tx}
        for type in self.patterns:
            d[type] = [re.sub(r'[^\d\w\s,.\-/\\]', "", t) for t in re.findall(self.patterns[type]["pattern"], str(tx))]
            if self.patterns[type]["use_mask"]:
                if d[type]:
                    for pt in d[type]:
                        tx = re.sub(pt, self.patterns[type]["mask"], str(tx))
        d["clear_text"] = tx
        return d

    def __call__(self, tx):
        return self.text_parser(tx)


df = pd.read_csv(os.path.join("data", "NUMERIC_FILTR.csv"), sep="\t")
tx_list = [re.sub(r'[^\d\w\s.,]', " ", str(tx)) for tx in list(df["Text"])]

date_patterns = re.compile(r'\d{2}\.\d{2}.\d{4}|\d{4}\.\d{2}.\d{2}|\d{4}\s{0,3}г|'
                           r'(?:янв\w+|фев\w+|мар\w+|апр\w+|мая\w+|июн\w+|июл\w+|авг\w+|сен\w+|окт\w+'
                           r'|ноя\w+|дек\w+)\s{0,3}\d{4}|\d\s{0,3}кв\w+\s+\d{4}|\d\s{0,3}кв.{0,3}\d{4}')

fsbu_patterns = re.compile(r'фсбу\s*\d+(?:\/|\-)\d+|\d+(?:\/|\-)\d+\s*фсбу')

nk_patterns = re.compile(r'(?:\bнк.{0,1}\b.+\bст|\bст.{0,1}\b.+\bнк|\bпп.{0,1}'
                         r'\b.+\bп[\.\s]{0,1}\b.+\bст.{0,1}\b.+\bнк|'
                         r'\bп[\.\s]{0,1}\b.+\bст.{0,1}\b.+\bнк)')

fz_patterns = re.compile(r'(?:\d+.{0,2}фз|фз.{0,2}\d+)')
kbk_patterns = re.compile(r'(?:\d+.{0,3}кбк|кбк.{0,3}\d+)')
forms_patterns = re.compile(r'(?:\d+.{0,2}\bформ\w+|\bформ\w+.{0,2}\d+|\bформ\w+.{0,2}\w+[-/\\\s+]\d+|'
                            r'\b\w+[-/\\\s+]\d+.{0,2}\bформ)')
knd_patterns = re.compile(r'(?:\d+.{0,2}кнд|кнд.{0,2}\d+)')
ndfl_patterns = re.compile(r'(?:\d\b.{0,2}ндфл|ндфл.{0,2}\d\b)')
npa_patterns = re.compile(r'\d+(?:[-/]\d+)+')
money_patterns = re.compile(r'(?:\d{1,10}(?:|[,.\s])\d{1,10})+(?:|\s+)(?:м[лнрдионад]{0,7}'
                            r'\b(?:|[\s.,])р[убляей]{0,7}\b|т[ысячи]{0,7}\b(?:|[\s.,])р[убляей]{0,7}'
                            r'\b|р[убляей]{0,7}\b(?:|[\s.,]))')
uncknow_num_patterns = re.compile(r'(?:\w+[\/-]\d+|\d+[\/-]\w+|\d+)')

keys_df = pd.read_csv(os.path.join("data", "keywords.csv"), sep="\t")
keys_patterns = re.compile("|".join(list(keys_df["keys"])))

patterns_dict = {"DATES": {"pattern": date_patterns, "mask": "genдата", "use_mask": True},
                 "FSBU": {"pattern": fsbu_patterns, "mask": "genфсбу", "use_mask": True},
                 "NK": {"pattern": nk_patterns, "mask": "genнкстатья", "use_mask": True},
                 "FZ": {"pattern": fz_patterns, "mask": "genфз", "use_mask": True},
                 "KBK": {"pattern": kbk_patterns, "mask": "genкбк", "use_mask": True},
                 "FORMS": {"pattern": forms_patterns, "mask": "genформа", "use_mask": True},
                 "KND": {"pattern": knd_patterns, "mask": "genкнд", "use_mask": True},
                 "NDFL": {"pattern": ndfl_patterns, "mask": "genндфл", "use_mask": True},
                 "NPA": {"pattern": npa_patterns, "mask": "genнпа", "use_mask": True},
                 "MONEY": {"pattern": money_patterns, "mask": "genденьги", "use_mask": True},
                 "UNCNOWN_NUM": {"pattern": uncknow_num_patterns, "mask": "genцифра", "use_mask": True},
                 "KEYS": {"pattern": keys_patterns, "mask": "genключевик", "use_mask": False}
                 }


parser = TextParser(patterns_dict)