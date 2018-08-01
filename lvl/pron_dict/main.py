#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The pron_dict module processes an ASR pronunciation dictionary, containing entries of the form 'word     transcription',
computes the necessary additional information for TTS (part-of-speech, syllabification and stress marks) and
outputs the results in the CMU format or plain syllable format.

Example:
    Input entry:

    adolfsdóttir     a: t O l f s t ou h t I r

    CMU output entry:

    ("adolfsdóttir" n (((a:) 1) ((t O l f s) 3) ((t ou h) 1) ((t I r) 3))))

    Plain syllable output entry:

    adolfsdóttir - a:.t O l f s.t ou h.t I r


"""

__license__ = 'Apache 2.0 (see: LICENSE)'

import argparse
import gpos
import syllabification
import stress
import tree_builder


from entry import PronDictEntry


def init_pron_dict(dict_file):
    pron_dict = []
    for line in dict_file:
        word, transcr = line.split('\t')
        entry = PronDictEntry(word, transcr)
        pron_dict.append(entry)
    return pron_dict


def create_tree_list(pron_dict, dict_db):
    comp_analyzer = tree_builder.CompoundAnalyzer(dict_db)
    tree_list = []
    for entry in pron_dict:
        t = comp_analyzer.build_compound_tree(entry)
        tree_list.append(t)
    return tree_list


def parse_args():
    parser = argparse.ArgumentParser(description='pronunciation dictionary for TTS', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('i', type=argparse.FileType('r'), help='ASR pronunciation dictionary')
    parser.add_argument('bin_db', help='The BÍN database (SHSnid.sql)')
    parser.add_argument('dict_db', help='The dictionary database (dictionary.db)')
   # parser.add_argument('o', type=argparse.FileType('w'), default='', help='Output: TTS pronunciation dictionary')

    return parser.parse_args()


def main():

    args = parse_args()
    pron_dict = init_pron_dict(args.i)
    bin_db = args.bin_db
    dict_db = args.dict_db

    g_pos = gpos.GPOS(bin_db)
    g_pos.perform_gpos_for_entry_list(pron_dict)

    tree_dict = create_tree_list(pron_dict, dict_db)

    syllabified = syllabification.syllabify_tree_dict(tree_dict)
    syllab_with_stress = stress.set_stress(syllabified)

    # print in cmu or in plain syllable format (syllable format not containing stress info):

    print('MNCL')
    for entry in syllab_with_stress:
        print(entry.cmu_format())

    #for entry in syllab_with_stress:
    #    print(entry.syllable_format())


if __name__ == '__main__':
    main()
