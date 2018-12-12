#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tokenising and text normalising for Icelandic.

Author: Anna B. Nikulásdóttir
Reykjavík University, 2018
https://lvl.ru.is/

"""

from processors.UtteranceProcessor import SUtteranceProcessor, Element

class LVL_TextaHaukur(SUtteranceProcessor):

    def __init__(self, processor_name='text_norm', target_nodes='//utt', split_attribute='text'):

        self.processor_name = processor_name
        self.target_nodes = target_nodes
        self.split_attribute = split_attribute

        super(LVL_TextaHaukur, self).__init__()


    def process_utterance(self, utt):

        print('target nodes: %s'%(utt.xpath(self.target_nodes)))
        for node in utt.xpath(self.target_nodes):
            print(str(node))
            assert node.has_attribute(self.split_attribute)
            text_to_normalise = node.get(self.split_attribute)
            print(text_to_normalise)

        #######################################################
        #
        #   TEXTAHAUKUR COMES HERE
        #
        #######################################################

        #    #normalised = self.normalise(to_split)
        #    normalised = self.normalise_ice(to_split)
        #    child_chunks = self.splitting_function(normalised)

        #    for chunk in child_chunks:
                # print '=='
                # print chunk
        #        child = Element(self.child_node_type)
        #        child.set(self.split_attribute, chunk)

        #        if self.add_token_classes:
        #            token_class = self.classify_token(chunk)
        #            # print token_class
        #            child.set(self.class_attribute, token_class)

        #        if self.add_safetext:
        #            token_safetext = self.safetext_token(chunk)
        #            child.set(self.safetext_attribute, token_safetext)

        #        node.add_child(child)