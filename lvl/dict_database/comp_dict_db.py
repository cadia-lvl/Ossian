#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provides a connection to the compound database

"""

import sqlite3
<<<<<<< HEAD
import lvl.pron_dict.entry
=======
>>>>>>> master

class Comp_DB:

    def __init__(self, db):
        self.DATABASE = db
        self.init_statements()

    def init_statements(self):

        self.SQL_SELECT = 'SELECT * FROM compound_transcr'
        self.SQL_SELECT_COMPOUND = 'SELECT * FROM compound_transcr WHERE word = ?'
        self.SQL_SELECT_MODIFIERS = 'SELECT * FROM compound_transcr WHERE modifier = ?'
        self.SQL_SELECT_HEADS = 'SELECT * FROM compound_transcr WHERE head = ?'

    def create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            print(e)

    def get_compound(self, wordform, conn):
        result = conn.execute(self.SQL_SELECT_COMPOUND, (wordform,))
        compound = result.fetchone()
        if compound:
            return compound[1], compound[2], compound[3]

    def create_map(self, comp_list, key_index, val_index):

        comp_map = {}
        for comp in comp_list:
            if comp[key_index] in comp_map:
                comp_map[comp[key_index]].append(comp[val_index])
            else:
                comp_map[comp[key_index]] = [val_index]

        return comp_map

    def get_modifier_map(self):
        conn = self.open_connection()
        result = conn.execute(self.SQL_SELECT)
        compounds = result.fetchall()
        conn.close()
        return self.create_map(compounds, 2, 3)

    def get_head_map(self):
        conn = self.open_connection()
        result = conn.execute(self.SQL_SELECT)
        compounds = result.fetchall()
        conn.close()
        return self.create_map(compounds, 3, 2)

    def open_connection(self):
        return self.create_connection(self.DATABASE)


