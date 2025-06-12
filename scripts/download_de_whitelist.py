#!/usr/bin/env python

import csv
import json
import urllib.request
from pathlib import Path

project_dir = Path(__file__).parent.parent.resolve()
de_vulger_file = project_dir / "gdex" / "VulGer.csv"
de_vulger_blacklist = set()
de_whitelist = set()

with urllib.request.urlopen("https://www.dwds.de/lemma/json") as f:
    lemma_database = json.load(f)

with de_vulger_file.open(encoding="utf-8") as vulger:
    for n, (word, score) in enumerate(csv.reader(vulger)):
        if n == 0:
            continue
        if float(score) > 0:
            continue
        de_vulger_blacklist.add(word)

for lemma in lemma_database:
    freq_class = lemma["freq"]
    if freq_class == "n/a":
        continue
    freq_class = int(freq_class)
    if freq_class < 2:
        continue
    lemma_form = lemma["lemma"]
    if lemma_form in de_vulger_blacklist:
        continue
    de_whitelist.add(lemma_form)

de_whitelist_file = project_dir / "gdex" / "de_whitelist.txt"
de_whitelist_file.write_text("\n".join(sorted(de_whitelist)), encoding="utf-8")
