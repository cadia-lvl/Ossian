#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from Lexicon import Lexicon
from LexiconLVL import LexiconLVL
from util.LookupTable import LookupTable


class TestLexicon(unittest.TestCase):

    def test_syllabify(self):
        lex = self.init_lexicon()
        phonestring = 'a:1 v h E0 n_0 t I0'
        syllabified = lex.syllabify(phonestring)
        self.assertEqual('a:1 v | h E0 n_0 | t I0', syllabified)

    def test_lvl_syllabify(self):
        lex = self.init_lvl_lexicon()
        syllabified = lex.syllabify('landsbókasafn', 'l a1 n t s p ou:0 k a0 s a0 p n_0')
        self.assertEqual('l a1 n t s | p ou:0 | k a0 | s a0 p n_0', syllabified)

    def init_lvl_lexicon(self):
        lex = LexiconLVL(dictionary='lvldict')
        lex.model_dir = 'data/'
        lex.lexicon_fname = os.path.join(lex.model_dir, 'lexicon.txt')
        # lex.lts_fname = os.path.join(lex.model_dir, 'lts.model')
        lex.phoneset_fname = os.path.join(lex.model_dir, 'phones.table')
        lex.onsets_fname = os.path.join(lex.model_dir, 'onsets.txt')
        lex.letter_fname = os.path.join(lex.model_dir, 'letter.names')
        lex.load_lexicon()  # populate self.entries
        lex.load_onsets()  # populate self.onsets
        lex.phoneset = LookupTable(lex.phoneset_fname, is_phoneset=True)
        lex.load_letternames()  # populate self.letternames

        return lex

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