import mysql.connector as sql
import textwrap
from getpass import getpass


try:
    print("-" * 45)
    sqlpass = getpass("Enter your MySQL Password: ")
    print("-" * 45)
except KeyboardInterrupt as k:
    print("\nKeyboard Interrupt!\nExiting Softly!")
    print("-" * 45)
    exit()


def establish_connection():
    try:
        conn = sql.connect(
            host="localhost", user="root", password=sqlpass, charset="utf8"
        )

        if conn.is_connected():
            print()
            print("=" * 45)
            print(" Successfully Connected to MySQL Database!☑️")
            print("=" * 45)

        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS TDL;")
        cur.execute("USE TDL;")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS to_do_list (ID INT UNIQUE KEY, TASK VARCHAR(255));"
        )
        conn.commit()

        cur.close()
        conn.close()
        return True

    except sql.Error as e:
        print("=" * 45)
        print("             Access Denied! ❌")
        print("    Wrong Password or MySQL Server Error")
        print("=" * 45)

        return False


def ID_Renumber():
    conn = sql.connect(host="localhost", user="root", password=sqlpass, charset="utf8")
    cur = conn.cursor()
    cur.execute("USE TDL;")
    cur.execute("DROP PROCEDURE IF EXISTS RenumberID")
    cur.execute("""
        CREATE PROCEDURE RenumberID()
        BEGIN
            SET @count = 0;

            UPDATE TO_DO_LIST
            SET ID = (@count := @count + 1)
            ORDER BY ID;
        END
    """)
    cur.close()
    conn.close()


my_tasks = []
unsaved_tasks = []
tasks_dataset = {}


def retrieve_from_table():
    global my_tasks
    global tasks_dataset

    conn = sql.connect(host="localhost", user="root", password=sqlpass, charset="utf8")
    cur = conn.cursor()
    cur.execute("USE TDL;")
    cur.execute("SELECT * FROM to_do_list;")
    rows = cur.fetchall()
    if rows:
        for row in rows:
            my_tasks.append(row[1])
            tasks_dataset[row[0]] = row[1]

    cur.close()
    conn.close()


def save_memory():
    global unsaved_tasks

    if not unsaved_tasks:
        print("No new tasks to save.")
        return

    conn = sql.connect(host="localhost", user="root", password=sqlpass, charset="utf8")
    cur = conn.cursor()
    cur.execute("USE TDL;")
    cur.execute("SELECT MAX(ID) FROM to_do_list;")
    row = cur.fetchone()
    max_id = row[0] if row and row[0] is not None else 0

    for task in unsaved_tasks:
        max_id += 1
        cur.execute("INSERT INTO to_do_list VALUES (%s, %s);", (max_id, task))

    conn.commit()
    cur.close()
    conn.close()

    unsaved_tasks.clear()


def dataset_design():
    global tasks_dataset
    for index, task in enumerate(my_tasks):
        tasks_dataset[index + 1] = task


def add_task(task):
    global my_tasks
    global unsaved_tasks

    my_tasks.append(task)
    unsaved_tasks.append(task)
    print(f"\nThe task `[{task}]`\nhas been successfully added to your\nTo-Do-List.")
    dataset_design()
    save_memory()


def remove_task(index):
    global unsaved_tasks

    try:
        item = my_tasks.pop(index - 1)
        if item in unsaved_tasks:
            unsaved_tasks.remove(item)
        else:
            conn = sql.connect(
                host="localhost", user="root", password=sqlpass, charset="utf8"
            )
            cur = conn.cursor()
            cur.execute("USE TDL;")
            cur.execute(
                "DELETE FROM to_do_list WHERE TASK = %s ORDER BY ID LIMIT 1;", (item,)
            )
            cur.execute("CALL RenumberID();")
            conn.commit()
            cur.close()
            conn.close()
    except IndexError as e:
        print("=" * 45)
        print("Index is Out of Range!")
        print("=" * 45)
    try:
        print()
        print("=" * 45)
        print(
            f"The task '[{item}]'\nhas been successfully removed from your\nTo-Do List."
        )
        print("=" * 45)
    except UnboundLocalError as e:
        print("That index doesn't exist right now!")

    dataset_design()


