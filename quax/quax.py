from typing import List


def total_score(**kwargs) -> float:
    """ Rule-based sentence scoring formula

    Parameters:
    -----------
    **kwargs : Dict (named input arguments)
        txt=sent,
        dependency_tree=tree,
        headword=headword,
        lemmas=lemmas,
        xpos=xpos,
        tokens=tokens
        (what we need so far: tokens, lemmas, dependency information, STTS and
        UPOS tags)
        The called subfunctions will throw an error if something is missing

    Returns:
    --------
    float
        Score if a sentence example is suitable as dictionary example.
    """
    return .5 * isa_knockout_criteria(**kwargs) \
         + .5 * factor_gradual_criteria(**kwargs)


def isa_knockout_criteria(**kwargs):
    # read input arguments
    txt = kwargs.get('txt')
    headword = kwargs.get('headword')
    dependency_tree = kwargs.get('dependency_tree')
    lemmas = [t.get('lemma') for t in dependency_tree]
    # compute factor
    return has_finite_verb_and_subject(dependency_tree) \
         * is_misparsed(txt) \
         * has_illegal_chars(txt) \
         * has_blacklist_words(txt, headword, lemmas)


def factor_gradual_criteria(**kwargs):
    # read input arguments
    txt = kwargs.get('txt')
    headword = kwargs.get('headword')
    dependency_tree = kwargs.get('dependency_tree')
    lemmas = [t.get('lemma') for t in dependency_tree]
    num_tokens = len(dependency_tree)
    # compute factor
    return factor_graylist_rarechars(txt) \
         * factor_graylist_nongermankeyboardchars(txt) \
         * factor_graylist_words(txt, xpos) \
         * greylist_ne(txt, xpos) \
         * (
            deixis_space(txt, headword, lemmas)
            + deixis_time(txt, headword, lemmas)
            + deixis_person(txt, headword, dependency_tree)
           ) / 3. \
         * optimal_interval(num_tokens)


def has_finite_verb_and_subject(dependency_tree: List[dict]) -> bool:
    """Has finite verb as root and subject as one of its children.

    It is a knockout criterion.
    """
    # find the root of the dependency tree
    root = [token for token in dependency_tree if token['deprel'].lower() == 'root']
    assert len(root) == 1
    root = root[0]
    
    # finite verb is root
    verb_root = False
    if root['upos'] in {'AUX', 'VERB'}:
        if root['feats'].get('VerbForm', '') == 'Fin':
            verb_root = True

    # subject is one of its children
    subj_child_of_verb = False
    for child in root['children']:
        child_dict = [c for c in dependency_tree if c['text'] == child][0]
        if child_dict['upos'] in {'NOUN', 'PROPN', 'PRON'}:
            if 'subj' in child_dict['deprel']:
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

def has_blacklist_words(txt: str, headword: str, lemmas: List[str]):
    return any([l.lower() in blacklist_words and l != headword for l in lemmas])


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
             upos: List[str],
             xpos: List[str],
             greylist_pos: List[str] = ['NE', 'PROPN'],
             penalty_factor: float = 0.1):
    num_matches = len([_ for u, x in zip(upos, xpos) if (u in greylist_pos or x in greylist_pos)])
    return max(0.0, 1.0 - penalty_factor * num_matches)


DEFAULT_TIME_DEIXIS_TERMS = [
    'jetzt', 'heute', 'gestern', 'morgen', 'dann', 'damals', 'bald',
    'kürzlich']

DEFAULT_SPACE_DEIXIS_TERMS = [
    'hier', 'dort', 'über', 'da', 'vor', 'hinter', 'links', 'von', 'rechts',
    'von', 'oben', 'unten']


def _deixis(headword: str, 
            lemmas: List[str], 
            deixis_terms: List[str],
            penalty_factor: float = 0.1):
    """Deixis factor"""
    cnt = len([l for l in lemmas if l != headword and l in deixis_terms])
    return max(0.0, 1.0 - penalty_factor * cnt)


def deixis_space(headword: str, 
                 lemmas: List[str],
                 space_deixis_terms: List[str] = DEFAULT_SPACE_DEIXIS_TERMS,
                 penalty_factor: float = 0.1) -> float:
    """Space deixis factor"""
    return _deixis(headword=headword, 
                   lemmas=lemmas, 
                   deixis_terms=space_deixis_terms,
                   penalty_factor=penalty_factor)


def deixis_time(headword: str, 
                lemmas: List[str],
                time_deixis_terms: List[str] = DEFAULT_TIME_DEIXIS_TERMS,
                penalty_factor: float = 0.1) -> float:
    """Time deixis factor"""
    return _deixis(headword=headword, 
                   lemmas=lemmas, 
                   deixis_terms=time_deixis_terms,
                   penalty_factor=penalty_factor)


def deixis_person(headword: str, 
                  dependency_tree: List[dict],
                  penalty_factor: float = 0.1) -> float:
    """Count personal deixis

    We use UD's PronType=Prs as criteron. It includes personal pronouns,
    but also possessive personal pronoun, e.g. "seiner"
    
    see https://universaldependencies.org/en/feat/PronType.html
    """
    cnt = len([
        t for t in dependency_tree 
        if t.get('feats', {}).get('PronType', '') == 'Prs'
        and t['lemma'] != headword])
    return max(0.0, 1.0 - penalty_factor * cnt)


def optimal_interval(num_tokens: int, low: int=10, high: int=20):
    """Optimal sentence length by the number of word tokens"""
    if low <= num_tokens <= high:
        return 1.
    elif num_tokens < low:
        if num_tokens < low / 2.:
            return 0.
        else:
            diff = low - num_tokens
            return 1 - diff * (1. / (low / 2.))
    else:
        if num_tokens > (2 * high):
            return 0.
        diff = (2 * high) - num_tokens
        return diff / high

