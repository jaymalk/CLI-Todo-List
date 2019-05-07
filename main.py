# /anaconda3/bin/python3

import sqlite3
import sys
import argparse
import datetime

# ==== ==== ==== ==== ==== ====
# Global path to accomodate 'sed' resetting
path = "/Users/rajbirmalik/Documents/.db/tasks.db"

# ==== ==== ==== ==== ==== ====
# Setting the parser
def set_parser():
    parser = argparse.ArgumentParser(
        description="For performing list operations from command line.")
    parser.add_argument('-all', action="store_true",
                        dest='list', default=False, help='Show the list.')
    parser.add_argument('-new', action="store_true",
                        dest='enter', default=False, help='New entry')
    parser.add_argument('-rm', action="store_true",
                        dest='delete', default=False, help='Delete entry')
    parser.add_argument('-more', action="store_true",
                        dest='detail', default=False, help='Show task detail')
    parser.add_argument('-edit', action="store_true",
                        dest='edit', default=False, help='Edit task detail')
    # Limiting the list items in display
    parser.add_argument('-lmt', action="store",
                        dest='limit', default=-1,
                        type=int, help='Limiting the display of tasks')
    parser.add_argument('-sort', action="store_true",
                        dest='dl', default=False, help='Display sorted by deadline')
    return parser

# ==== ==== ==== ==== ==== ====
# Function for comaparing dates (item:4 in database)
def date_compare(x):
    if x is None:
        return 90000000
    y = list(map(int, x.split('/')))
    return y[0]*1000000+y[1]*10000+(y[2] if y[2] > 100 else 2000+y[2])

# Function for printing the data
def print_tasks(cursor, limit, deadline):
    if limit >= 0:
        cursor.execute("SELECT * FROM todos LIMIT "+str(limit))
    else:
        cursor.execute("SELECT * FROM todos")
    result = cursor.fetchall()
    if deadline:
        result.sort( key=lambda y : date_compare(y[4]) )
        print("%3s | %30s | %10s | %10s"%('ID', 'Title', 'Date Set', 'Deadline'))
        print('-'*62)
        for categories in result:
            print("%3d | %30s | %10s | %10s"%(categories[0], categories[1], categories[3], categories[4]))
    else:
        print("%3s | %30s | %10s"%('ID', 'Title', 'Date Set'))
        print('-'*49)
        for categories in result:
            print("%3d | %30s | %10s"%(categories[0], categories[1], categories[3]))

# ==== ==== ==== ==== ==== ====
# Function for printing the data
def print_detail(cursor):
    # Setting ID
    ind = int(input("Enter ID : "))
    cursor.execute("SELECT * FROM todos WHERE id="+str(ind))
    result = cursor.fetchall()
    # Checking if ID exists
    if not result:
        print("ID doesn't exist.")
        return
    result = result[0]
    print('-'*40)
    print("%10s : %s"%('Title', result[1]))
    print('-'*40)
    print("%10s : %s"%('Detail', result[2]))
    print('-'*40)
    print("%10s : %s"%('Date Set', result[3]))
    print('-'*40)
    if result[4] is None:
        _ds = 'Not Set'
        _ts = ''
    elif result[5] is None:
        _ds = result[4]
        _ts = ''
    else:
        _ds = result[4]
        _ts = result[5]
    print("%10s : %s %s"%('Deadline', _ds, _ts))
    print('-'*40)

# ==== ==== ==== ==== ==== ====
# Function for entering a new entry.
def enter_task(cursor):
    # Setting ID
    ind = int(input("Enter ID : "))
    # Checking for ID uniqueness
    cursor.execute("SELECT id FROM todos WHERE id="+str(ind))
    if cursor.fetchall():
        print("ID already exists.")
        return
    # Setting title
    title = input("Title : ")
    # Setting detail
    detail = input("Detail : ")
    # Setting final date (optional)
    date_set = input("Enter date (deadline): ")
    if date_set == '':
        date_set = None
    # Setting final time (optional)
    time = input("Enter time (deadline): ")
    if time == '':
        time = None
    # Creating Date (current)
    curr = datetime.datetime.now()
    date = str(curr.day)+"/"+str(curr.month)+"/"+str(curr.year)
    # Executing the command
    cursor.execute("insert into todos(id, title, detail, date_labeled, date_set, time_set) values (?, ?, ?, ?, ?, ?);"
                   , (ind, title, detail, date, date_set, time))

