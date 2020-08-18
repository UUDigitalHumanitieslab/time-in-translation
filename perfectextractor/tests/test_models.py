import unittest

from perfectextractor.apps.extractor.models import Perfect

XML_ID = 'test_id'


class TestPerfect(unittest.TestCase):
    def setUp(self):
        self.pp = Perfect('has', 'have', 'VERB', XML_ID)
        self.pp.add_word('always', 'always', 'ADVERB', XML_ID, in_construction=False)
        self.pp.add_word('loved', 'love', 'VERB', XML_ID)

    def test_extractions(self):
        self.assertEqual(self.pp.perfect_lemma(), 'love')
        self.assertEqual(self.pp.construction(), ['has', 'loved'])
        self.assertEqual(self.pp.construction_to_string(), 'has loved')
        self.assertEqual(self.pp.words_between(), 1)

    def test_extend(self):
        ppp = Perfect('has', 'have', 'VERB', XML_ID)
        ppp.add_word('been', 'be', 'VERB', XML_ID)
        pp_extend = Perfect('been', 'be', 'VERB', XML_ID)
        pp_extend.add_word('created', 'create', 'VERB', XML_ID)
        ppp.extend(pp_extend)

        self.assertEqual(ppp.perfect_lemma(), 'create')
        self.assertEqual(ppp.construction(), ['has', 'been', 'created'])
        self.assertEqual(ppp.construction_to_string(), 'has been created')
        self.assertEqual(ppp.words_between(), 0)
