import unittest
import quax


SENTS = [
    "Manasse ist ein einzigartiger Parfümeur.",
    "Ich hatte Gelegenheit eines seiner Seminare zu besuchen.",
    (
        "7 Tage Erholung im Ferienhaus am Müritz See in einer idyllischen "
        "Landschaft inmitten der Mecklenburgischen Seenplatte.")
]


TREES = [
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
            "head": "Parfümeur",
            "deprel": "nsubj",
            "children": []
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
            "head": "Parfümeur",
            "deprel": "cop",
            "children": []
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
            "head": "Parfümeur",
            "deprel": "det",
            "children": []
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
            "head": "Parfümeur",
            "deprel": "amod",
            "children": []
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
            "head": "",
            "deprel": "root",
            "children": [
                "Manasse",
                "ist",
                "ein",
                "einzigartiger",
                "."
            ]
        },
        {
            "id": 6,
            "text": ".",
            "lemma": ".",
            "upos": "PUNCT",
            "head": "Parfümeur",
            "deprel": "punct",
            "children": []
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
            "head": "hatte",
            "deprel": "nsubj",
            "children": []
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
            "head": "",
            "deprel": "root",
            "children": [
                "Ich",
                "Gelegenheit",
                "."
            ]
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
            "head": "hatte",
            "deprel": "obj",
            "children": [
                "besuchen"
            ]
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
            "head": "Seminare",
            "deprel": "det",
            "children": []
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
            "head": "Seminare",
            "deprel": "det:poss",
            "children": []
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
            "head": "besuchen",
            "deprel": "obj",
            "children": [
                "eines",
                "seiner"
            ]
        },
        {
            "id": 7,
            "text": "zu",
            "lemma": "zu",
            "upos": "PART",
            "head": "besuchen",
            "deprel": "mark",
            "children": []
        },
        {
            "id": 8,
            "text": "besuchen",
            "lemma": "besuchen",
            "upos": "VERB",
            "feats": {
                "VerbForm": "Inf"
            },
            "head": "Gelegenheit",
            "deprel": "xcomp",
            "children": [
                "Seminare",
                "zu"
            ]
        },
        {
            "id": 9,
            "text": ".",
            "lemma": ".",
            "upos": "PUNCT",
            "head": "hatte",
            "deprel": "punct",
            "children": []
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
            "head": "Tage",
            "deprel": "nummod",
            "children": []
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
            "head": "Erholung",
            "deprel": "nmod",
            "children": [
                "7"
            ]
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
            "head": "",
            "deprel": "root",
            "children": [
                "Tage",
                "Ferienhaus",
                "."
            ]
        },
        {
            "id": [4, "-", 5],
            "text": "im",
            "lemma": "_",
            "upos": "_",
            "head": "",
            "deprel": "_",
            "children": []
        },
        {
            "id": 4,
            "text": "in",
            "lemma": "in",
            "upos": "ADP",
            "head": "dem",
            "deprel": "case",
            "children": []
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
            "head": "dem",
            "deprel": "det",
            "children": [
                "in",
                "dem",
                "Müritz"
            ]
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
            "head": "Erholung",
            "deprel": "nmod",
            "children": []
        },
        {
            "id": [7, "-", 8],
            "text": "am",
            "lemma": "_",
            "upos": "_",
            "head": "",
            "deprel": "_",
            "children": []
        },
        {
            "id": 7,
            "text": "an",
            "lemma": "an",
            "upos": "ADP",
            "head": "an",
            "deprel": "case",
            "children": [
                "an",
                "dem",
                "See",
                "Landschaft",
                "Seenplatte"
            ]
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
            "head": "an",
            "deprel": "det",
            "children": [
                "in",
                "dem",
                "Müritz"
            ]
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
            "head": "dem",
            "deprel": "nmod",
            "children": []
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
            "head": "an",
            "deprel": "flat",
            "children": []
        },
        {
            "id": 11,
            "text": "in",
            "lemma": "in",
            "upos": "ADP",
            "head": "einer",
            "deprel": "case",
            "children": []
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
            "head": "einer",
            "deprel": "det",
            "children": [
                "in",
                "einer",
                "idyllischen"
            ]
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
            "head": "einer",
            "deprel": "amod",
            "children": []
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
            "head": "an",
            "deprel": "nmod",
            "children": []
        },
        {
            "id": 15,
            "text": "inmitten",
            "lemma": "inmitten",
            "upos": "ADP",
            "head": "der",
            "deprel": "case",
            "children": []
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
            "head": "der",
            "deprel": "det",
            "children": [
                "inmitten",
                "der",
                "Mecklenburgischen"
            ]
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
            "head": "der",
            "deprel": "amod",
            "children": []
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
            "head": "an",
            "deprel": "nmod",
            "children": []
        },
        {
            "id": 19,
            "text": ".",
            "lemma": ".",
            "upos": "PUNCT",
            "head": "Erholung",
            "deprel": "punct",
            "children": []
        }
    ]
]


