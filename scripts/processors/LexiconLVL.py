#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import default.const as c

from Lexicon import Lexicon

from lvl.pron_dict import entry
from lvl.pron_dict import syllabification
from lvl.pron_dict import tree_builder


class LexiconLVL(Lexicon):
    def __init__(self, processor_name='lexicon', target_nodes="//token", \
                 target_attribute='text', part_of_speech_attribute='pos', child_node_type='segment',
                 output_attribute='pronunciation', \
                 class_attribute='token_class', word_classes=['word'],
                 probable_pause_classes=['punctuation', c.TERMINAL], \
                 possible_pause_classes=['space'], \
                 dictionary='some_dictionary_name', backoff_pronunciation='axr', lts_variants=1, \
                 lts_ntrain=0, lts_gram_length=3, max_graphone_letters=2, max_graphone_phones=2):

        super(LexiconLVL, self).__init__(processor_name, target_nodes, target_attribute, part_of_speech_attribute,
                                         child_node_type, output_attribute, class_attribute, word_classes, probable_pause_classes,
                                         possible_pause_classes, dictionary, backoff_pronunciation, lts_variants,
                                         lts_ntrain, lts_gram_length, max_graphone_letters, max_graphone_phones)

    def verify(self, voice_resources):
        """
        Overridden because we need to locate the dictionary database

        :param voice_resources: a Resources object containing path, lang, and config information to the current voice
        :return:
        """
        super(LexiconLVL, self).verify(voice_resources)
        self.set_dictdatabase()

    def set_dictdatabase(self):
        db_location = os.path.join(self.voice_resources.path[c.LANG], 'labelled_corpora', self.dictionary + '_db')
        assert os.path.isfile(db_location + '/dictionary.db')
        self.comp_analyzer = tree_builder.CompoundAnalyzer(db_location + '/dictionary.db')

    def needs_letter_pronunciation(self, word):
        letter_patt = ur'[a-záðéóúýþæö]'
        if len(word) == 1 and re.match(letter_patt, word):
            return True
        initialism_patt = 'ur\A([a-záðéóúýþæö]\.)+\Z'
        if re.match(initialism_patt, word):
            return True
        return False

    def get_phonetic_segments(self, word, part_of_speech=None):

        word = word.lower()
        word = word.strip("'\" ;,")

        if self.needs_letter_pronunciation(word):
            pronunciation = self.get_initialism(word)
            method = 'letter_prons'
        elif word in self.entries:
            method = 'lex'
            if len(self.entries[word]) == 1:  ## unique, no disambig necessary
                tag, pronunciation = self.entries[word][0]  ## for now take first
            else:
                ## filter ambiguous pronunciations by first part of tag (POS):
                ## if there *is* no POS, take first in list:
                if not part_of_speech:
                    print 'WARNING: no pos tag to disambiguate pronunciation of "%s" -- take first entry in lexicon' % (
                        word)
                    tag, pronunciation = self.entries[word][0]  # take first
                else:
                    wordpos = part_of_speech.lower()  # node.attrib['pos']
                    filtered = [(tag, pron) for (tag, pron) in self.entries[word] \
                                if tag[0] == wordpos]
                    if len(filtered) == 0:
                        tag, pronunciation = self.entries[word][0]  # if no POS matches, take first anyway
                    else:
                        tag, pronunciation = filtered[0]  ## take first matching filtered dictionary entry

        else:
            if self.lts_variants == 1:
                pronunciation = self.get_oov_pronunciation(word)
            else:
                pronunciation = self.get_nbest_oov_pronunciations(word, self.lts_variants)
            if pronunciation != None:
                pronunciation = self.syllabify(word, pronunciation)
                method = 'lts'
            else:
                pronunciation = self.backoff_pronunciation
                method = 'default'

        return (pronunciation, method)

    def get_syllable_arr(self, syllables, phonestring):
        """
        Create an array of correctly formatted syllables:
        a) use phonestring to reconstruct the stress labels
        b) add a '|' at the end of each internal syllable (not after the last syllable)

        :param syllables: an array of Syllable objects, syllable strings are without stress labels
        :param phonestring: the original phonestring containing stress labels
        :return:
        """
        phone_arr = phonestring.split()
        syllable_arr = []
        start_index = 0
        for syll in syllables:
            syll_arr = syll.content.split()
            end_index = start_index + len(syll_arr)
            stressed_transcr = phone_arr[start_index:end_index]
            start_index = end_index
            if end_index == len(phone_arr):
                syllable_arr.append(' '.join(stressed_transcr))
            else:
                syllable_arr.append(' '.join(stressed_transcr) + ' |')

        return syllable_arr

    def syllabify(self, word, phonestring):
        '''
        Syllabify with maximum legal (=observed) onset.
        Take "e g z a1 m"
        return "e g | z a1 m"
        '''

        assert '|' not in phonestring
        plain = re.sub('[012]', '', phonestring)  ## remove stress marks
        plain = re.sub('_ ', '_0 ', plain) ## reconstruct voicelessness label
        plain = re.sub('_$', '_0', plain)  ## reconstruct voicelessness label
        comp_tree = self.comp_analyzer.build_compound_tree(entry.PronDictEntry(word, plain))
        syllables = []
        syllabification.syllabify_tree(comp_tree, syllables)
        res_syllables = self.get_syllable_arr(syllables, phonestring)

        return ' '.join(res_syllables)
