import unittest

from quax.quax import is_whole_sentence, is_misparsed, has_illegal_chars, has_blacklist_words

class QuaxTester(unittest.TestCase):
    def setUp(self):
        # EXAMPLE 1
        sent1 = 'Ich hatte Gelegenheit eines seiner Seminare zu besuchen.',
        tree1 = [{'text': 'Ich',
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
        lemma1 = 'haben'
        tokens1 = ['Ich',
                    'hatte',
                    'Gelegenheit',
                    'eines',
                    'seiner',
                    'Seminare',
                    'zu',
                    'besuchen',
                    '.']
        lemmata1 = ['ich',
                    'haben',
                    'Gelegenheit',
                    'ein',
                    'sein',
                    'Seminar',
                    'zu',
                    'besuchen',
                    '.']
        upos1 = ['PRON', 'VERB', 'NOUN', 'DET', 'DET', 'NOUN', 'PART', 'VERB', 'PUNCT']
        xpos1 = ['PPER', 'VAFIN', 'NN', 'PIS', 'PPOSAT', 'NN', 'PTKZU', 'VVINF', '$.']


    def test_is_whole_sentence(self):
        result1 = is_whole_sentence(self.sent1, self.tree1)
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
        result2 = is_whole_sentence(txt, baum)
        self.assertFalse(result2)

    def test_is_misparsed(self):
        result1 = is_misparsed(self.sent1)
        self.assertFalse(result1)
        result2 = is_misparsed('Das ist ein Beispieltext')
        self.assertTrue(result2)
        result3 = is_misparsed('das ist ein Beispieltext.')
        self.assertTrue(result3)
        result4 = is_misparsed('\tDas ist ein Beispieltext.')
        self.assertTrue(result4)

    def test_has_illegal_chars(self):
        result1 = has_illegal_chars(self.sent1)
        self.assertFalse(result1)
        result2 = has_illegal_chars('https://somerandomurl.com')
        self.assertTrue(result2)
        result3 = has_illegal_chars('name@mail.com')
        self.assertTrue(result3)

    def test_has_blacklist_words(self):
        result1 = has_blacklist_words(self.sent1, self.lemma1, self.lemmata1)
        self.assertFalse(result1)
        result2 = has_blacklist_words("Und das ist ein Beispielsatz mit Idiot.", 'Beispielsatz',
            ['und', 'der', 'sein', 'ein', 'Beispielsatz', 'mit', 'Idiot', '--'])
        self.assertTrue(result2)
        result3 = has_blacklist_words("Und das ist ein Beispielsatz mit Idiot.", 'Idiot',
            ['und', 'der', 'sein', 'ein', 'Beispielsatz', 'mit', 'Idiot', '--'])
        self.assertTrue(result3)