# ==== ==== ==== ==== ==== ====
# Function for deleting an entry
def delete_task(cursor):
    # Getting the ID
    ind = int(input("Enter ID : "))
    # Checking if ID exists
    cursor.execute("SELECT id FROM todos WHERE id="+str(ind))
    if not cursor.fetchall():
        print("ID doesn't exist.")
        return
    # Executing the command
    cursor.execute("DELETE FROM todos WHERE id="+str(ind))

# ==== ==== ==== ==== ==== ====
# Function for editing an entry
def edit_task(cursor):
    # Getting the ID
    ind = int(input("Enter ID : "))
    # Checking if ID exists
    cursor.execute("SELECT id FROM todos WHERE id="+str(ind))
    if not cursor.fetchall():
        print("ID doesn't exist.")
        return
    # Getting current data
    cursor.execute("SELECT * FROM todos WHERE id="+str(ind))
    result = cursor.fetchall()
    result = result[0]
    # Instruction message
    print("Enter details. (Press enter to retain)")
    # Taking new information
    # Setting title
    title = input("Title : ")
    if title.replace(' ', '') == '':
        title = result[1]
    # Setting detail
    detail = input("Detail : ")
    if detail.replace(' ', '') == '':
        detail = result[2]
    # Setting final date (optional)
    date_set = input("Enter date (deadline): ")
    if date_set.replace(' ', '') == '':
        date_set = result[4]
    elif date_set.replace(' ', '') == 'NA':
        date_set = None
    # Setting final time (optional)
    time = input("Enter time (deadline): ")
    if time.replace(' ', '') == '':
        time = result[5]
    elif time.replace(' ', '') == 'NA':
        time = None
    # Executing the command
    cursor.execute("UPDATE todos SET title=?, detail=?, date_labeled=?, date_set=?, time_set=? WHERE id=?"
                   , (title, detail, result[3], date_set, time, ind))

# Main function
def main():
    # ---- ---- ---- ---- ---- ---- ----
    # Setting up the connection with the database
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    except Exception as _e:
        print(_e.__doc__)
        exit(0)
    # ---- ---- ---- ---- ---- ---- ----
    # Creating table if it doesn't exist
    table_schema = """CREATE TABLE IF NOT EXISTS todos 
                        (
                            id INT PRIMARY KEY NOT NULL,
                            title TEXT NOT NULL,
                            detail TEXT NOT NULL,
                            date_labeled DATE NOT NULL,
                            date_set DATE DEFAULT NULL,
                            time_set TIME DEFAULT NULL
                        );"""
    cursor.execute(table_schema)
    # ---- ---- ---- ---- ---- ---- ----
    # Setting up the CLI parser
    parser = set_parser()
    # ---- ---- ---- ---- ---- ---- ----
    # Working with parsed arguments
    if len(sys.argv) == 1:
        # No arguments
        print("Tool for handeling todo-lists.")
        return
    # ---- ---- ---- ---- ---- ---- ----
    # Try block
    try:
    # Parsing stage
        parse = parser.parse_args(sys.argv[1:])
        # List option set
        if parse.list:
            print_tasks(cursor, parse.limit, parse.dl)
        # Detail option set
        elif parse.detail:
            print_detail(cursor)
        # Enter option set
        elif parse.enter:
            enter_task(cursor)
        # Delete option set
        elif parse.delete:
            delete_task(cursor)
        elif parse.edit:
            edit_task(cursor)
        # No option set
        else:
            print("Tool for handeling todo-lists.")
    # Exception handeling
    except Exception as _e:
        print(_e.__doc__)
        # print('Error')
    # ---- ---- ---- ---- ---- ---- ----
    # Committing changes and exiting
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
