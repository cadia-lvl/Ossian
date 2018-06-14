#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performs a simple Guessed Part-of-speech (gpos) of entries in a dictionary.

Uses a BIN database (http://bin.arnastofnun.is/forsida/) to look up possible POS for each entry.
The results of the look up can be:
    a) one single POS for the entry -> set POS of the entry
    b) more than one POS possible for the entry -> choose one POS according to a hierarchy of POS tags
    c) the entry is not found in BIN -> do nothing

Collects statistics about the three categories.

"""

import sys
import sqlite3
import entry

#statistics
NONE = 0
SINGLE = 1
MULTI = 2

# pos map BÍN => OALD lex. Replace 'fn' with 'n' - might not be correct
POS_MAP = {'so': 'v', 'kk': 'n', 'hk': 'n', 'kvk': 'n', 'ao': 'a', 'lo': 'j', 'fn': 'n'}

# Priority list - if a word form belongs to more than one pos, chose one according to this priority list
# n > v > j > a
PRIO_1 = 'n'
PRIO_2 = 'v'
PRIO_3 = 'j'
PRIO_4 = 'a'

###
DATABASE = '<path-to-BIN-database>'

SQL_SELECT = 'SELECT field3 FROM SHsnid WHERE field5 = ?'


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)


def get_entries_from_BIN(wordform, conn):

    result = conn.execute(SQL_SELECT, (wordform,))
    entries = result.fetchall()
    # converts the pos from BÍN already at this place, change if original BÍN-pos are needed
    pos_list = set([(POS_MAP[entry[0]]) for entry in entries])
    return pos_list


def get_priority_pos(pos_list):

    if PRIO_1 in pos_list:
        return PRIO_1

    if PRIO_2 in pos_list:
        return PRIO_2

    if PRIO_3 in pos_list:
        return PRIO_3

    if PRIO_4 in pos_list:
        return PRIO_4

    else:
        return 'nil'


def create_entry(word, transcription, pos_list):
    dict_entry = entry.PronDictEntry(word, transcription)
    dict_entry.gpos = get_priority_pos(pos_list)

    return dict_entry


def collect_pos_statistics(statistics, pos_list):
    no_pos = len(pos_list)
    if no_pos == 0:
        statistics[NONE] += 1
    elif no_pos == 1:
        statistics[SINGLE] += 1
    else:
        statistics[MULTI] += 1


def print_statistics(statistics):
    print('Entries with non-ambiguous POS: ' + str(statistics[SINGLE]))
    print('Entries with ambiguous POS: ' + str(statistics[MULTI]))
    print('Entries not found in BÍN: ' + str(statistics[NONE]))


def perform_gpos_for_dict(dictionary):
    """
    Guess the part-of-speech for each entry in dictionary.
    :param dictionary: dictionary of words for which to guess POS
    :return: a list of entry objects, containing gpos information
    """

    conn = create_connection(DATABASE)
    gpos_dict = []
    statistics = {NONE: 0, SINGLE: 0, MULTI: 0}
    for line in dictionary:
        word, transcr = line.split('\t')
        pos_list = get_entries_from_BIN(word, conn)
        collect_pos_statistics(statistics, pos_list)
        entry = create_entry(word, transcr, pos_list)
        gpos_dict.append(entry)

    conn.close()
    #print_statistics(statistics)
    return gpos_dict


def perform_gpos_for_entry_list(entry_list):
    """
    Guess the part-of-speech for each PronDictEntry in entry_list, add POS-info
    to each entry ('nil' if nothing found)
    :param entry_list: list of PronDictEntries for which to guess POS

    """

    conn = create_connection(DATABASE)
    statistics = {NONE: 0, SINGLE: 0, MULTI: 0}
    for dict_entry in entry_list:
        pos_list = get_entries_from_BIN(dict_entry.word, conn)
        collect_pos_statistics(statistics, pos_list)
        dict_entry.gpos = get_priority_pos(pos_list)

    conn.close()
    #print_statistics(statistics)


def main():

    pron_dict_file = open(sys.argv[1])
    gpos_entries = perform_gpos_for_dict(pron_dict_file.readlines())


if __name__ == '__main__':
    main()

