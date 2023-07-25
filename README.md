[![PyPI version](https://badge.fury.io/py/quaxa.svg)](https://badge.fury.io/py/quaxa)
[![PyPi downloads](https://img.shields.io/pypi/dm/quaxa)](https://img.shields.io/pypi/dm/quaxa)

# QUAXA: QUAlity of sentence eXAmples scoring
Rule-based sentence scoring algorithm based on GDEX.


## Rules

### Formel

```
score = 0.5 * isnoknockout + 0.5 * gesamtfaktor
```

### Knock-out Kritieren
Wenn 1 Knock-out Kriterium identifiziert wird, dann wird direkt der Score direkt um 0.5 (von 1.0) gesenkt.

| Funktion | Ausgabe | Beschreibung | Hinweis |
|:---:|:---:|:---|:---|
| `has_finite_verb_and_subject` | bool | Der Satz hat ein finites Verb und ein Subjekt, wovon eines Root des Dependenzbaum ist oder via beide über Root Node verknüpft sind. | [1] GDEX whole sentence |
| `is_misparsed` | bool | Das 1. Zeichen des Strings ist kleingeschrieben, ein Leerzeichen oder eine Punktuation; oder das letzte Zeichen ist keine Punktuation. | [1] GDEX whole sentence |
| `has_illegal_chars` | bool | String enhält Kontrolzeichen (ASCII 0-31), oder die Zeichen `<>|[]/\^@'` (z.B. HTML Tags, Markdown Hyperlinks, Dateipfade, E-Mail, u.a.) | [1] GDEX illegal chars |
| `has_blacklist_words` | bool | Satzbeleg enthält Wörter, sodass in keinem Fall der Satzbeleg als Wörterbuchbeispiel in Betracht gezogen wird; ausgenommen das Blacklist-Wort ist selbt der Wörterbucheintrag. (dt. Blacklist ist voreingestellt) | [1] GDEX blacklist |

### Diskontierungsfakoren
Je Kriterium wird ein Faktor berechnet, und alle Faktoren miteinander multipliziert. 
Wenn bspw. ein Faktor eine Penality von 0.1 bekommt, dann ist der Faktor 0.9.
Für den Gesamtscore wird der Gesamtfaktor mit 0.5 multipliziert.

| Funktion | Ausgabe | Beschreibung | Hinweis |
|:---:|:---:|:---|:---|
| `factor_rarechars` | [0.0, 1.0] | Strafe für jedes Zeichen, was `0123456789\'.,!?)(;:-` ist (Zahlen bzw. lange Zahlen; `.` für Abk.; mehrere Punktuationen; Bindestrichwörter, u.a.) | [1] GDEX rare chars |
| `factor_notkeyboardchar` | [0.0, 1.0] | Der Prozentsatz der Zeichen, die mit einem deutsche Tastaturlayout getippt werden können. | n.a. |
| `factor_graylist_words` | [0.0, 1.0] | Strafe Satzbelege ab, wenn Lemma auf einer Graylist steht; ausgenommen das Graylist-Wort ist selbt der Wörterbucheintrag. (Default: Keine Graylist voreingestellt) | [1] GDEX greylist |
| `factor_named_entity` | [1.0 - penalty, 1.0] | Strafe Satzbeleg ab, wenn Lemma ein o. Teil eines Eigennamen ist | [1] GDEX upper case (rare chars), [2] GBEX NE |
| `deixis_time` | [0.0, 1.0] | Strafe Signalwörter für Temporaldeixis ab. | [2] GBEX Dexis; [3] |
| `deixis_space` | [0.0, 1.0] | Strafe Signalwörter für Lokaldeixis ab. | [2] GBEX Dexis; [3] |
| `deixis_person` | [0.0, 1.0] | Strafe Wörter mit `UPOS=PRON` und `PronType=Prs|Dem|Ind|Neg|Tot` ab. Entspricht STTS PoS-Tags `PDS` (`PRON` + `Dem`, z.B, das, dies, die, diese, der), `PIS` (`PRON` + `Ind|Neg|Tot`, z.B, man, allem, nichts, alles, mehr), `PPER` (`PRON` + `Prs`, z.B, es, sie, er, wir, ich), `PPOSS` (`PRON` + `Prs`, z.B, ihren, Seinen, seinem, unsrigen, meiner). | [1] GDEX graylist PoS- Tags, [2] GBEX Dexis; [3], [4] |
| `optimal_interval` | [0.0, 1.0] | Strafe Satzbelege mit zu wenigen/vielen Wörter ab ab. | [1] GDEX |


Quellen:
- [1] Lexical Computing, "GDEX configuration introduction", URL: https://www.sketchengine.eu/syntax-of-gdex-configuration-files/
- [2] Didakowski, Lemnitzer, Geyken, 2012, "Automatic example sentence ex- traction for a contemporary German dictionary", URL: https://euralex.org/publications/automatic-example-sentence-extraction-for-a-contemporary-german-dictionary/
- [3] LingTermNet, URL: https://gsw.phil-fak.uni-duesseldorf.de/diskurslinguistik/index.php?title=Deiktischer_Ausdruck
- [4] Universial Dependency, UPOS-STTS conversion table, URL: https://universaldependencies.org/tagset-conversion/de-stts-uposf.html


## Appendix

### Installation
The `quaxa` [git repo](http://github.com/ulf1/quaxa) is available as [PyPi package](https://pypi.org/project/quaxa)

```sh
pip install quaxa
pip install git+ssh://git@github.com/ulf1/quaxa.git
```

### Install a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. python -m unittest`

Publish

```sh
python setup.py sdist 
twine upload -r pypi dist/*
```

### Clean up 

```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### Support
Please [open an issue](https://github.com/ulf1/quaxa/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/quaxa/compare/).


### Acknowledgements
The "Evidence" project was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - [433249742](https://gepris.dfg.de/gepris/projekt/433249742) (GU 798/27-1; GE 1119/11-1).

### Maintenance
- till 31.Aug.2023 (v0.1.0) the code repository was maintained within the DFG project [433249742](https://gepris.dfg.de/gepris/projekt/433249742)
- since 01.Sep.2023 (v0.1.0) the code repository is maintained by Ulf Hamster.