def clear_list():
    global my_tasks
    conn = sql.connect(host="localhost", user="root", password=sqlpass, charset="utf8")
    cur = conn.cursor()
    cur.execute("USE TDL;")
    cur.execute("TRUNCATE TABLE to_do_list;")
    my_tasks.clear()
    conn.commit()
    cur.close()
    conn.close()


def view_tasks():
    if not my_tasks:
        print()
        print("=" * 45)
        print("          Your To-Do-List is Empty!")
        print("=" * 45)
        return

    print("\n" + "=" * 45)
    print("               YOUR TO-DO LIST")
    print("=" * 45)
    print(f"{'ID':<6}{'TASK'}")
    print("-" * 45)

    for index, task in enumerate(my_tasks):
        wrapped = textwrap.wrap(task, width=35)
        print(f"\n{index + 1:<6}{wrapped[0]}")
        for line in wrapped[1:]:
            print(f"{'':<6}{line}")

    print("=" * 45)


if __name__ == "__main__":
    try:
        if establish_connection() == True:
            ID_Renumber()
            retrieve_from_table()
            while True:
                print("\n" + "=" * 45)
                print("       📝 TO-DO LIST APPLICATION MENU")
                print("=" * 45)
                print(" [1] ➕ Add Task")
                print(" [2] 📋 See List")
                print(" [3] ❌ Remove Task")
                print(" [4] 🗑️  Clear List")
                print(" [5] 👋 Exit")
                print("=" * 45)

                choice = input("\nEnter your choice from [1]|[2]|[3]|[4]|[5]: ")

                if choice == "1":
                    print()
                    print("-" * 45)
                    task = input("Enter the Task you want to Add:\n=> ")
                    add_task(task)
                    print("-" * 45)
                elif choice == "2":
                    view_tasks()
                elif choice == "3":
                    print()
                    print("=" * 45)
                    print()
                    
                    ch = input("Are you Sure?,\nYou want to Remove a Task from your\nTo-Do-List?\nEnter Y/n to Proceed: ")
                    if ch in "Y":
                        print()
                        index = int(input("Enter the index of the task you want to Remove: "))
                        print()

                        remove_task(index)
                    elif ch in "Nn":
                        print()
                        print("=" * 45)
                        print("No Change in Tasks, Tasks are Intact")
                        print("=" * 45)
                    else:
                        print()
                        print("=" * 45)
                        print("Invalid Choice!")
                        print("=" * 45)
                elif choice == "4":
                    print()
                    print("-" * 45)
                    command = input("Are you Sure?,\nYou want to Clear your To-Do-List?\nEnter Y/n to Proceed: ")
                    print()
                    if command in "Y":
                        clear_list()
                        print("=" * 45)
                        print("The To-Do-List has been Successfully Cleared")
                        print("=" * 45)
                    elif command in "Nn":
                        print()
                        print("=" * 45)
                        print("No Change in Tasks, Tasks are Intact")
                        print("=" * 45)
                        print()
                    else:
                        print()
                        print("=" * 45)
                        print("Invalid Choice!")
                        print("=" * 45)

                elif choice == "5":
                    print()
                    print("=" * 45)
                    print("      Exiting the Application. Goodbye!")
                    print("=" * 45)
                    print()
                    break
                else:
                    print()
                    print("=" * 45)
                    print("Invalid Choice. Please Try Again.")
                    print("=" * 45)
    except KeyboardInterrupt as k:
        print()
        print()
        print("="*45)
        print("Keyboard Interrupt!\nExiting Softly!")
        print("=" * 45)
        print()
        exit()
