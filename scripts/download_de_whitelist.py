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
# add other (mis)spellings or forms, for example "deppat" and "Looser",
# based on "deppert" and "Loser", respectively;
# unless: new form + 'e' = original form (i.e., not "blöd" based on "blöde")
for entry in lemma_database:
    lemma = entry["lemma"]
    if lemma in de_vulger_blacklist and "other_lemmata" in entry:
        for related_lemma in entry["other_lemmata"]:
            if related_lemma not in de_vulger_blacklist:
                if not (lemma.endswith("e") and related_lemma == lemma[:-1]):
                    de_vulger_blacklist.add(related_lemma)

for entry in lemma_database:
    freq_class = entry["freq"]
    if freq_class == "n/a":
        continue
    freq_class = int(freq_class)
    if freq_class < 2:
        continue
    lemma = entry["lemma"]
    if lemma in de_vulger_blacklist:
        continue
    de_whitelist.add(lemma)

de_whitelist_file = project_dir / "gdex" / "de_whitelist.txt"
de_whitelist_file.write_text("\n".join(sorted(de_whitelist)) + "\n", encoding="utf-8")
