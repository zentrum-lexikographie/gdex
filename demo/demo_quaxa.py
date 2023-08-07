import conllu
import random
import quaxa
import quaxa.reader

random.seed(42)


def demo():
    # read conllu file
    corpus = conllu.parse(open('demo.conllu', 'r').read())
    # compute scores for example sentences
    for annot in corpus:
        lemmas_content = [
            tok.get('lemma') for tok in annot 
            if tok.get('upos') in {'NOUN', 'VERB', 'ADJ'}
        ]
        sent = annot.metadata['text']
        for headword in lemmas_content:
            factor = quaxa.total_score(
                headword=headword, txt=sent, annotation=annot)
            print((
                "total_score:"
                f"{factor: 7.4f}  | {headword} | {sent[:50]} ..."))


if __name__ == '__main__':
    demo()
