#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tokenising and text normalising for Icelandic.

Author: Anna B. Nikulásdóttir
Reykjavík University, 2018
https://lvl.ru.is/

"""

import sys
import default.const as c
from naive import naive_util
from processors.UtteranceProcessor import SUtteranceProcessor, Element
from lvl.normalizing.normalizer import Normalizer

try:
    import regex as new_regex
except ImportError:
    sys.exit('Please install "regex": https://pypi.python.org/pypi/regex ')


class LVL_TextaHaukur(SUtteranceProcessor):

    def __init__(self, processor_name='text_norm', target_nodes='//utt', child_node_type='token',
                 class_attribute='token_class', safetext_attribute='safetext',
                 class_patterns=[('space', '\A\s+\Z'), ('punctuation', '\A[\.\,\;\!\?\s]+\Z')],
                 default_class='word',
                 add_token_class=True, add_terminal_tokens=True, add_safetext=True,
                 lowercase_safetext=True,
                 split_attribute='text'):

        self.processor_name = processor_name
        self.target_nodes = target_nodes
        self.split_attribute = split_attribute
        self.class_attribute = class_attribute
        self.safetext_attribute = safetext_attribute
        self.class_patterns = [(name, new_regex.compile(patt)) for (name, patt) in class_patterns]
        self.default_class = default_class
        self.child_node_type = child_node_type

        self.add_token_classes = add_token_class
        self.add_terminal_tokens = add_terminal_tokens
        self.add_safetext = add_safetext
        self.lowercase_safetext = lowercase_safetext

        self.normalizer = Normalizer()

        super(LVL_TextaHaukur, self).__init__()


    def process_utterance(self, utt):

        print('target nodes: %s'%(utt.xpath(self.target_nodes)))
        node_count = 0
        for node in utt.xpath(self.target_nodes):
            node_count += 1
            assert node.has_attribute(self.split_attribute)
            text_to_normalise = node.get(self.split_attribute)
            print(text_to_normalise)
            normalised = self.normalizer.normalize(text_to_normalise)
            # get tokenized arr from normalizer, don't split here again
            child_chunks = self.splitting_function(normalised)

            for chunk in child_chunks:
                # print '=='
                # print chunk
                child = Element(self.child_node_type)
                child.set(self.split_attribute, chunk)

                if self.add_token_classes:
                    token_class = self.classify_token(chunk)
                    # print token_class
                    child.set(self.class_attribute, token_class)

                if self.add_safetext:
                    token_safetext = self.safetext_token(chunk)
                    child.set(self.safetext_attribute, token_safetext)

                node.add_child(child)

    def do_training(self, speech_corpus, text_corpus):
        print("LVL_TextaHaukur requires no training")

    def classify_token(self, token):
        ## LVL: do we need to change this according to resuts from Haukur?
        ## Special handling of terminal token:
        if token == c.TERMINAL:
            return c.TERMINAL
        for (item_class, pattern) in self.class_patterns:
            if pattern.match(token):
                return item_class
        ## if we have got this far, none of patterns matched -- return default:
        return self.default_class

    def safetext_token(self, instring):

        ## Special handling of terminal token:
        if instring == c.TERMINAL:
            return c.TERMINAL
        else:
            if self.lowercase_safetext == 'True':
                return naive_util.safetext(instring.lower())
            else:
                return naive_util.safetext(instring)

    def splitting_function(self, instring):
        tokens = instring.split()
        tokens = [t for t in tokens if t]
        if self.add_terminal_tokens:
            tokens = [c.TERMINAL] + tokens + [c.TERMINAL]
        return tokens