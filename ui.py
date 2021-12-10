import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from tkinter import *
from tkinter import ttk

import queries


def hello():
    print("hello")


def runAdd():
    def add():
        entries_get = []
        for i in range(len(entries)):
            entries_get.append(entries[i].get())
        entries_get = tuple(entries_get)
        cur.execute(f"INSERT INTO {current_state} {'(%s)' % ', '.join(map(str, colnames))} VALUES {entries_get};")
        conn.commit()
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
        global current_user

        query = f"UPDATE {current_state} SET "
        for i in range(len(colnames)):
            if i == len(colnames) - 1:
                query += f"{colnames[i]} = '{entries[i].get()}' "
            else:
                query += f"{colnames[i]} = '{entries[i].get()}', "
        query += f"WHERE {cond[0]} = {cond[1]};"

        if current_state == "iuser":
            current_user = entries[0].get()
        cur.execute(query)
        conn.commit()
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
    conn.commit()
    printTable(current_state)


def runClearAll():
    global current_state

    cur.execute(f"DELETE FROM {current_state};")
    conn.commit()
    printTable(current_state)


def runFindIn():
    def find():
        for item in tab.get_children():
            tab.delete(item)

        tab.heading("#0", text="")
        tab.column("#0", anchor=W, width=0, stretch=False)

        tab["columns"] = colnames

        for col in colnames:
            tab.column(col)
        for col in colnames:
            tab.heading(col, text=col, anchor=CENTER)

        cur.execute(f"SELECT * FROM {current_state} WHERE {find_in_choose.get()} LIKE '%{find_in_entry.get()}%'")
        result = cur.fetchall()
        for col in result:
            tab.insert(parent='', index='end', text='', values=list(col))

        find_in_window.destroy()

    global current_state

    cur.execute(f"SELECT * FROM {current_state} LIMIT 0;")
    colnames = [cols[0] for cols in cur.description]

    find_in_window = Toplevel(main)
    find_in_window.title("Find in")
    find_in_window.resizable(False, False)
    find_in_window.iconphoto(False, PhotoImage(file="src/logo.png"))

    find_in_choose = StringVar(find_in_window)
    find_in_choose.set(colnames[0])
    find_in_option = OptionMenu(find_in_window, find_in_choose, *colnames)
    find_in_option.pack(side=TOP)

    find_in_text = Label(find_in_window, text="request")
    find_in_text.pack(side=LEFT)

    find_in_entry = Entry(find_in_window, width=20, font="Arial 9")
    find_in_entry.pack(side=LEFT)

    f_button = Button(find_in_window, text="Search", command=find)
    f_button.pack(side=LEFT, padx=5)


def updateOptions():
    global current_state
    global choose

    choose.set("")
    option["menu"].delete(0, "end")
    for choice in tables:
        option["menu"].add_command(label=choice, command=lambda i=choice: printTable(i))
    choose.set(current_state)


def createMyMusic():
    global current_state
    global current_user
    global create_library_flag

    if create_library_flag:
        cur.execute(queries.my_music_query)
        create_lib_button.destroy()
    else:
        create_lib_button.destroy()

    cur.execute(f"UPDATE iuser SET libflag = 'TRUE' WHERE username = '{current_user}'")
    conn.commit()

    tables.append("my_music")
    updateOptions()


def runExit():
    cur.close()
    exit()


def printTable(event=None):
    global current_state
    global current_user
    global choose

    cur.execute(f"SELECT * FROM {event} LIMIT 0;")
    colnames = [cols[0] for cols in cur.description]
    print(colnames)

    for item in tab.get_children():
        tab.delete(item)

    tab.heading("#0", text="")
    tab.column("#0", anchor=W, width=0, stretch=False)

    tab["columns"] = colnames

    for col in colnames:
        tab.column(col)
    for col in colnames:
        tab.heading(col, text=col, anchor=CENTER)

    if event == "my_music":
        cur.execute(
            f"SELECT * FROM {event} JOIN iuser ON {event}.user_id = iuser.user_id WHERE iuser.username = '{current_user}';")
    else:
        cur.execute(f"SELECT * FROM {event} ORDER BY {colnames[0]};")
    result = cur.fetchall()
    for col in result:
        tab.insert(parent="", index="end", text="", values=list(col))

    current_state = event
    choose.set(current_state)


