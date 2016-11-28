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


def clear_sample_tables():
    (conn, cursor) = get_connection()
    with conn:
        cursor.execute("DROP TABLE IF EXISTS Cars")
        cursor.execute("DROP TABLE IF EXISTS Friends")


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
        cursor.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
        cursor.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")


def summarize_sample_table(table_name="Cars"):
    (conn, cursor) = get_connection()
    with conn:
        cursor.execute("SELECT COUNT(*) FROM {}".format(table_name))
        count = cursor.fetchone()[0]
        print("There are {} rows in the table.".format(count))
        cursor.execute("SELECT * FROM {}".format(table_name))
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


def select_via_dict():
    # Note that the cursor has to be gotten after the row_factory is set
    # on conn.
    (conn, _) = get_connection()
    with conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cars")
        rows = cursor.fetchall()

        for row in rows:
            print("{} {} {}".format(row["Id"],
                                    row["Name"],
                                    row["Price"]))


def update_one_row():
    row_id = 1
    new_price = 90999

    (conn, cursor) = get_connection()
    with conn:
        cursor.execute("UPDATE Cars SET Price=? WHERE Id=?",
                       (new_price, row_id))
        conn.commit()
        print("Updated {} rows.".format(cursor.rowcount))


def select_with_placeholders():
    row_id = 4

    (conn, cursor) = get_connection()
    with conn:
        cursor.execute("SELECT Name, Price FROM Cars WHERE Id=:Id",
                       {"Id": row_id})
        conn.commit()

        row = cursor.fetchone()
        print("Name = {}, Price = {}".format(row[0], row[1]))


def display_metadata():
    (conn, cursor) = get_connection()
    with conn:
        cursor.execute('PRAGMA table_info(Cars)')
        data = cursor.fetchall()

        for d in data:
            print("{} {} {}".format(d[0], d[1], d[2]))


def display_table_prettily():
    (conn, cursor) = get_connection()
    with conn:
        cursor.execute("SELECT * FROM Cars")
        col_names = [cn[0] for cn in cursor.description]
        rows = cursor.fetchall()

        print("{:2} {:10} {}".format(col_names[0],
                                col_names[1],
                                col_names[2]))
        print("{:2} {:10} {}".format("-"*2,
                                     "-"*10,
                                     "-"*7))
        for row in rows:
            print("{:2} {:10} {}".format(row[0],
                                    row[1],
                                    row[2]))


def dump_to_file():
    (conn, cursor) = get_connection()
    with conn:
        data = '\n'.join(conn.iterdump())

    f = open('cars.sql', 'w')
    with f:
        f.write(data)


def create_table_from_file():
    data = None
    f = open('cars.sql', 'r')
    with f:
        data = f.read()

    (conn, cursor) = get_connection()
    with conn:
        cursor.executescript(data)


def insert_within_a_transaction():
    """
    The sqlite3 library defaults to 'None'.  For the different options,
    see https://www.sqlite.org/isolation.html.
    :return:
    """
    conn = None

    try:
        conn = sqlite3.connect("sample.db", isolation_level="DEFERRED")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Friends")
        cursor.execute("CREATE TABLE Friends(Id INTEGER PRIMARY KEY, Name TEXT)")
        cursor.execute("INSERT INTO Friends(Name) VALUES ('Tom')")
        cursor.execute("INSERT INTO Friends(Name) VALUES ('Rebecca')")
        cursor.execute("INSERT INTO Friends(Name) VALUES ('Jim')")
        cursor.execute("INSERT INTO Friends(Name) VALUES ('Robert')")

        conn.commit()
    except sqlite3.Error, e:
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
    clear_sample_tables()
    create_sample_table()
    summarize_sample_table()

    print("\n-- Recreate it from a python variable:")
    clear_sample_tables()
    create_sample_table_from_variable()
    summarize_sample_table()

    print("\n-- Again with a single transaction:")
    clear_sample_tables()
    create_via_transaction()
    summarize_sample_table()

    print("\n-- Now with a dictionary based cursor:")
    select_via_dict()

    print("\n-- Do an update:")
    update_one_row()
    summarize_sample_table()

    print("\n-- Do another update; this time with placeholders:")
    select_with_placeholders()

    print("\n-- Let's get some metadata:")
    display_metadata()

    print("\n-- Print the table using nicer formatting:")
    display_table_prettily()

    print("\n-- Now dump table to file:")
    dump_to_file()

    print("\n-- Read that file in:")
    clear_sample_tables()
    create_table_from_file()
    display_table_prettily()

    print("\n-- Use a transaction to create another table:")
    insert_within_a_transaction()
    summarize_sample_table("Friends")

if __name__ == "__main__":
    main()










