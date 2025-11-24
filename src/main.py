from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect('users.db')

@app.route('/users')
def get_users():
    username = request.args.get('username')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Parameterized SQL query (prevents SQL injection)
    if username:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    else:
        cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()
    conn.close()

    # Return JSON instead of string for correctness and security
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
