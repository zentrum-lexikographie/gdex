from typing import List


def total_score(**kwargs) -> float:
    """ Rule-based sentence scoring formula

    Parameters:
    -----------
    **kwargs : Dict (named input arguments)
        txt=sent,
        annotation=tree,
        headword=headword,
        [others ...]

    Returns:
    --------
    float
        Score if a sentence example is suitable as dictionary example.
    """
    score = .5 * isa_knockout_criteria(**kwargs)
    score += .5 * factor_gradual_criteria(**kwargs)
    return score


def isa_knockout_criteria(**kwargs):
    # read input arguments
    headword = kwargs.get('headword')
    txt = kwargs.get('txt')
    annotation = kwargs.get('annotation')
    blacklist = kwargs.get('blacklist')  # optional
    # prepare variables
    lemmas = [t.get('lemma') for t in annotation]
    # compute factor
    if not has_finite_verb_and_subject(annotation):
        return False
    if is_misparsed(txt):
        return False
    if has_illegal_chars(txt):
        return False
    if has_blacklist_words(headword, lemmas, blacklist_words=blacklist):
        return False
    return True


def factor_gradual_criteria(**kwargs):
    # read input arguments
    headword = kwargs.get('headword')
    txt = kwargs.get('txt')
    annotation = kwargs.get('annotation')
    graylist = kwargs.get('graylist')  # optional
    # prepare variables
    lemmas = [t.get('lemma') for t in annotation]
    num_tokens = len(annotation)
    # penalties
    penalty_rarechars = kwargs.get('penalty_rarechars', 0.125)
    penalty_notkeyboardchar = kwargs.get('penalty_notkeyboardchar', True)
    penalty_graylist_words = kwargs.get('penalty_graylist_words', 0.075)
    penalty_named_entity = kwargs.get('penalty_named_entity', 0.1667)
    penalty_interval = kwargs.get('penalty_interval', True)
    optimal_interval_low = kwargs.get('optimal_interval_low', 10)
    optimal_interval_high = kwargs.get('optimal_interval_high', 20)
    penalty_space_deixis = kwargs.get('penalty_space_deixis', 0.034)
    penalty_time_deixis = kwargs.get('penalty_time_deixis', 0.034)
    penalty_person_deixis = kwargs.get('penalty_person_deixis', 0.034)
    # compute factor
    factor = 1.0
    if penalty_rarechars >= 0.0:
        factor *= factor_rarechars(txt, penalty_factor=penalty_rarechars)
    if penalty_notkeyboardchar:
        factor *= factor_notkeyboardchar(txt)
    if penalty_graylist_words >= 0.0:
        factor *= factor_graylist_words(
            headword, lemmas, graylist, penalty_factor=penalty_graylist_words)
    if penalty_named_entity >= 0.0:
        factor *= factor_named_entity(
            headword, annotation, penalty_factor=penalty_named_entity)
    if penalty_interval:
        factor *= optimal_interval(
            num_tokens, low=optimal_interval_low, high=optimal_interval_high)
    if penalty_space_deixis >= 0.0:
        factor *= deixis_space(
            headword, lemmas, penalty_factor=penalty_space_deixis)
    if penalty_time_deixis >= 0.0:
        factor *= deixis_time(
            headword, lemmas, penalty_factor=penalty_time_deixis)
    if penalty_person_deixis >= 0.0:
        factor *= deixis_person(
            headword, annotation, penalty_factor=penalty_person_deixis)
    # done
    return factor


def has_finite_verb_and_subject(annotation: List[dict]) -> bool:
    """Has finite verb as root and subject as one of its children.

    It is a knockout criterion.
    """
    # find the root of the dependency tree
    root = [token for token in annotation if token['deprel'].lower() == 'root']
    assert len(root) == 1
    root = root[0]
    root_id = root['id']

    # find finite verb
    def is_finite_verb(tok):
        if tok.get('upos', '') in {'AUX', 'VERB'}:
            flag = tok.get('feats', '').get('VerbForm', '') == 'Fin'
            return flag or tok.get('xpos', '').endswith('FIN')
        return False
    # find finite verb that are a) root, or b) child of root
    verb = [
        tok for tok in annotation
        if is_finite_verb(tok) and (
            tok['id'] == root_id or tok.get('head', '') == root_id)
    ]
    if len(verb) == 0:
        return False

    # find subject that are a) root, or b) child of root
    subj = [
        tok for tok in annotation
        if (tok['upos'] in {'NOUN', 'PROPN', 'PRON'}) and (
            tok['id'] == root_id or tok.get('head', '') == root_id)
    ]
    if len(subj) == 0:
        return False
    # done
    return True


