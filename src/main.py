from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/users')
def get_users():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Vulnerable SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    return str(users)

if __name__ == '__main__':
    app.run(debug=True)
