import conllu
import random
import quaxa
import quaxa.reader

random.seed(42)


def demo():
    # read conllu file
    corpus = conllu.parse(open('demo.conllu', 'r').read())
    sents, annot = quaxa.reader.parse_conllu(corpus)
    # compute scores for example sentences
    print(f'{sents[0]}')
    for sent, anno in zip(sents, annot):
        lemmas_content = [tok.get('lemma') for tok in anno if tok.get('upos') in {'NOUN', 'VERB', 'ADJ'}]
        for headword in lemmas_content:
            factor = quaxa.total_score(
                        headword=headword, txt=sent, annotation=anno)
            print((
            "total_score:"
            f"{factor: 7.4f}  | {headword} | {sent[:50]} ..."))


if __name__ == '__main__':
    demo()
