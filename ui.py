import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from tkinter import *
from tkinter import ttk


def hello(event=None):
    print('hello')


def runAdd():
    def add():
        entries_get = []
        for i in range(len(entries)):
            entries_get.append(entries[i].get())
        entries_get = tuple(entries_get)
        cur.execute(f"INSERT INTO {current_state} {'(%s)' % ', '.join(map(str, colnames))} VALUES {entries_get};")
        add_window.destroy()
        printTable(current_state)

    global current_state
    cur.execute(f"SELECT * FROM {current_state} LIMIT 0;")
    colnames = [cols[0] for cols in cur.description]
    colnames.pop(0)

    add_window = Toplevel(main)
    add_window.title("Add")
    add_window.resizable(False, False)
    add_window.iconphoto(False, PhotoImage(file="src/logo.png"))

    entries = []

    count = 0
    for col in colnames:
        label = Label(add_window, text=col)
        label.grid(row=count, column=0)

        entries.append(Entry(add_window, width=20, font="Arial 9"))
        entries[-1].grid(row=count, column=1)

        count += 1

    add_b = Button(add_window, text="Add", command=add, width=10)
    add_b.grid(row=count, column=0, columnspan=2, pady=5)

    colnames = tuple(colnames)

    add_window.mainloop()


def runEdit():
    def edit():
        query = f"UPDATE {current_state} SET "
        for i in range(len(colnames)):
            if i == len(colnames) - 1:
                query += f"{colnames[i]} = '{entries[i].get()}' "
            else:
                query += f"{colnames[i]} = '{entries[i].get()}', "
        query += f"WHERE {cond[0]} = {cond[1]};"

        cur.execute(query)
        edit_window.destroy()
        printTable(current_state)

    global current_state
    cond = []

    cur.execute(f"SELECT * FROM {current_state} LIMIT 0;")
    colnames = [cols[0] for cols in cur.description]
    cond.append(colnames[0])
    colnames.pop(0)

    selected = tab.focus()
    if len(selected) == 0:
        return
    selected = list(tab.item(selected)['values'])
    cond.append(selected[0])
    selected.pop(0)

    edit_window = Toplevel(main)
    edit_window.title("Edit")
    edit_window.resizable(False, False)
    edit_window.iconphoto(False, PhotoImage(file="src/logo.png"))

    entries = []

    count = 0
    i = 0
    for col in colnames:
        label = Label(edit_window, text=col)
        label.grid(row=count, column=0)

        entries.append(Entry(edit_window, width=20, font="Arial 9"))
        entries[-1].insert(0, str(selected[i]))
        i += 1
        entries[-1].grid(row=count, column=1)

        count += 1

    edit_b = Button(edit_window, text="Edit", command=edit, width=10)
    edit_b.grid(row=count, column=0, columnspan=2, pady=5)


def runDelete():
    global current_state

    cur.execute(f"SELECT * FROM {current_state} LIMIT 0;")
    colnames = [cols[0] for cols in cur.description]

    selected = tab.focus()
    if len(selected) == 0:
        return
    selected = list(tab.item(selected)['values'])

    cur.execute(f"DELETE FROM {current_state} WHERE {colnames[0]} = {selected[0]};")
    printTable(current_state)


def runClearAll():
    global current_state

    cur.execute(f"DELETE * FROM {current_state}")
    printTable(current_state)


def runExit():
    exit()


def connectToDatabase():
    global flag_connect
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='ifruits',
            user='bool',
            password='bool'
        )
    except psycopg2.OperationalError:
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='bool',
            password='bool'
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE ifruits;")
    flag_connect = True
    entrance.destroy()


def printTable(event=None):
    global current_state
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
        tab.heading(col, text=col, anchor=CENTER)

    iid_counter = 0
    # if event == "track_list":
    #     cur.execute(
    #         "SELECT t_l.track_id AS Track_ID, t_l.track_title AS Title, al.album_title AS Album, t_l.duration AS Duration, aut.name AS Author FROM track_list t_l LEFT JOIN album al ON t_l.album_id = al.album_id LEFT JOIN author aut ON t_l.author_id = aut.author_id;")
    # elif event == "my_music":
    #     cur.execute(
    #         "SELECT my.mus_id, iu.username, t_l.track_title FROM my_music my JOIN iuser iu ON my.user_id = iu.user_id JOIN track_list t_l ON my.track_id = t_l.track_id;")
    # else:
    cur.execute(f"SELECT * FROM {event} ORDER BY {colnames[0]};")
    result = cur.fetchall()
    for col in result:
        tab.insert(parent='', index='end', text='', iid=iid_counter, values=list(col))
        iid_counter += 1

    current_state = event


# create db
entrance = Tk()
entrance.title("Logging...")
entrance.geometry("300x150")
entrance.resizable(False, False)
entrance.iconphoto(False, PhotoImage(file="src/logo.png"))
flag_connect = False

entrance_frame = Frame(entrance)

login_button = Button(entrance_frame, text="Log in to the database", command=connectToDatabase)
login_button.pack(anchor=CENTER)

hint_text = Label(text="NOTE: If database doesn't exist, it would be created", font="Arial 9")
hint_text.pack(side=BOTTOM)

entrance_frame.pack(side=TOP, expand=True)

entrance.mainloop()

if not flag_connect:
    exit(0)

conn = psycopg2.connect(
    host='localhost',
    database='ifruits',
    user='bool',
    password='bool'
)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
tables = [table[0] for table in cur.fetchall()]

current_user = None
current_state = "track_list"

main = Tk()
main.title("tunes")
main.geometry("1000x500")
main.resizable(False, False)
main.iconphoto(False, PhotoImage(file="src/logo.png"))

option_frame = Frame(main)

choose = StringVar(main)
choose.set("Table")
option = OptionMenu(option_frame, choose, *tables, command=printTable)
option.pack(side=LEFT)

# main buttons
add_button = Button(option_frame, text="Add", command=runAdd, width=10)
add_button.pack(side=LEFT)

edit_button = Button(option_frame, text="Edit", command=runEdit, width=10)
edit_button.pack(side=LEFT)

delete_button = Button(option_frame, text="Delete", command=runDelete, width=10)
delete_button.pack(side=LEFT)

add_button = Button(option_frame, text="Clear all", command=runClearAll, width=10)
add_button.pack(side=LEFT)

add_button = Button(option_frame, text="Find in", command=hello, width=10)
add_button.pack(side=LEFT)

exit_button = Button(option_frame, text="Exit", command=runExit, width=10)
exit_button.pack(side=RIGHT)

option_frame.pack(side=TOP, fill=X)

# table
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

print(current_state)
printTable(current_state)
main.mainloop()
cur.close()
print("Ended")
