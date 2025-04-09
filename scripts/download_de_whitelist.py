#!/usr/bin/env python

import csv
import io
import urllib.request
from pathlib import Path

project_dir = Path(__file__).parent.parent.resolve()
de_vulger_file = project_dir / "gdex" / "VulGer.csv"
de_vulger_blacklist = set()

with de_vulger_file.open(encoding="utf-8") as vulger:
    for n, (word, score) in enumerate(csv.reader(vulger)):
        if n == 0:
            continue
        if float(score) > 0:
            continue
        de_vulger_blacklist.add(word)

de_whitelist = []
with urllib.request.urlopen("https://www.dwds.de/lemma/csv") as f:
    lemmata = f.read().decode("utf-8")
    for lemma in csv.DictReader(io.StringIO(lemmata)):
        freq_class = lemma["frequenzklasse"]
        if freq_class == "n/a":
            continue
        freq_class = int(freq_class)
        if freq_class < 2:
            continue
        lemma_form = lemma["lemma"]
        if lemma_form in de_vulger_blacklist:
            continue
        de_whitelist.append(lemma_form)

de_whitelist_file = project_dir / "gdex" / "de_whitelist.txt"
de_whitelist_file.write_text("\n".join(de_whitelist))