def is_misparsed(txt: str):
    """Misparsed strings

    Rules:
    ------
    - The first character is lowercase
    - The first character is a whitespace
    - The first character is a punctuation mark
    - The last character is not a punctuation mark

    Parameters:
    -----------
    txt : str
        The sentence as plain text

    Returns:
    --------
    flag : bool
        True if the sentence is misparsed
    """
    conditions = [
        txt[0].islower(),
        txt[0].isspace(),
        txt[0] in ',.?!()/&%-_:;#+*~<>|^°',
        txt[-1] not in '?!.'
    ]
    return any(conditions)


def has_illegal_chars(txt: str, illegal_chars='<>|[]/\\^@'):
    """Blacklist of illegal characters

    Rules:
    ------
    - ASCII/Unicode control characters, ID 0-31
    - `<>/`  XML/HTML tags
    - `|`    pipe symbol or OR operator
    - `[]`   square brackets, e.g. Markdown links
    - slash  escape characters, Windows paths
    - `@`    email addresses
    - caret  regular expressions
    - ...

    Parameters:
    -----------
    txt : str
        The sentence as plain text

    illegal_chars : str (Default)
        The list of illegal characters

    Returns:
    --------
    flag : bool
        True if the sentence contains illegal characters
    """
    # any ASCII/Unicode control characers, e.g. newline \n
    if len([c for c in txt if ord(c) < 32]) > 0:  # 0 =< ord(c) =< 31
        return True
    # other illegal characters
    return len([c for c in txt if c in illegal_chars]) > 0


BLACKLIST_WORDS_DE = [
    'negroid',
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
    'Negerstamm'
]


def has_blacklist_words(headword: str,
                        lemmas: List[str],
                        blacklist_words: List[str] = BLACKLIST_WORDS_DE):
    if blacklist_words is None:
        blacklist_words = BLACKLIST_WORDS_DE
    a = set(lemmas)
    b = set([w for w in blacklist_words if w != headword])
    return len(a.intersection(b)) > 0


RARE_CHARS_DE = '0123456789\'.,!?)(;:-'

ORD_RARE_CHARS_DE = [ord(c) for c in RARE_CHARS_DE]


def factor_rarechars(txt: str,
                     rare_chars: List[int] = ORD_RARE_CHARS_DE,
                     penalty_factor: float = 0.1):
    """Penalize rare characters

    Parameters:
    -----------
    txt : str
        The sentence as plain text

    rare_chars : List (Default ORD_RARE_CHARS_DE)
        List of characters. Use the ASCII/Unicode IDs, see `ord(c)`

    Returns:
    --------
    factor : float
        Number between 0.0 and 1.0
    """
    num_matches = len([c for c in txt if ord(c) in rare_chars])
    return max(0.0, 1.0 - penalty_factor * num_matches)


QWERTZ_DE = [
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
    '', '›', '‹', '©', '‚', '‘', '’', 'º', '×', '÷', '—',
    ' '
]

ORDS_QWERTZ_DE = sorted([ord(c) for c in QWERTZ_DE if c])


def factor_notkeyboardchar(
        txt: str, eligible: List[int] = ORDS_QWERTZ_DE):
    """Computes the percentage of characters not typable on a German keyboard.

    Parameters:
    -----------
    txt : str
        The sentence to evaluate

    eligible : List[int] (Default ORDS_QWERTZ_DE)
        The list of eligible characters (ordinals) that are typable on a
        German keyboard. Use the ASCII/Unicode IDs, see `ord(c)`

    Returns:
    --------
    factor : float
        Percentage of characters that are typable on a German keyboard.
    """
    return len([c for c in txt if ord(c) in eligible]) / len(txt)


def factor_graylist_words(headword: str,
                          lemmas: List[str],
                          graylist_words: List[str],
                          penalty_factor: float = 0.1):
    """Penalize graylist words"""
    if graylist_words is None:
        return 1.0   # no default list
    num_matches = len([
        lem for lem in lemmas
        if lem != headword and lem in graylist_words])
    return max(0.0, 1.0 - penalty_factor * num_matches)


def factor_named_entity(headword: str,
                        annotation: List[dict],
                        penalty_factor: float = 0.15):
    """Named Enity / Proper Noun penality

    If the headword is a named entity, we want to avoid that the sentence.

    UPOS=PROPN
    see https://universaldependencies.org/u/pos/PROPN.html

    XPOS=NE
    https://universaldependencies.org/tagset-conversion/de-stts-uposf.html

    Parameters:
    -----------
    headword : str
        The headword (lemma) to evaluate in combination with the sentence.

    annotation : List[dict]
        The linguistic annoations of the sentence

    penality_factor : float (Default 0.15)
        The penality factor for each named entity occurence

    Returns:
    --------
    factors : float
        Number between 0.0 and 1.0
    """
    num_matches = 0
    for tok in annotation:
        if tok.get('lemma', '') == headword:
            if (tok.get('upos', '') == 'PROPN') or (tok.get('xpos') == 'NE'):
                num_matches += 1
    return max(0.0, 1.0 - penalty_factor * num_matches)


