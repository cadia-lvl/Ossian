import unittest
import os
from Lexicon import Lexicon
from util.LookupTable import LookupTable


class TestLexicon(unittest.TestCase):

    def test_syllabify(self):
        lex = self.init_lexicon()
        phonestring = 'a:1 v h E0 n_0 t I0'
        syllabified = lex.syllabify(phonestring)
        self.assertEqual('a:1 v | h E0 n_0 | t I0', syllabified)


    def init_lexicon(self):
        lex = Lexicon(dictionary='lvldict')
        #lex.voice_resources = Resources()
        lex.model_dir = 'data/'
        lex.lexicon_fname = os.path.join(lex.model_dir, 'lexicon.txt')
        #lex.lts_fname = os.path.join(lex.model_dir, 'lts.model')
        lex.phoneset_fname = os.path.join(lex.model_dir, 'phones.table')
        lex.onsets_fname = os.path.join(lex.model_dir, 'onsets.txt')
        lex.letter_fname = os.path.join(lex.model_dir, 'letter.names')
        lex.load_lexicon()  # populate self.entries
        lex.load_onsets()  # populate self.onsets
        lex.phoneset = LookupTable(lex.phoneset_fname, is_phoneset=True)
        lex.load_letternames()  # populate self.letternames

        return lex