def connectToDatabase():
    global flag_connect
    global current_user

    if username_form.get() == "":
        return

    username = username_form.get()

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="tunes",
            user="bool",
            password="bool"
        )
        cur = conn.cursor()
    except psycopg2.OperationalError:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="bool",
            password="bool"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE tunes;")
        conn.commit()
        cur.close()
        conn = psycopg2.connect(
            host="localhost",
            database="tunes",
            user="bool",
            password="bool"
        )
        cur = conn.cursor()
        cur.execute(queries.main_query)
        conn.commit()
        cur.execute(f"INSERT INTO iuser(username, email, passwd, phone, country, my_tracks_count)"
                    f"VALUES ('{username}', '*mail*_{username}', '*passwd*_{username}', '*number*_{username}', "
                    f"'*country*_{username}', 0);")
        conn.commit()
        cur.close()
    else:
        cur.execute(f"SELECT * FROM iuser WHERE username = '{username}'")
        if len(cur.fetchall()) != 1:
            cur.execute(f"INSERT INTO iuser(username, email, passwd, phone, country, my_tracks_count)"
                        f"VALUES ('{username}', '*mail*_{username}', '*passwd*_{username}', '*number*_{username}', "
                        f"'*country*_{username}', 0);")
            conn.commit()
    flag_connect = True
    current_user = username
    entrance.destroy()


current_user = None

# create db
entrance = Tk()
entrance.title("Logging...")
entrance.geometry("300x150")
entrance.resizable(False, False)
entrance.iconphoto(False, PhotoImage(file="src/logo.png"))
flag_connect = False

entrance_frame = Frame(entrance)

username_label = Label(entrance_frame, text="username", font="Arial 9")
username_label.pack(anchor=CENTER)

username_form = Entry(entrance_frame, width=20, font="Arial 9")
username_form.pack(anchor=CENTER)

login_button = Button(entrance_frame, text="Log in", command=connectToDatabase)
login_button.pack(anchor=CENTER, pady=5)

hint_text = Label(text="NOTE: If database doesn't exist, it would be created", font="Arial 9")
hint_text.pack(side=BOTTOM)

entrance_frame.pack(expand=True)

entrance.mainloop()

if not flag_connect:
    exit(0)

conn = psycopg2.connect(
    host="localhost",
    database="tunes",
    user="bool",
    password="bool"
)

create_library_flag = None

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
tables = [table[0] for table in cur.fetchall()]

current_state = "track_list"
if "my_music" in tables:
    create_library_flag = False
    tables.remove("my_music")
else:
    create_library_flag = True

main = Tk()
main.title("tunes")
main.geometry("1000x500")
main.resizable(False, False)
main.iconphoto(False, PhotoImage(file="src/logo.png"))

option_frame = Frame(main)

choose = StringVar(main)
choose.set(current_state)
option = OptionMenu(option_frame, choose, *tables, command=printTable)
option.pack(side=LEFT)

# main buttons
add_button = Button(option_frame, text="Add", command=runAdd, width=10)
add_button.pack(side=LEFT)

edit_button = Button(option_frame, text="Edit", command=runEdit, width=10)
edit_button.pack(side=LEFT)

delete_button = Button(option_frame, text="Delete", command=runDelete, width=10)
delete_button.pack(side=LEFT)

clear_all_button = Button(option_frame, text="Clear all", command=runClearAll, width=10)
clear_all_button.pack(side=LEFT)

find_in_button = Button(option_frame, text="Find in", command=runFindIn, width=10)
find_in_button.pack(side=LEFT)

exit_button = Button(option_frame, text="Exit", command=runExit, width=10)
exit_button.pack(side=RIGHT)

cur.execute(f"SELECT libflag FROM iuser WHERE username = '{current_user}'")
if not cur.fetchall()[0][0]:
    create_lib_button = Button(option_frame, text="Create library", command=createMyMusic, width=10)
    create_lib_button.pack(side=LEFT)
else:
    tables.append("my_music")
    updateOptions()

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
print(current_user)
printTable(current_state)
main.mainloop()
cur.close()
print("Finished")
