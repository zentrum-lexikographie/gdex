import unittest
import quaxa


SENTS = [
    "Manasse ist ein einzigartiger Parfümeur.",
    "Ich hatte Gelegenheit eines seiner Seminare zu besuchen.",
    (
        "7 Tage Erholung im Ferienhaus am Müritz See in einer idyllischen "
        "Landschaft inmitten der Mecklenburgischen Seenplatte.")
]


ANNOTS = [
    [
        {
            "id": 1,
            "text": "Manasse",
            "lemma": "Manasse",
            "upos": "PROPN",
            "feats": {
                "Case": "Nom",
                "Gender": "Fem",
                "Number": "Sing"
            },
            "head": 5,
            "deprel": "nsubj"
        },
        {
            "id": 2,
            "text": "ist",
            "lemma": "sein",
            "upos": "AUX",
            "feats": {
                "Mood": "Ind",
                "Number": "Sing",
                "Person": "3",
                "Tense": "Pres",
                "VerbForm": "Fin"
            },
            "head": 5,
            "deprel": "cop"
        },
        {
            "id": 3,
            "text": "ein",
            "lemma": "ein",
            "upos": "DET",
            "feats": {
                "Case": "Nom",
                "Definite": "Ind",
                "Gender": "Masc",
                "Number": "Sing",
                "NumType": "Card",
                "PronType": "Art"
            },
            "head": 5,
            "deprel": "det"
        },
        {
            "id": 4,
            "text": "einzigartiger",
            "lemma": "einzigartig",
            "upos": "ADJ",
            "feats": {
                "Case": "Nom",
                "Degree": "Pos",
                "Gender": "Masc",
                "Number": "Sing"
            },
            "head": 5,
            "deprel": "amod"
        },
        {
            "id": 5,
            "text": "Parfümeur",
            "lemma": "Parfümeur",
            "upos": "NOUN",
            "feats": {
                "Case": "Nom",
                "Gender": "Masc",
                "Number": "Sing"
            },
            "head": 0,
            "deprel": "root"
        },
        {
            "id": 6,
            "text": ".",
            "lemma": ".",
            "upos": "PUNCT",
            "head": 5,
            "deprel": "punct"
        }
    ],
    [
        {
            "id": 1,
            "text": "Ich",
            "lemma": "ich",
            "upos": "PRON",
            "feats": {
                "Case": "Nom",
                "Number": "Sing",
                "Person": "1",
                "PronType": "Prs"
            },
            "head": 2,
            "deprel": "nsubj"
        },
        {
            "id": 2,
            "text": "hatte",
            "lemma": "haben",
            "upos": "VERB",
            "feats": {
                "Mood": "Ind",
                "Number": "Sing",
                "Person": "1",
                "Tense": "Past",
                "VerbForm": "Fin"
            },
            "head": 0,
            "deprel": "root"
        },
        {
            "id": 3,
            "text": "Gelegenheit",
            "lemma": "Gelegenheit",
            "upos": "NOUN",
            "feats": {
                "Case": "Acc",
                "Gender": "Fem",
                "Number": "Sing"
            },
            "head": 2,
            "deprel": "obj"
        },
        {
            "id": 4,
            "text": "eines",
            "lemma": "ein",
            "upos": "DET",
            "feats": {
                "Case": "Acc",
                "Definite": "Ind",
                "Gender": "Neut",
                "Number": "Sing",
                "NumType": "Card",
                "PronType": "Art"
            },
            "head": 6,
            "deprel": "det"
        },
        {
            "id": 5,
            "text": "seiner",
            "lemma": "sein",
            "upos": "DET",
            "feats": {
                "Case": "Gen",
                "Gender": "Neut",
                "Gender[psor]": "Masc,Neut",
                "Number": "Plur",
                "Number[psor]": "Sing",
                "Person": "3",
                "Poss": "Yes",
                "PronType": "Prs"
            },
            "head": 6,
            "deprel": "det:poss"
        },
        {
            "id": 6,
            "text": "Seminare",
            "lemma": "Seminar",
            "upos": "NOUN",
            "feats": {
                "Case": "Gen",
                "Gender": "Neut",
                "Number": "Plur"
            },
            "head": 8,
            "deprel": "obj"
        },
        {
            "id": 7,
            "text": "zu",
            "lemma": "zu",
            "upos": "PART",
            "head": 8,
            "deprel": "mark"
        },
        {
            "id": 8,
            "text": "besuchen",
            "lemma": "besuchen",
            "upos": "VERB",
            "feats": {
                "VerbForm": "Inf"
            },
            "head": 3,
            "deprel": "xcomp"
        },
        {
            "id": 9,
            "text": ".",
            "lemma": ".",
            "upos": "PUNCT",
            "head": 2,
            "deprel": "punct"
        }
    ],
    [
        {
            "id": 1,
            "text": "7",
            "lemma": "7",
            "upos": "NUM",
            "feats": {
                "NumType": "Card"
            },
            "head": 2,
            "deprel": "nummod"
        },
        {
            "id": 2,
            "text": "Tage",
            "lemma": "Tag",
            "upos": "NOUN",
            "feats": {
                "Case": "Nom",
                "Gender": "Fem",
                "Number": "Sing"
            },
            "head": 3,
            "deprel": "nmod"
        },
        {
            "id": 3,
            "text": "Erholung",
            "lemma": "Erholung",
            "upos": "NOUN",
            "feats": {
                "Case": "Acc",
                "Gender": "Fem",
                "Number": "Sing"
            },
            "head": 0,
            "deprel": "root"
        },
        {
            "id": (4, "-", 5),
            "text": "im",
            "lemma": "_",
            "upos": "_",
            "deprel": "_"
        },
        {
            "id": 4,
            "text": "in",
            "lemma": "in",
            "upos": "ADP",
            "head": 6,
            "deprel": "case"
        },
        {
            "id": 5,
            "text": "dem",
            "lemma": "der",
            "upos": "DET",
            "feats": {
                "Case": "Dat",
                "Definite": "Def",
                "Gender": "Neut",
                "Number": "Sing",
                "PronType": "Art"
            },
            "head": 6,
            "deprel": "det"
        },
        {
            "id": 6,
            "text": "Ferienhaus",
            "lemma": "Ferienhaus",
            "upos": "NOUN",
            "feats": {
                "Case": "Dat",
                "Gender": "Neut",
                "Number": "Sing"
            },
            "head": 3,
            "deprel": "nmod"
        },
        {
            "id": (7, "-", 8),
            "text": "am",
            "lemma": "_",
            "upos": "_",
            "deprel": "_"
        },
        {
            "id": 7,
            "text": "an",
            "lemma": "an",
            "upos": "ADP",
            "head": 9,
            "deprel": "case"
        },
        {
            "id": 8,
            "text": "dem",
            "lemma": "der",
            "upos": "DET",
            "feats": {
                "Case": "Dat",
                "Definite": "Def",
                "Gender": "Masc",
                "Number": "Sing",
                "PronType": "Art"
            },
            "head": 9,
            "deprel": "det"
        },
        {
            "id": 9,
            "text": "Müritz",
            "lemma": "Müritz",
            "upos": "PROPN",
            "feats": {
                "Case": "Dat",
                "Gender": "Masc",
                "Number": "Sing"
            },
            "head": 6,
            "deprel": "nmod"
        },
        {
            "id": 10,
            "text": "See",
            "lemma": "See",
            "upos": "PROPN",
            "feats": {
                "Case": "Dat",
                "Gender": "Masc",
                "Number": "Sing"
            },
            "head": 9,
            "deprel": "flat"
        },
        {
            "id": 11,
            "text": "in",
            "lemma": "in",
            "upos": "ADP",
            "head": 14,
            "deprel": "case"
        },
        {
            "id": 12,
            "text": "einer",
            "lemma": "ein",
            "upos": "DET",
            "feats": {
                "Case": "Dat",
                "Definite": "Ind",
                "Gender": "Fem",
                "Number": "Sing",
                "NumType": "Card",
                "PronType": "Art"
            },
            "head": 14,
            "deprel": "det"
        },
        {
            "id": 13,
            "text": "idyllischen",
            "lemma": "idyllisch",
            "upos": "ADJ",
            "feats": {
                "Case": "Dat",
                "Degree": "Pos",
                "Gender": "Fem",
                "Number": "Sing"
            },
            "head": 14,
            "deprel": "amod"
        },
        {
            "id": 14,
            "text": "Landschaft",
            "lemma": "Landschaft",
            "upos": "NOUN",
            "feats": {
                "Case": "Dat",
                "Gender": "Fem",
                "Number": "Sing"
            },
            "head": 9,
            "deprel": "nmod"
        },
        {
            "id": 15,
            "text": "inmitten",
            "lemma": "inmitten",
            "upos": "ADP",
            "head": 18,
            "deprel": "case"
        },
        {
            "id": 16,
            "text": "der",
            "lemma": "der",
            "upos": "DET",
            "feats": {
                "Case": "Dat",
                "Definite": "Def",
                "Gender": "Fem",
                "Number": "Sing",
                "PronType": "Art"
            },
            "head": 18,
            "deprel": "det"
        },
        {
            "id": 17,
            "text": "Mecklenburgischen",
            "lemma": "Mecklenburgischen",
            "upos": "PROPN",
            "feats": {
                "Case": "Dat",
                "Gender": "Fem",
                "Number": "Sing"
            },
            "head": 18,
            "deprel": "amod"
        },
        {
            "id": 18,
            "text": "Seenplatte",
            "lemma": "Seenplatte",
            "upos": "PROPN",
            "feats": {
                "Case": "Dat",
                "Gender": "Fem",
                "Number": "Sing"
            },
            "head": 9,
            "deprel": "nmod"
        },
        {
            "id": 19,
            "text": ".",
            "lemma": ".",
            "upos": "PUNCT",
            "head": 3,
            "deprel": "punct"
        }
    ]
]


