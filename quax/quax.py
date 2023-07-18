import random
from typing import List

import conllu
from spacy_conll import init_parser

random.seed(42)

def total_score(**kwargs) -> float:
    """ Rule-based sentence scoring formula

    Parameters:
    -----------
    **kwargs : Dict (named input arguments)
        txt=sent,
        dependency_tree=tree,
        lemma=lemma,
        lemmata=lemmata,
        xpos=xpos,
        tokens=tokens
        (what we need so far: tokens, lemmata, dependency information, STTS and
        UPOS tags)
        The called subfunctions will throw an error if something is missing

    Returns:
    --------
    float
        Score if a sentence example is suitable as dictionary example.


    """
    return .5 * factor_knockout_criteria(**kwargs) \
         + .5 * factor_gradual_criteria(**kwargs)

def factor_knockout_criteria(**kwargs):
    dependency_tree = kwargs.get('dependency_tree')
    txt = kwargs.get('txt')
    return is_whole_sentence(txt, dependency_tree) \
         * is_misparsed(txt) \
         * has_illegal_chars(txt) \
         * has_blacklist_words(txt, lemma, lemmata)


def factor_gradual_criteria(**kwargs):
    txt = kwargs.get('txt')
    return factor_graylist_rarechars(txt) \
         * factor_graylist_nongermankeyboardchars(txt) \
         * factor_graylist_words(txt, xpos) \
         * greylist_ne(txt, xpos) \
         * (ortsdeixis(txt, lemma, lemmata)
         + zeitdeixis(txt, lemma, lemmata)
         + personendeixis(txt, lemma, lemmata, xpos)) / 3. \
         * optimal_interval(tokens)


def is_whole_sentence(txt: str, dependency_tree: List[dict]):
    root = [token for token in dependency_tree if token['dep'].lower() == 'root']
    assert len(root) == 1
    root = root[0]
    # finite verb is root and subject is one of its children
    verb_root = False
    if root['pos'] in {'AUX', 'VERB'} and root['tag'].endswith('FIN'):
        verb_root = True
    subj_child_of_verb = False
    for child in root['children']:
        child_dict = [c for c in dependency_tree if c['text'] == child][0]
        if child_dict['pos'] in {'NOUN', 'PROPN', 'PRON'}:
            # subj for conll, sb for spacy
            if 'subj' in child_dict['dep'] or 'sb' in child_dict['dep']:
                subj_child_of_verb = True
    return (verb_root and subj_child_of_verb)


def is_misparsed(txt: str):
    conditions = [txt[0].islower(),
                  txt[0].isspace(),
                  txt[0] in ',.?!()/&%-_:;#+*~<>|^°',
                  txt[-1] not in '?!.']
    return any(conditions)


def has_illegal_chars(txt: str, illegal_chars = '<|][>/\^@\a\b\e\E\f\n\r\v\t'):
  return any([s in illegal_chars for s in txt])


blacklist_words = ['negroid',
 'Zigeunerbande',
 'Mischling',
 'Zigeunerleben',
 'Zigeunerkind',
 'durchvögeln',
 'durchficken',
 'durchbumsen',
 'Idiot',
 'Polenböller',
 'geisteskrank',
 'Neger',
 'Zigeuner',
 'Nigger',
 'Schwuchtel',
 'Herrenrasse',
 'Negersklave',
 'Negerin',
 'Negerblut',
 'Negerkind',
 'Negerstamm']

def has_blacklist_words(txt: str, lemma: str, lemmata: List[str]):
    return any([l.lower() in blacklist_words and l != lemma for l in lemmata])


def factor_graylist_rarechars(txt: str,
                              rare_chars="0123456789'.,!?)(;:-",
                              penalty_factor: float = 0.1):
    num_matches = len([s for s in txt if s in rare_chars])
    return max(0.0, 1.0 - penalty_factor * num_matches)


qwertz_de = [
        '^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ß', "'",
        'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ü', '+',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', '#',
        '<', 'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-',
        '°', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', '`',
        'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'Ü', '*',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', "'",
        '>', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_',
        '′', '¹', '²', '³', '¼', '½', '¬', '{', '[', ']', '}', '\\', '¸',
        '@', 'ł', '€', '¶', 'ŧ', '←', '↓', '→', 'ø', 'þ', '"', '~',
        'æ', 'ſ', 'ð', 'đ', 'ŋ', 'ħ', '̣', 'ĸ', 'ł', '˝', '^', '’',
        '|', '»', '«', '¢', '„', '“', '”', 'µ', '·', '…', '–',
        '″', '¡', '⅛', '£', '¤', '⅜', '⅝', '⅞', '™', '±', '°', '¿', '˛',
        'Ω', 'Ł', '€', '®', 'Ŧ', '¥', '↑', 'ı', 'Ø', 'Þ', '°', '¯',
        'Æ', 'ẞ', 'Ð', 'ª', 'Ŋ', 'Ħ', '˙', '&', 'Ł', '̣', '̣', '˘',
        '', '›', '‹', '©', '‚', '‘', '’', 'º', '×', '÷', '—'
    ]

ords = sorted([ord(c) for c in qwertz_de if c])

def factor_graylist_nongermankeyboardchars(txt: str, eligible: List=ords):
    """Computes the percentage of characters not typable on a German keyboard."""
    return len([_ for c in txt if ord(c) in eligible])/len(txt)


greylist_pos = {'PPER', 'PIS'}
# irreflexives Personalpronomen, subst. Indefinitpron.
# https://homepage.ruhr-uni-bochum.de/Stephen.Berman/Korpuslinguistik/Tagsets-STTS.html

def factor_graylist_words(txt: str,
                          xpos: List[str],
                          penalty_factor: float = 0.1):
    num_matches = len([p for p in xpos if p in greylist_pos])
    return max(0.0, 1.0 - penalty_factor * num_matches)


def greylist_ne(txt: str,
             xpos: List[str],
             greylist_pos: List[str] = ['NE'],
             penalty_factor: float = 0.1):
    num_matches = len([p for p in xpos if p in greylist_pos])
    return max(0.0, 1.0 - penalty_factor * num_matches)


tempdeixis = ['jetzt', 'heute', 'gestern', 'morgen', 'dann', 'damals', 'bald', 'kürzlich']
localdeixis = ['hier', 'dort', 'über', 'da', 'vor', 'hinter', 'links', 'von', 'rechts',
  'von', 'oben', 'unten']

def deixis(txt: str, lemma: str, lemmata: List[str], deixis_terms: List[str]):
  return len([l for l in lemmata if l != lemma and l in deixis_terms])

def ortsdeixis(txt: str, lemma: str, lemmata: List[str]):
    return deixis(txt, lemma, lemmata, localdeixis)

def zeitdeixis(txt: str, lemma: str, lemmata: List[str]):
    return deixis(txt, lemma, lemmata, tempdeixis)

def personendeixis(txt:str, lemma: str, lemmata: List[str], xpos: List[str]):
    return len([p for i, p in enumerate(xpos) if p == 'PPER'
    and not lemmata[i] == lemma])


def optimal_interval(txt: str, low: int=10, high: int=20):
    if isinstance(txt, (list, tuple)):
        tokens = txt
    else:
        tokens = txt.split()
    if low <= len(tokens) <= high:
        return 1.
    elif len(tokens) < low:
        if len(tokens) < low/2:
            return 0.
        else:
            diff = low - len(tokens)
            return 1 - diff * (1 / (low/2))
    else:
        if len(tokens) > (2*high):
            return 0.
        diff = (2*high) - len(tokens)
        return diff / high