def _deixis(headword: str,
            lemmas: List[str],
            deixis_terms: List[str],
            penalty_factor: float = 0.1):
    """Deixis factor function

    Utility function used for deixis_space and deixis_time.
    """
    num_matches = len([
        lem for lem in lemmas
        if lem != headword and lem in deixis_terms])
    return max(0.0, 1.0 - penalty_factor * num_matches)


DEFAULT_SPACE_DEIXIS_TERMS = [
    'hier', 'dort', 'über', 'da', 'vor', 'hinter', 'links', 'von', 'rechts',
    'von', 'oben', 'unten']


def deixis_space(headword: str,
                 lemmas: List[str],
                 space_deixis_terms: List[str] = DEFAULT_SPACE_DEIXIS_TERMS,
                 penalty_factor: float = 0.1) -> float:
    """Space deixis penality

    Parameters:
    -----------
    headword : str
        The headword (lemma) to evaluate in combination with the sentence.
        The headword is excluded from the count.

    lemmas : List[str]
        All lemmas of the sentence

    space_deixis_terms : List[str] (Default DEFAULT_SPACE_DEIXIS_TERMS)
        The space deixis terms to look for in the sentence

    penalty_factor : float (Default 0.1)
        The penality factor for each space deixis occurence

    Returns:
    --------
    factors : float
        Number between 0.0 and 1.0


    Information:
    ------------
    https://gsw.phil-fak.uni-duesseldorf.de/diskurslinguistik/index.php?title=Deiktischer_Ausdruck
    """
    return _deixis(headword=headword,
                   lemmas=lemmas,
                   deixis_terms=space_deixis_terms,
                   penalty_factor=penalty_factor)


DEFAULT_TIME_DEIXIS_TERMS = [
    'jetzt', 'heute', 'gestern', 'morgen', 'dann', 'damals', 'bald',
    'kürzlich']


def deixis_time(headword: str,
                lemmas: List[str],
                time_deixis_terms: List[str] = DEFAULT_TIME_DEIXIS_TERMS,
                penalty_factor: float = 0.1) -> float:
    """Time deixis penality

    Parameters:
    -----------
    headword : str
        The headword (lemma) to evaluate in combination with the sentence.
        The headword is excluded from the count.

    lemmas : List[str]
        All lemmas of the sentence

    time_deixis_terms : List[str] (Default DEFAULT_TIME_DEIXIS_TERMS)
        The time deixis terms to look for in the sentence

    penalty_factor : float (Default 0.1)
        The penality factor for each time deixis occurence
        in the sentence.

    Returns:
    --------
    factors : float
        Number between 0.0 and 1.0

    Information:
    ------------
    https://gsw.phil-fak.uni-duesseldorf.de/diskurslinguistik/index.php?title=Deiktischer_Ausdruck
    """
    return _deixis(headword=headword,
                   lemmas=lemmas,
                   deixis_terms=time_deixis_terms,
                   penalty_factor=penalty_factor)


def deixis_person(headword: str,
                  annotation: List[dict],
                  penalty_factor: float = 0.1) -> float:
    """Personal deixis penality

    We use UD's UPOS and features as filter criteria. The following
    pronoums are substituting:
    - PDS (PRON + Dem): das, dies, die, diese, der
    - PIS (PRON + Ind,Neg,Tot): man, allem, nichts, alles, mehr
    - PPER (PRON + Prs): es, sie, er, wir, ich
    - PPOSS (PRON + Prs): ihren, Seinen, seinem, unsrigen, meiner
    see https://universaldependencies.org/tagset-conversion/de-stts-uposf.html
    see https://universaldependencies.org/en/feat/PronType.html

    Parameters:
    -----------
    headword : str
        The headword (lemma) to evaluate in combination with the sentence.
        The headword is excluded from the count.

    annotation : List[dict]
        The linguistic annoations of the sentence

    penality_factor : float (Default 0.1)
        The penality factor for each personal deixis occurence
        in the sentence.

    Returns:
    --------
    factors : float
        Number between 0.0 and 1.0
    """
    PTyp = {'Prs', 'Dem', 'Ind', 'Neg', 'Tot'}
    num_matches = 0
    for t in annotation:
        if t['lemma'] != headword:
            if t.get('upos', '') == 'PRON':
                if t.get('feats', {}).get('PronType', '') in PTyp:
                    num_matches += 1
    return max(0.0, 1.0 - penalty_factor * num_matches)


def optimal_interval(num_tokens: int, low: int = 10, high: int = 20) -> float:
    """Optimal sentence length by the number of word tokens

    Parameters:
    -----------
    num_tokens : int
        Number of word tokens in the sentence

    low : int (Default 10)
        Lower bound of the optimal interval

    high : int (Default 20)
        Upper bound of the optimal interval

    Returns:
    --------
    factor : float
        Number between 0.0 and 1.0
        0.0 (=sentence length bad), 1.0 (=sentence length ok)
    """
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
