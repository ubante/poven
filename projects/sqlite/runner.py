#!/usr/bin/env python

import sys

import sqlite3

'''
http://zetcode.com/db/sqlitepythontutorial/
'''


def print_versions():
    sv = sqlite3.version
    ssv = sqlite3.sqlite_version

    print("Using sqlite v{} and sqlite3 v{}\n".format(sv, ssv))


def get_connection():
    conn = sqlite3.connect("sample.db")
    cursor = conn.cursor()

    return conn, cursor


def connect_db():
    conn = None

    # could 'with conn' here
    try:
        conn = sqlite3.connect("sample.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SQLITE_VERSION")
        data = cursor.fetchone()
    except sqlite3.Error as e:
        print("FATAL: {}".format(e.args[0]))
        sys.exit()
    finally:
        if conn:
            conn.close()

    print("SQLite version is {}".format(data))


def clear_sample_table():
    (conn, cursor) = get_connection()

    with conn:
        cursor.execute("DROP TABLE IF EXISTS Cars")


def create_sample_table():
    (conn, cursor) = get_connection()

    with conn:
        cursor.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
        cursor.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
        cursor.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
        cursor.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
        cursor.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
        cursor.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
        cursor.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
        cursor.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
        cursor.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")


def summarize_sample_table():
    (conn, cursor) = get_connection()

    with conn:
        cursor.execute("SELECT COUNT(*) FROM Cars")
        count = cursor.fetchone()[0]
        print("There are {} cars in the table.".format(count))
        cursor.execute("SELECT * FROM Cars")
        rows = cursor.fetchall()
        for row in rows:
            print(row)


def create_sample_table_from_variable():
    cars = (
        (1, 'Audi', 52642),
        (2, 'Mercedes', 57127),
        (3, 'Skoda', 9000),
        (4, 'Volvo', 29000),
        (5, 'Bentley', 350000),
        (6, 'Citroen', 21000),
        (7, 'Hummer', 41400),
        (8, 'Volkswagen', 21600)
    )

    (conn, cursor) = get_connection()

    with conn:
        cursor.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
        cursor.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)


def create_via_transaction():
    try:
        (conn, cursor) = get_connection()
        cursor.executescript("""
            DROP TABLE IF EXISTS Cars;
            CREATE TABLE Cars(Id INT, Name TEXT, Price INT);
            INSERT INTO Cars VALUES(1,'Audi',52642);
            INSERT INTO Cars VALUES(2,'Mercedes',57127);
            INSERT INTO Cars VALUES(3,'Skoda',9000);
            INSERT INTO Cars VALUES(4,'Volvo',29000);
            INSERT INTO Cars VALUES(5,'Bentley',350000);
            INSERT INTO Cars VALUES(6,'Citroen',21000);
            INSERT INTO Cars VALUES(7,'Hummer',41400);
            INSERT INTO Cars VALUES(8,'Volkswagen',21600);
            """)
        conn.commit()

    except sqlite3.Error as e:
        if conn:
            conn.rollback()

        print("FATAL: {}".format(e.args[0]))
        sys.exit()

    finally:
        if conn:
            conn.close()

def main():
    print_versions()

    print("-- Create the cars table the simplest way:")
    clear_sample_table()
    create_sample_table()
    summarize_sample_table()

    print("\n-- Recreate it from a python variable:")
    clear_sample_table()
    create_sample_table_from_variable()
    summarize_sample_table()

    print("\n-- Again with a single transaction:")
    clear_sample_table()
    create_via_transaction()
    summarize_sample_table()

if __name__ == "__main__":
    main()










