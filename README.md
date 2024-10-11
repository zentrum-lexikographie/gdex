# quaxa - QUAlity of sentence eXAmples

_Rule-based sentence scoring algorithm based on GDEX_

This package provides a
[GDEX](https://www.sketchengine.eu/guide/gdex/)-based algorithm for
evaluating sentences with regard to their suitability as good examples
in dictionaries. It applies a numeric score between zero and one to
sentences which have been preprocessed with the NLP tool
[spaCy](https://spacy.io/). The score is computed by taking several
configurable criteria into account, firstly knock-out criteria which
have to be fulfilled in order to reach a score above zero at all, as
well as gradual criteria that factor into a score greater than zero.

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
* an optimal length of the sentence, and
* a whitelist-based coverage test, i. e. for penalizing usage of rare lemmata.

## Installation

`quaxa` can be installed as a package from its GitHub source repository:

```sh
pip install git+https://github.com/zentrum-lexikographie/quaxa.git
```

For development, clone it from GitHub and install it locally, including optional dependencies:

``` sh
pip install -e .[dev]
```

## Usage


``` python-console
>>> import spacy, quaxa
>>> nlp = spacy.load("de_core_news_sm")
>>> [s._.quaxa for s in quaxa.de_core(nlp("Achtung! Das ist ein toller Test.")).sents]
[0.0, 0.5966]
```

## Testing

Run tests, including calculation of code coverage:

``` sh
pytest --cov=quaxa
```

## Acknowledgements

This package was initially developed as part of the [EVIDENCE
project](https://gepris.dfg.de/gepris/projekt/433249742) and funded by
the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation,
GU 798/27-1; GE 1119/11-1). Between August 2023 and October 2024, it
has been maintained by [Ulf Hamster](https://github.com/ulf1/).

Quaxa makes use of [VulGer](https://aclanthology.org/W19-3513), a
lexicon covering words from the lower end of the German language
register — terms typically considered rough, vulgar, or
obscene. VulGer is used under the terms of the CC-BY-SA license.

## Bibliography

* Adam Kilgarriff, Miloš Husák, Katy McAdam, Michael Rundell and Pavel
  Rychlý. [GDEX: Automatically finding good dictionary examples in a
  corpus](http://www.sketchengine.co.uk/wp-content/uploads/2015/05/GDEX_Automatically_finding_2008.pdf).
  In Proceedings of the 13th EURALEX International Congress. Spain,
  July 2008, pp. 425–432.
* Didakowski, Jörg, Lothar Lemnitzer, and Alexander Geyken. [Automatic
  example sentence extraction for a contemporary German
  dictionary](https://euralex.org/publications/automatic-example-sentence-extraction-for-a-contemporary-german-dictionary/). Proceedings
  EURALEX. 2012.
* Elisabeth Eder, Ulrike Krieg-Holz, and Udo Hahn. 2019. [At the Lower
  End of Language—Exploring the Vulgar and Obscene Side of
  German.](https://aclanthology.org/W19-3513) In Proceedings of the
  Third Workshop on Abusive Language Online, pages 119–128, Florence,
  Italy. Association for Computational Linguistics.