class QuaxTester(unittest.TestCase):
    def setUp(self):
        self.sents = SENTS
        self.annots = ANNOTS
        self.lemmata = [
            [tok.get('lemma') for tok in tree] for tree in self.annots]

    def test_total_score(self):
        for txt, annot in zip(self.sents, self.annots):
            for tok in annot:
                if tok.get('upos', '') in {'NOUN', 'VERB', 'ADJ'}:
                    headword = tok['lemma']
                    factor = quaxa.total_score(
                        headword=headword, txt=txt, annotation=annot)
                    print((
                        "total_score:"
                        f"{factor: 7.4f}  | {headword} | {txt[:20]} ..."))
                    self.assertGreaterEqual(factor, 0.)
                    self.assertLessEqual(factor, 1.)

    def test_isa_knockout_criteria(self):
        for txt, annot in zip(self.sents, self.annots):
            for tok in annot:
                if tok.get('upos', '') in {'NOUN', 'VERB', 'ADJ'}:
                    headword = tok['lemma']
                    flag = quaxa.isa_knockout_criteria(
                        headword=headword, txt=txt, annotation=annot)
                    print((
                        "isa_knockout_criteria:"
                        f"{flag}  | {headword} | {txt[:20]} ..."))
                    self.assertIs(flag is True or flag is False, True)

    def test_factor_gradual_criteria(self):
        for txt, annot in zip(self.sents, self.annots):
            for tok in annot:
                if tok.get('upos', '') in {'NOUN', 'VERB', 'ADJ'}:
                    headword = tok['lemma']
                    factor = quaxa.factor_gradual_criteria(
                        headword=headword, txt=txt, annotation=annot)
                    print((
                        "factor_gradual_criteria:"
                        f"{factor:7.4f}  | {headword} | {txt[:20]} ..."))
                    self.assertGreaterEqual(factor, 0.)
                    self.assertLessEqual(factor, 1.)

    def test_has_finite_verb_and_subject(self):
        target = [True, True, False]
        for i, annot in enumerate(self.annots):
            res = quaxa.has_finite_verb_and_subject(annot)
            self.assertEqual(res, target[i])

    def test_is_misparsed(self):
        for sent in self.sents:
            res = quaxa.is_misparsed(sent)
            self.assertFalse(res)

        res = quaxa.is_misparsed('Das ist ein Beispieltext.')
        self.assertFalse(res)

        res = quaxa.is_misparsed('Das ist ein Beispieltext')
        self.assertTrue(res)

        res = quaxa.is_misparsed('das ist ein Beispieltext.')
        self.assertTrue(res)

        res = quaxa.is_misparsed('\tDas ist ein Beispieltext.')
        self.assertTrue(res)

    def test_has_illegal_chars(self):
        for sent in self.sents:
            res = quaxa.has_illegal_chars(sent)
            self.assertFalse(res)

        res = quaxa.has_illegal_chars('https://somerandomurl.com')
        self.assertTrue(res)

        res = quaxa.has_illegal_chars('name@mail.com')
        self.assertTrue(res)

        res = quaxa.has_illegal_chars('my test\rnew windows paragraph')
        self.assertTrue(res)

    def test_has_blacklist_words(self):
        for annot in self.annots:
            lemmas = [tok.get('lemma') for tok in annot]
            for tok in annot:
                headword = tok['lemma']
                res = quaxa.has_blacklist_words(
                    headword=headword, lemmas=lemmas)
                self.assertFalse(res)

        res = quaxa.has_blacklist_words('Beispielsatz', [
            'und', 'der', 'sein', 'ein', 'Beispielsatz', 'mit', 'Idiot', '--'])
        self.assertTrue(res)

        res = quaxa.has_blacklist_words('Idiot', [
            'und', 'der', 'sein', 'ein', 'Beispielsatz', 'mit', 'Idiot', '--'])
        self.assertFalse(res)

    def test_factor_graylist_rarechars(self):
        target = [0.9, 0.9, 0.8]
        for i, sent in enumerate(self.sents):
            res = quaxa.factor_rarechars(sent)
            self.assertEqual(res, target[i])

        res = quaxa.factor_rarechars("\'\'..??")
        self.assertAlmostEqual(res, 0.4)  # rounding error

    def test_factor_graylist_notkeyboardchar(self):
        for sent in self.sents:
            res = quaxa.factor_notkeyboardchar(sent)
            self.assertEqual(res, 1.)

        res = quaxa.factor_notkeyboardchar('ßÄÖÜäöü')
        self.assertEqual(res, 1.)

        res = quaxa.factor_notkeyboardchar(
            'À la carte, s\'il vous plaît\n')
        self.assertLess(res, 1.0)

    def test_factor_graylist_words(self):
        GRAYLIST = ['Seminar']
        target = [1.0, 0.9, 1.0]
        for i, annot in enumerate(self.annots):
            lemmas = [tok.get('lemma') for tok in annot]
            for tok in annot:
                headword = tok['lemma']
                res = quaxa.factor_graylist_words(
                    headword=headword, lemmas=lemmas, graylist_words=GRAYLIST)
                if headword in GRAYLIST:
                    self.assertEqual(res, target[i] + 0.1)
                else:
                    self.assertEqual(res, target[i])

    def test_factor_named_entity(self):
        for annot in self.annots:
            for tok in annot:
                headword = tok['lemma']
                res = quaxa.factor_named_entity(
                    headword=headword, annotation=annot, penalty_factor=0.15)
                flag = tok.get('upos', '') == 'PROPN'
                flag = flag or tok.get('xpos', '') == 'NE'
                if flag:
                    self.assertEqual(res, 0.85)
                else:
                    self.assertEqual(res, 1.0)

    def test_deixis(self):
        lemmas = ['heute', 'hier', '--', 'morgen', 'dort', '--']
        result2 = [quaxa.deixis_space('heute', lemmas),
                   quaxa.deixis_time('heute', lemmas)]
        self.assertEqual(result2, [.8, .9])

        result3 = [quaxa.deixis_space('hier', lemmas),
                   quaxa.deixis_time('hier', lemmas)]
        self.assertEqual(result3, [.9, .8])

    def test_deixis_person(self):
        target = [1.0, 0.9, 1.0]
        for i, annot in enumerate(self.annots):
            for tok in annot:
                headword = tok['lemma']
                res = quaxa.deixis_person(
                    headword=headword, annotation=annot)
                flag = tok.get('upos', '') == 'PRON'
                flag = flag and tok.get('feats', {}).get('PronType', '') in [
                    'Prs', 'Dem', 'Ind', 'Neg', 'Tot']
                if flag:
                    self.assertEqual(res, target[i] + 0.1)
                else:
                    self.assertEqual(res, target[i])

    def test_optimal_interval(self):
        for annot in self.annots:
            num_tokens = len(annot)
            res = quaxa.optimal_interval(
                num_tokens=num_tokens,
                low=num_tokens * 2,
                high=num_tokens * 3)
            self.assertLess(res, 1.)
            res = quaxa.optimal_interval(
                num_tokens=num_tokens,
                low=num_tokens // 2,
                high=num_tokens * 2)
            self.assertEqual(res, 1.)

        num_tokens = len((
            "Das ist ein Beispielsatz mit optimaler Länge von über 10 Tokens."
        ).split(" "))
        result2 = quaxa.optimal_interval(num_tokens=num_tokens)
        self.assertEqual(result2, 1.)

        num_tokens = len('Viel zu kurz.'.split(" "))
        result3 = quaxa.optimal_interval(num_tokens=num_tokens)
        self.assertEqual(result3, 0.)

        num_tokens = len((
            "Dieser hingegen ist leider zu lang. Das macht ihn weniger "
            "angenehm zu lesen. Daher ist der zurückgegebene Wert kleiner "
            "als 1, schade.").split(" "))
        result4 = quaxa.optimal_interval(num_tokens=num_tokens)
        self.assertLess(result4, 1.)
