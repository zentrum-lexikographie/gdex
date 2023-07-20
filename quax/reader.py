from typing import List
import conllu
import random
random.seed(42)


def parse_conllu(corpus: List[conllu.models.TokenList]) -> List[dict]:
    """

    Usage:
    ------
    >>> import conllu
    >>> import quax
    >>> corpus = conllu.parse(open('myfile.conllu', 'r').read())
    >>> sents, trees, lemmata = quax.parse_conllu(corpus)
    """

    # process each sentence of a corpus
    sents, trees, lemmata = [], [], []
    for sent in corpus:
        sents.append(sent.metadata['text'])

        # process each token of a sentence
        s = []
        for tok in sent:
            d = {
                'text': tok['form'], 
                'lemma': tok['lemma'],
                'pos': tok['upos'], 
                'tag': tok['xpos'],
                'head': '', 
                'dep': tok['deprel']
            }
            if tok['head']:  # can be none in multi-line
                if sent[int(tok['head'])] != '0':
                    d['head'] = sent[int(tok['head'])-1]['form']
            s.append(d)

        # determine children
        for t in s:
            t['children'] = [t2['text'] for t2 in s if t2['head'] == t['text']]
        trees.append(s)

        # Shuffle lemmata ... WHY???
        lemmata.append(s[random.randrange(len(s))]['lemma'])

    # done
    return sents, trees, lemmata
