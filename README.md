# GDEX

_Good Dictionary Examples – Rule-based Sentence Scoring Algorithm_

[![DOI](https://zenodo.org/badge/894010183.svg)](https://doi.org/10.5281/zenodo.15735626)

This Python package provides a
[GDEX](https://www.sketchengine.eu/guide/gdex/)-based algorithm for
evaluating sentences with regard to their suitability as good examples
in dictionaries. It applies a numeric score between zero and one to
sentences which have been preprocessed with the NLP tool
[spaCy](https://spacy.io/). The score is computed by taking several
configurable criteria into account, firstly knock-out criteria which
have to be fulfilled in order to reach a score above 0.5, as well as
gradual criteria that factor into a score.

Among the knock-out criteria are

* the character set of a sentence not containing any invalid ones (i. e. control characters),
* properly parsed sentences with punctuation at the end, and
* the existence of a finite verb and a subject, annotated and related
  in a sentence's dependency parse tree.

Among the gradual criteria are

* the absence of blacklisted words (i. e. vulgar or obscene),
* the absence of rare characters or those normally not available on a keyboard,
* the absence of named entities,
* the absence of deictic expressions,
* an optimal length of the sentence,
* a whitelist-based coverage test, i. e. for penalizing usage of rare lemmata, and
* the absence of subordinate clauses / the headword being part of a main clause.

## Installation

`gdex` can be installed as a package from its GitHub source repository:

```sh
pip install git+https://github.com/zentrum-lexikographie/gdex.git@v1.4.1
```

For development, clone it from GitHub and install it locally, including optional dependencies:

``` sh
pip install -e .[dev]
```

## Usage


``` python-console
>>> import zdl_spacy
>>> import gdex
>>> nlp = zdl_spacy.load()
>>> [s._.gdex for s in gdex.de_hdt(nlp("Achtung! Das ist ein toller Test.")).sents]
[0.0, 0.5968749999999999]
```

## Testing

Run tests, including calculation of code coverage:

``` sh
coverage run -m pytest
```

## Acknowledgements

This package was initially developed as part of the [EVIDENCE
project](https://gepris.dfg.de/gepris/projekt/433249742) and funded by
the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation,
GU 798/27-1; GE 1119/11-1). Between August 2023 and October 2024, it
has been maintained by [Ulf Hamster](https://github.com/ulf1/).

This implementation makes use of [VulGer](https://aclanthology.org/W19-3513),
a lexicon covering words from the lower end of the German language
register — terms typically considered rough, vulgar, or
obscene. VulGer is used under the terms of the CC-BY-SA license.

## Bibliography

* Rychlý, Pavel, Miloš Husák, Adam Kilgarriff, Michael Rundell, und Katy McAdam. GDEX: Automatically Finding Good Dictionary Examples in a Corpus. Institut Universitari de Lingüística Aplicada, 2008. https://is.muni.cz/publication/772821/en/GDEX-Automatically-finding-good-dictionary-examples-in-a-corpus/Rychly-Husak-Kilgarriff-Rundell.
* Didakowski, Jörg, Lothar Lemnitzer, und Alexander Geyken. „Automatic Example Sentence Extraction for a Contemporary German Dictionary“, 343–49, 2012. https://euralex.org/publications/automatic-example-sentence-extraction-for-a-contemporary-german-dictionary/.
* Eder, Elisabeth, Ulrike Krieg-Holz, und Udo Hahn. „At the Lower End of Language—Exploring the Vulgar and Obscene Side of German“. In Proceedings of the Third Workshop on Abusive Language Online, herausgegeben von Sarah T. Roberts, Joel Tetreault, Vinodkumar Prabhakaran, und Zeerak Waseem, 119–28. Florence, Italy: Association for Computational Linguistics, 2019. https://doi.org/10.18653/v1/W19-3513.
