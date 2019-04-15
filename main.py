# usr/bin/python3

import sqlite3
import sys
import argparse
import datetime

def set_parser():
    parser = argparse.ArgumentParser(
        description="For performing list operations from command line.")
    parser.add_argument('-list', action="store_true",
                        dest='list', default=False, help='Show the list.')
    parser.add_argument('-enter', action="store_true",
                        dest='enter', default=False, help='New entry')
    parser.add_argument('-delete', action="store_true",
                        dest='delete', default=False, help='Delete entry')
    parser.add_argument('-detail', action="store_true",
                        dest='detail', default=False, help='Show a task detail')
    # Limiting the list items in display
    parser.add_argument('-lmt', action="store",
                        dest='limit', default=-1,
                        type=int, help='Limiting the display of tasks')
    return parser

# Function for printing the data
def print_tasks(cursor, limit):
    if limit >= 0:
        cursor.execute("SELECT * FROM todos LIMIT "+str(limit))
    else:
        cursor.execute("SELECT * FROM todos")
    result = cursor.fetchall()
    print("%3s | %30s | %10s"%('ID', 'Title', 'Date Set'))
    print('-'*49)
    for categories in result:
        print("%3d | %30s | %10s"%(categories[0], categories[1], categories[3]))

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
    print("%10s : %s"%('Title', result[1]))
    print("%10s : %s"%('Detail', result[2]))
    print("%10s : %s"%('Date Set', result[3]))
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

# Main function
def main():
    # Setting up the connection with the database
    connection = sqlite3.connect("/Users/rajbirmalik/Documents/.db/tasks.db")
    cursor = connection.cursor()
    # Setting up the CLI parser
    parser = set_parser()
    # Working with parsed arguments
    if len(sys.argv) == 1:
        # No arguments
        print("Tool for handeling todo-lists.")
        return
    # Try block
    try:
    # Parsing stage
        parse = parser.parse_args(sys.argv[1:])
        # List option set
        if parse.list:
            print_tasks(cursor, parse.limit)
        # Detail option set
        elif parse.detail:
            print_detail(cursor)
        # Enter option set
        elif parse.enter:
            enter_task(cursor)
        # Delete option set
        elif parse.delete:
            delete_task(cursor)
        # No option set
        else:
            print("Tool for handeling todo-lists.")
    # Exception handeling
    except:
        print('Error')

    # Committing changes and exiting
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
