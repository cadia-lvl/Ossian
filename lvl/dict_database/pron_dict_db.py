

import sys
import sqlite3


DATABASE = '</PATH/TO/DATABASE>'

SQL_CREATE = 'CREATE TABLE IF NOT EXISTS frob(id INTEGER PRIMARY KEY, word TEXT, ' \
                     'transcript TEXT) '

SQL_INSERT = 'INSERT OR IGNORE INTO frob(word, transcript) VALUES(?, ?)'

SQL_SELECT_TRANSCR = 'SELECT * FROM frob'


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def populate_database(dict_list):
    db = create_connection(DATABASE)
    db.execute(SQL_CREATE)
    for entry in dict_list:
        db.execute(SQL_INSERT, (entry[0], entry[1]))

    db.commit()


def get_transcriptions_map():
    conn = create_connection(DATABASE)
    result = conn.execute(SQL_SELECT_TRANSCR)
    transcriptions = result.fetchall()
    transcr_dict = {}
    for transcr in transcriptions:
        transcr_dict[transcr[1]] = transcr[2]

    return transcr_dict


def main():

    frob = sys.argv[1]

    frob_list = []
    for line in open(frob).readlines():
        word, transcr = line.split('\t')
        frob_list.append([word, transcr.strip()])

    populate_database(frob_list)


if __name__ == '__main__':
    main()
