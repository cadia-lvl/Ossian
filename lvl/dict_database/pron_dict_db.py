

import sys
import sqlite3


class PronunciationDB:

    def __init__(self, db):
        self.DATABASE = db
        self.init_statements()

    def init_statements(self):
        self.SQL_CREATE = 'CREATE TABLE IF NOT EXISTS frob(id INTEGER PRIMARY KEY, word TEXT, ' \
                     'transcript TEXT) '

        self.SQL_INSERT = 'INSERT OR IGNORE INTO frob(word, transcript) VALUES(?, ?)'
        self.SQL_SELECT_TRANSCR = 'SELECT * FROM frob'

    def create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            print(e)

        return None

    def populate_database(self, dict_list):
        db = self.create_connection(self.DATABASE)
        db.execute(self.SQL_CREATE)
        for entry in dict_list:
            db.execute(self.SQL_INSERT, (entry[0], entry[1]))

        db.commit()

    def get_transcriptions_map(self):
        conn = self.create_connection(self.DATABASE)
        result = conn.execute(self.SQL_SELECT_TRANSCR)
        transcriptions = result.fetchall()
        transcr_dict = {}
        for transcr in transcriptions:
            transcr_dict[transcr[1]] = transcr[2]

        return transcr_dict


def main():

    frob = sys.argv[1]
    db_path = sys.argv[2]

    frob_list = []
    for line in open(frob).readlines():
        word, transcr = line.split('\t')
        frob_list.append([word, transcr.strip()])

    pron_db = PronunciationDB(db_path)
    pron_db.populate_database(frob_list)


if __name__ == '__main__':
    main()
