from flask import Flask, request, jsonify
from flask_cors import CORS


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

def update_user(user):
    message = {}
    try:
        # Connect to the database
        conn = connect_to_db()
        
        # Execute the UPDATE query
        conn.execute(
            '''UPDATE users 
            SET name = ?, email = ?, phone = ?, address = ?, country = ? 
            WHERE user_id = ?''',
            (user['name'], user['email'], user['phone'], user['address'], user['country'], user['user_id'])
        )
        conn.commit()  # Commit the changes
        
        message["status"] = "User updated successfully"
    
    except Exception as e:
        # Rollback changes if there's an error
        conn.rollback()
        message["status"] = "Cannot update user"
        print(f"Error updating user: {e}")
    
    finally:
        # Ensure the connection is closed
        conn.close()
    
    return message




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/api/users', methods=['GET'])
def api_get_users():
    # Call your get_users() function and return the results as JSON
    return jsonify(get_users())

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    # Call your get_user_by_id() function to fetch a single user by ID
    return jsonify(get_user_by_id(user_id))

@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    # Fetch data from the request and call insert_user() to add a new user
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    # Fetch data from the request and call update_user() to update user details
    user = request.get_json()
    return jsonify(update_user(user))

@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    # Call your delete_user() function to remove the user with the specified ID
    return jsonify(delete_user(user_id))
if __name__ == "__main__":
    app.run()  # Starts the Flask app