class QuaxTester(unittest.TestCase):
    def setUp(self):
        self.sents = SENTS
        self.trees = TREES
        self.lemmata = [
            [tok.get('lemma') for tok in tree] for tree in self.trees]


    # def test_is_whole_sentence(self):
    #     result1 = quax.is_whole_sentence(self.sent1, self.tree1)
    #     self.assertTrue(result1)
    #     txt = 'Keine Ahnung, was das soll.'
    #     baum = [
    #         {'text': 'Keine', 'lemma': 'kein', 'upos': 'DET', 'xpos': 'PIAT', 'deprel': 'nk', 'head': 'Ahnung', 'children': []},
    #         {'text': 'Ahnung', 'lemma': 'Ahnung', 'upos': 'NOUN', 'xpos': 'NN', 'deprel': 'ROOT', 'head': 'Ahnung', 'children': ['Keine', ',', 'soll', '.']},
    #         {'text': ',', 'lemma': '--', 'upos': 'PUNCT', 'xpos': '$,', 'deprel': 'punct', 'head': 'Ahnung', 'children': []},
    #         {'text': 'was', 'lemma': 'wer', 'upos': 'PRON', 'xpos': 'PWS', 'deprel': 'oa', 'head': 'soll', 'children': []},
    #         {'text': 'das', 'lemma': 'der', 'upos': 'PRON', 'xpos': 'PDS', 'deprel': 'sb', 'head': 'soll', 'children': []},
    #         {'text': 'soll', 'lemma': 'sollen', 'upos': 'AUX', 'xpos': 'VMFIN', 'deprel': 'rc', 'head': 'Ahnung', 'children': ['was', 'das']},
    #         {'text': '.', 'lemma': '--', 'upos': 'PUNCT', 'xpos': '$.', 'deprel': 'punct', 'head': 'Ahnung', 'children': []}
    #         ]
    #     result2 = quax.is_whole_sentence(txt, baum)
    #     self.assertFalse(result2)

    # def test_is_misparsed(self):
    #     result1 = quax.is_misparsed(self.sent1)
    #     self.assertFalse(result1)
    #     result2 = quax.is_misparsed('Das ist ein Beispieltext')
    #     self.assertTrue(result2)
    #     result3 = quax.is_misparsed('das ist ein Beispieltext.')
    #     self.assertTrue(result3)
    #     result4 = quax.is_misparsed('\tDas ist ein Beispieltext.')
    #     self.assertTrue(result4)

    # def test_has_illegal_chars(self):
    #     result1 = quax.has_illegal_chars(self.sent1)
    #     self.assertFalse(result1)
    #     result2 = quax.has_illegal_chars('https://somerandomurl.com')
    #     self.assertTrue(result2)
    #     result3 = quax.has_illegal_chars('name@mail.com')
    #     self.assertTrue(result3)

    # def test_has_blacklist_words(self):
    #     result1 = quax.has_blacklist_words(self.sent1, self.lemma1, self.lemmata1)
    #     self.assertFalse(result1)
    #     result2 = quax.has_blacklist_words("Und das ist ein Beispielsatz mit Idiot.", 'Beispielsatz',
    #         ['und', 'der', 'sein', 'ein', 'Beispielsatz', 'mit', 'Idiot', '--'])
    #     self.assertTrue(result2)
    #     result3 = quax.has_blacklist_words("Und das ist ein Beispielsatz mit Idiot.", 'Idiot',
    #         ['und', 'der', 'sein', 'ein', 'Beispielsatz', 'mit', 'Idiot', '--'])
    #     self.assertTrue(result3)

    # def test_factor_graylist_rarechars(self):
    #     result1 = quax.factor_graylist_rarechars(self.sent1)
    #     self.assertGreater(result1, 0.5)
    #     result2 = quax.factor_graylist_rarechars("''..??")
    #     self.assertGreater(0.5, result2)

    # def test_factor_graylist_nongermankeyboardchars(self):
    #     result1 = quax.factor_graylist_nongermankeyboardchars(self.sent1)
    #     self.assertEqual(result1, 1.)
    #     result2 = quax.factor_graylist_nongermankeyboardchars('ßÄÖÜäöü')
    #     self.assertEqual(result2, 1.)
    #     result3 = quax.factor_graylist_nongermankeyboardchars('À la carte, s\'il vous plaît\n')
    #     self.assertLess(result3, 1.)

    # def test_factor_graylist_words(self):
    #     result1 = quax.factor_graylist_words(self.sent1, self.xpos1)
    #     self.assertLess(result1, 1.)
    #     result2 = quax.factor_graylist_words('Kein Problem.', ['PIAT', 'NN'])
    #     self.assertEqual(result2, 1.)

    # def test_greylist_ne(self):
    #     result1 = quax.greylist_ne(self.sent1, self.upos1, self.xpos1)
    #     self.assertEqual(result1, 1.)
    #     result2 = quax.greylist_ne('Manasse ist ein einzigartiger Parfümeur.',
    #                           ['PROPN', 'AUX', 'DET', 'ADJ', 'NOUN', 'PUNCT'],
    #                           ['NE', 'VAFIN', 'ART', 'ADJA', 'NN', '$.'])
    #     self.assertLess(result2, 1.)


    def test_deixis(self):
        lemmas = ['heute', 'hier', '--', 'morgen', 'dort', '--']
        result2 = [quax.deixis_space('heute', lemmas),
                   quax.deixis_time('heute', lemmas)]
        self.assertEqual(result2, [.8, .9])

        result3 = [quax.deixis_space('hier', lemmas),
                   quax.deixis_time('hier', lemmas)]
        self.assertEqual(result3, [.9, .8])


    def test_deixis_person(self):
        target = [1.0, 0.8, 1.0]
        for i, tree in enumerate(self.trees):
            for tok in tree:
                headword = tok['lemma']
                res = quax.deixis_person(
                    headword=headword, dependency_tree=tree)
                if tok.get('feats', {}).get('PronType', '') == 'Prs':
                    self.assertEqual(res, target[i] + 0.1)
                else:
                    self.assertEqual(res, target[i])


    def test_optimal_interval(self):
        for tree in self.trees:
            num_tokens = len(tree)
            res = quax.optimal_interval(
                num_tokens=num_tokens, 
                low=num_tokens * 2, 
                high=num_tokens * 3)
            self.assertLess(res, 1.)
            res = quax.optimal_interval(
                num_tokens=num_tokens, 
                low=num_tokens // 2, 
                high=num_tokens * 2)
            self.assertEqual(res, 1.)

        num_tokens = len((
            "Das ist ein Beispielsatz mit optimaler Länge von über 10 Tokens."
            ).split(" "))
        result2 = quax.optimal_interval(num_tokens=num_tokens)
        self.assertEqual(result2, 1.)

        num_tokens = len('Viel zu kurz.'.split(" "))
        result3 = quax.optimal_interval(num_tokens=num_tokens)
        self.assertEqual(result3, 0.)

        num_tokens = len((
            "Dieser hingegen ist leider zu lang. Das macht ihn weniger "
            "angenehm zu lesen. Daher ist der zurückgegebene Wert kleiner "
            "als 1, schade.").split(" "))
        result4 = quax.optimal_interval(num_tokens=num_tokens)
        self.assertLess(result4, 1.)
