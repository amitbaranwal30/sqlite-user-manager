import sqlite3
import re
import csv
from datetime import datetime
DB_NAME = "user_database.db"

# DATABASE SETUP
def connect_db():
    return sqlite3.connect(DB_NAME)

#CREATING TABLE
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
                  CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL  )
                   ''')
    conn.commit()
    conn.close()

# ---------------------------------email Validation 
def is_valid_email(email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

# ----------------------------------CRUD Funtions

# ------------------------------=---add user 
def add_user(name, email):
    if not name.strip():
        print("Name can not be empty.")
        return

    if not is_valid_email(email):
        print("Incorrect email format")
        return

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('insert into users (name, email) values ( ?,?)', (name.strip(), email.strip()))
        conn.commit()
        print(f'\nUser "{name}" added successfully!')
    except sqlite3.IntegrityError:
        print("\nEmail Already Exist.")
    
    conn.close()

# -------------------------------------view user list
def view_users():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('select * from users order by id')

    rows = cursor.fetchall()
    if rows:

        print(" All Users : ")
        print('=' * 50)
        for row in rows:
            print( f'ID: {row[0]} | Name: {row[1]} | email: {row[2]}')
        print('=' * 50)
    else:
        print("No users found.")
    
    conn.close()

# ---------------------------------------search user
def search_user(name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('select * from users where name like ?', ('%' + name + '%',))
    rows = cursor.fetchall()

    if rows:
        print(F'\nSearch result with name: "{name}"')
        for row in rows:
            print(F' ID: {row[0]} | Name: {row[1]} | Email: {row[2]}')
    else:
        print(f'No matching user found with name "{name}"')

    conn.close()

# ----------------------------------------delete user
def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('delete from users where id = ?', (user_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f'\nUser with ID "{user_id}" deleted.')
        else:
            print("user not found.")
        conn.close()

    except Exception as e:
        print(e)

# ---------------------------------------export user list to CSV
def export_to_csv():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('select * from users order by id')
        rows = cursor.fetchall()
        if not rows:
            print("No records found to export !")
            conn.close()
            return
        filename = f'user_exported_date_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv'

        with open (filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print(f'User list is exported in file name {filename}')
    
    except Exception as e:
        print(e)


# ----------------------------------------menu

def menu():
    create_table()

    while True:
        print('\n=== Welcome to User Manager App ===')
        print("1. Add User")
        print("2. View All Users")
        print("3. Search User")
        print('4. Delete User')
        print('5. Export to CSV')
        print('6. Exit')

        choice = input("Enter your choice (1-6): ")

        if choice == "1":

            name = input("Enter name : ")
            email = input("Enter email id : ")
            add_user(name, email)

        elif choice == "2":

            view_users()

        elif choice == "3":

            name = input("Enter name to search : ")
            search_user(name)
        
        elif choice == "4":
            user_id = input("Enter user ID to delete: ")
            try:
                delete_user(user_id)
            except ValueError:
                print("Invalid ID format.")
        
        elif choice == "5":
            
            export_to_csv()

        elif choice == "6":
            print("\nExiting Program. Thankyou !")
            break
        else:
            print("\nInvalid choice. Try again.")

if __name__ == "__main__":
    menu()