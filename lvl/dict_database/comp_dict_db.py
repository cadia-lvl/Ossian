#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Provides a connection to the compound database

"""

import sys
import sqlite3
import entry


DATABASE = '<path-to-database>'

SQL_SELECT = 'SELECT * FROM compound_transcr'
SQL_SELECT_COMPOUND = 'SELECT * FROM compound_transcr WHERE word = ?'
SQL_SELECT_MODIFIERS = 'SELECT * FROM compound_transcr WHERE modifier = ?'
SQL_SELECT_HEADS = 'SELECT * FROM compound_transcr WHERE head = ?'


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)


def get_compound(wordform, conn):
    result = conn.execute(SQL_SELECT_COMPOUND, (wordform,))
    compound = result.fetchone()
    if compound:
        return compound[1], compound[2], compound[3]


def create_map(comp_list, key_index, val_index):

    comp_map = {}
    for comp in comp_list:
        if comp[key_index] in comp_map:
            comp_map[comp[key_index]].append(comp[val_index])
        else:
            comp_map[comp[key_index]] = [val_index]

    return comp_map


def get_modifier_map():
    conn = open_connection()
    result = conn.execute(SQL_SELECT)
    compounds = result.fetchall()
    conn.close()
    return create_map(compounds, 2, 3)


def get_head_map():
    conn = open_connection()
    result = conn.execute(SQL_SELECT)
    compounds = result.fetchall()
    conn.close()
    return create_map(compounds, 3, 2)


def open_connection():
    return create_connection(DATABASE)


