import unittest
import quax


class QuaxTester(unittest.TestCase):
    def setUp(self):
        # EXAMPLE 1
        self.sent1 = 'Ich hatte Gelegenheit eines seiner Seminare zu besuchen.',
        self.tree1 = [{'text': 'Ich',
                'lemma': 'ich',
                'pos': 'PRON',
                'tag': 'PPER',
                'head': 'hatte',
                'dep': 'nsubj',
                'children': []},
                {'text': 'hatte',
                'lemma': 'haben',
                'pos': 'VERB',
                'tag': 'VAFIN',
                'head': '',
                'dep': 'root',
                'children': ['Ich', 'Gelegenheit', '.']},
                {'text': 'Gelegenheit',
                'lemma': 'Gelegenheit',
                'pos': 'NOUN',
                'tag': 'NN',
                'head': 'hatte',
                'dep': 'obj',
                'children': ['besuchen']},
                {'text': 'eines',
                'lemma': 'ein',
                'pos': 'DET',
                'tag': 'PIS',
                'head': 'Seminare',
                'dep': 'det',
                'children': []},
                {'text': 'seiner',
                'lemma': 'sein',
                'pos': 'DET',
                'tag': 'PPOSAT',
                'head': 'Seminare',
                'dep': 'det:poss',
                'children': []},
                {'text': 'Seminare',
                'lemma': 'Seminar',
                'pos': 'NOUN',
                'tag': 'NN',
                'head': 'besuchen',
                'dep': 'obj',
                'children': ['eines', 'seiner']},
                {'text': 'zu',
                'lemma': 'zu',
                'pos': 'PART',
                'tag': 'PTKZU',
                'head': 'besuchen',
                'dep': 'mark',
                'children': []},
                {'text': 'besuchen',
                'lemma': 'besuchen',
                'pos': 'VERB',
                'tag': 'VVINF',
                'head': 'Gelegenheit',
                'dep': 'xcomp',
                'children': ['Seminare', 'zu']},
                {'text': '.',
                'lemma': '.',
                'pos': 'PUNCT',
                'tag': '$.',
                'head': 'hatte',
                'dep': 'punct',
                'children': []}]
        self.lemma1 = 'haben'
        self.tokens1 = ['Ich',
                    'hatte',
                    'Gelegenheit',
                    'eines',
                    'seiner',
                    'Seminare',
                    'zu',
                    'besuchen',
                    '.']
        self.lemmata1 = ['ich',
                    'haben',
                    'Gelegenheit',
                    'ein',
                    'sein',
                    'Seminar',
                    'zu',
                    'besuchen',
                    '.']
        self.upos1 = ['PRON', 'VERB', 'NOUN', 'DET', 'DET', 'NOUN', 'PART', 'VERB', 'PUNCT']
        self.xpos1 = ['PPER', 'VAFIN', 'NN', 'PIS', 'PPOSAT', 'NN', 'PTKZU', 'VVINF', '$.']


    def test_is_whole_sentence(self):
        result1 = quax.is_whole_sentence(self.sent1, self.tree1)
        self.assertTrue(result1)
        txt = 'Keine Ahnung, was das soll.'
        baum = [
            {'text': 'Keine', 'lemma': 'kein', 'pos': 'DET', 'tag': 'PIAT', 'dep': 'nk', 'head': 'Ahnung', 'children': []},
            {'text': 'Ahnung', 'lemma': 'Ahnung', 'pos': 'NOUN', 'tag': 'NN', 'dep': 'ROOT', 'head': 'Ahnung', 'children': ['Keine', ',', 'soll', '.']},
            {'text': ',', 'lemma': '--', 'pos': 'PUNCT', 'tag': '$,', 'dep': 'punct', 'head': 'Ahnung', 'children': []},
            {'text': 'was', 'lemma': 'wer', 'pos': 'PRON', 'tag': 'PWS', 'dep': 'oa', 'head': 'soll', 'children': []},
            {'text': 'das', 'lemma': 'der', 'pos': 'PRON', 'tag': 'PDS', 'dep': 'sb', 'head': 'soll', 'children': []},
            {'text': 'soll', 'lemma': 'sollen', 'pos': 'AUX', 'tag': 'VMFIN', 'dep': 'rc', 'head': 'Ahnung', 'children': ['was', 'das']},
            {'text': '.', 'lemma': '--', 'pos': 'PUNCT', 'tag': '$.', 'dep': 'punct', 'head': 'Ahnung', 'children': []}
            ]
        result2 = quax.is_whole_sentence(txt, baum)
        self.assertFalse(result2)

    def test_is_misparsed(self):
        result1 = quax.is_misparsed(self.sent1)
        self.assertFalse(result1)
        result2 = quax.is_misparsed('Das ist ein Beispieltext')
        self.assertTrue(result2)
        result3 = quax.is_misparsed('das ist ein Beispieltext.')
        self.assertTrue(result3)
        result4 = quax.is_misparsed('\tDas ist ein Beispieltext.')
        self.assertTrue(result4)

    def test_has_illegal_chars(self):
        result1 = quax.has_illegal_chars(self.sent1)
        self.assertFalse(result1)
        result2 = quax.has_illegal_chars('https://somerandomurl.com')
        self.assertTrue(result2)
        result3 = quax.has_illegal_chars('name@mail.com')
        self.assertTrue(result3)

    def test_has_blacklist_words(self):
        result1 = quax.has_blacklist_words(self.sent1, self.lemma1, self.lemmata1)
        self.assertFalse(result1)
        result2 = quax.has_blacklist_words("Und das ist ein Beispielsatz mit Idiot.", 'Beispielsatz',
            ['und', 'der', 'sein', 'ein', 'Beispielsatz', 'mit', 'Idiot', '--'])
        self.assertTrue(result2)
        result3 = quax.has_blacklist_words("Und das ist ein Beispielsatz mit Idiot.", 'Idiot',
            ['und', 'der', 'sein', 'ein', 'Beispielsatz', 'mit', 'Idiot', '--'])
        self.assertTrue(result3)

    def test_factor_graylist_rarechars(self):
        result1 = quax.factor_graylist_rarechars(self.sent1)
        self.assertGreater(result1, 0.5)
        result2 = quax.factor_graylist_rarechars("''..??")
        self.assertGreater(0.5, result2)

    def test_factor_graylist_nongermankeyboardchars(self):
        result1 = quax.factor_graylist_nongermankeyboardchars(self.sent1)
        self.assertEqual(result1, 1.)
        result2 = quax.factor_graylist_nongermankeyboardchars('ßÄÖÜäöü')
        self.assertEqual(result2, 1.)
        result3 = quax.factor_graylist_nongermankeyboardchars('À la carte, s\'il vous plaît\n')
        self.assertLess(result3, 1.)

    def test_factor_graylist_words(self):
        result1 = quax.factor_graylist_words(self.sent1, self.xpos1)
        self.assertLess(result1, 1.)
        result2 = quax.factor_graylist_words('Kein Problem.', ['PIAT', 'NN'])
        self.assertEqual(result2, 1.)

    def test_greylist_ne(self):
        result1 = quax.greylist_ne(self.sent1, self.upos1, self.xpos1)
        self.assertEqual(result1, 1.)
        result2 = quax.greylist_ne('Manasse ist ein einzigartiger Parfümeur.',
                              ['PROPN', 'AUX', 'DET', 'ADJ', 'NOUN', 'PUNCT'],
                              ['NE', 'VAFIN', 'ART', 'ADJA', 'NN', '$.'])
        self.assertLess(result2, 1.)

    def test_deixis(self):
        result1 = [quax.deixis_space(self.sent1, self.lemma1, self.lemmata1),
                   quax.deixis_time(self.sent1, self.lemma1, self.lemmata1),
                   quax.deixis_person(self.sent1, self.lemma1, self.lemmata1)]
        self.assertEqual(result1, [0, 0, 0])
        sent2, lemmata2 = "Heute hier, morgen dort.", ['heute', 'hier', '--', 'morgen', 'dort', '--']
        result2 = [quax.deixis_space(sent2, 'heute', lemmata2),
                   quax.deixis_time(sent2, 'heute', lemmata2),
                   quax.deixis_person(sent2, 'heute', lemmata2)]
        self.assertEqual(result2, [2, 1, 0])
        result3 = [quax.deixis_space(sent2, 'hier', lemmata2),
                   quax.deixis_time(sent2, 'hier', lemmata2),
                   quax.deixis_person(sent2, 'hier', lemmata2)]
        self.assertEqual(result3, [1, 2, 0])

    def test_optimal_interval(self):
        result1 = quax.optimal_interval(self.tokens)
        self.assertLess(result1, 1.)
        result2 = quax.optimal_interval('Das ist ein Beispielsatz mit optimaler Länge von über 10 Tokens.')
        self.assertEqual(result2, 1.)
        result3 = quax.optimal_interval('Viel zu kurz.')
        self.assertEqual(result3, 0.)
        result4 = quax.optimal_interval('Dieser hingegen ist leider zu lang. Das macht ihn weniger angenehm zu lesen. Daher ist der zurückgegebene Wert kleiner als 1, schade.')
        self.assertLess(result4, 1.)
