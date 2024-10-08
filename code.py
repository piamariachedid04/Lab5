#!/usr/bin/python
import sqlite3

# Function to connect to the database
def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

# Function to create the users table
def create_db_table():
    try:
        # Connect to the database
        conn = connect_to_db()
        # Execute SQL command to create table
        conn.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        );
        ''')
        conn.commit()  # Save changes
        print("User table created successfully")
    except sqlite3.OperationalError as e:
        # Catch and display error if table creation fails
        print(f"User table creation failed - {e}")
    finally:
        # Ensure the database connection is closed
        conn.close()

# Run the function to create the table
create_db_table()

def insert_user(user):
    inserted_user = {}
    try:
        # Connect to the database
        conn = connect_to_db()
        cur = conn.cursor()
        
        # Execute the INSERT query
        cur.execute(
            '''INSERT INTO users (name, email, phone, address, country)
            VALUES (?, ?, ?, ?, ?)''',
            (user['name'], user['email'], user['phone'], user['address'], user['country'])
        )
        
        # Commit the changes
        conn.commit()
        
        # Fetch the inserted user by ID
        inserted_user = get_user_by_id(cur.lastrowid)
        
    except Exception as e:
        # Rollback changes if there is any error
        conn.rollback()
        print(f"Error inserting user: {e}")
        
    finally:
        # Ensure the connection is closed
        conn.close()
    
    return inserted_user

user = {
"name": "John Doe",
"email": "jondoe@gamil.com",
"phone": "067765434567",
"address": "John Doe Street, Innsbruck",
"country": "Austria"
}
def get_users():
    users = []
    try:
        # Connect to the database
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Execute the SELECT query
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        
        # Convert row objects to dictionary
        for i in rows:
            user = {
                "user_id": i["user_id"],
                "name": i["name"],
                "email": i["email"],
                "phone": i["phone"],
                "address": i["address"],
                "country": i["country"]
            }
            users.append(user)
    
    except Exception as e:
        print(f"Error fetching users: {e}")
        users = []
    
    finally:
        # Ensure the connection is closed
        conn.close()

    return users


def get_user_by_id(user_id):
    user = {}
    try:
        # Connect to the database
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Execute the SELECT query to fetch the user by ID
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        
        # Convert row object to dictionary if user is found
        if row:
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"]
            }
    
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        user = {}
    
    finally:
        # Ensure the connection is closed
        conn.close()

    return user

import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        # Convert row objects to dictionaries
        for row in rows:
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"]
            }
            users.append(user)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        users = []
    finally:
        conn.close()
    return users

def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            # Convert row object to dictionary
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"]
            }
        else:
            print(f"No user found with user_id: {user_id}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        user = {}
    finally:
        conn.close()
    return user
def delete_user(user_id):
    message = {}
    try:
        # Connect to the database
        conn = connect_to_db()
        
        # Execute the DELETE query
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        
        message["status"] = "User deleted successfully"
    
    except Exception as e:
        # Rollback changes if there's an error
        conn.rollback()
        message["status"] = "Cannot delete user"
        print(f"Error deleting user: {e}")
    
    finally:
        # Ensure the connection is closed
        conn.close()
    
    return message
