import os
import sqlite3
import unittest
from app import app

class TestGetUsers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary test database
        cls.test_db = "users.db"
        conn = sqlite3.connect(cls.test_db)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT
            )
        """)

        # Insert mock data
        cursor.execute("INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com')")
        cursor.execute("INSERT INTO users (username, email) VALUES ('bob', 'bob@example.com')")

        conn.commit()
        conn.close()

        # Configure Flask test client
        app.testing = True
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        # Clean up test DB
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    def test_get_users_valid(self):
        response = self.client.get("/users?username=alice")
        self.assertEqual(response.status_code, 200)
        self.assertIn("alice", response.data.decode())

    def test_get_users_no_match(self):
        response = self.client.get("/users?username=nonexistent")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "[]")

    def test_get_users_missing_param(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "[]")

if __name__ == "__main__":
    unittest.main()
