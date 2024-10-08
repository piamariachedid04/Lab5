from flask import Flask, request, jsonify
from flask_cors import CORS
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
