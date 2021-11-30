import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from tkinter import *
from tkinter import ttk


def hello(event=None):
    print('hello')


def printTable(event=None):
    cur.execute(f"SELECT * FROM {event} LIMIT 0;")
    colnames = [cols[0] for cols in cur.description]
    print(colnames)

    for item in tab.get_children():
        tab.delete(item)

    tab.heading("#0", text="")
    tab.column("#0", anchor=W, width=0, stretch=False)

    tab['columns'] = colnames

    for col in colnames:
        tab.column(col)
    for col in colnames:
        tab.heading(col, text=col, anchor="center")

    iid_counter = 0
    cur.execute(f"SELECT * FROM {event}")
    result = cur.fetchall()
    for col in result:
        tab.insert(parent='', index='end', text='', iid=iid_counter, values=list(col))
        iid_counter += 1


conn = psycopg2.connect(
    host='localhost',
    database='ifruits',
    user='bool',
    password='bool'
)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
tables = [table[0] for table in cur.fetchall()]

# try:
#     cur.execute("""CREATE DATABASE tunes;""")
# except psycopg2.errors.DuplicateDatabase:
#     print("Already here")
#
# conn = psycopg2.connect(
#     host='localhost',
#     database='tunes',
#     user='bool',
#     password='bool'
# )


main = Tk()
main.title("tunes")
main.geometry("1300x500")

option_frame = Frame(main)

choose = StringVar(main)
choose.set("Table")
option = OptionMenu(option_frame, choose, *tables, command=printTable)
option.pack(side=LEFT)

# main buttons
add_button = Button(option_frame, text="Add", command=hello, width=10)
add_button.pack(side=LEFT)

edit_button = Button(option_frame, text="Edit", command=hello, width=10)
edit_button.pack(side=LEFT)

delete_button = Button(option_frame, text="Delete", command=hello, width=10)
delete_button.pack(side=LEFT)

add_button = Button(option_frame, text="Clear all", command=hello, width=10)
add_button.pack(side=LEFT)

add_button = Button(option_frame, text="Find in", command=hello, width=10)
add_button.pack(side=LEFT)

option_frame.pack(side=TOP)

tree_frame = Frame(main)
tab = ttk.Treeview(tree_frame)
tree_scroll_y = Scrollbar(main, orient=VERTICAL)
tree_scroll_x = Scrollbar(main, orient=HORIZONTAL)

tab.config(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
tree_scroll_y.config(command=tab.yview)
tree_scroll_x.config(command=tab.xview)

tree_scroll_y.pack(side=RIGHT, fill=Y)
tree_scroll_x.pack(side=BOTTOM, fill=X)
tab.pack(fill=BOTH, expand=1)

tree_frame.pack(side=TOP, fill=BOTH, expand=1)

printTable("track_list")
main.mainloop()
cur.close()
print("Ended")
