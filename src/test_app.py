import os
import sqlite3
import pytest
from app import app, get_db_connection

# ----- FIXTURES -----

@pytest.fixture
def client(tmp_path, monkeypatch):
    """
    Creates a temporary SQLite database for testing
    and overrides the app DB connection to use it.
    """
    test_db = tmp_path / "test_users.db"

    # Create test DB schema + seed data
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
    cursor.execute("INSERT INTO users (username) VALUES ('alice')")
    cursor.execute("INSERT INTO users (username) VALUES ('bob')")
    conn.commit()
    conn.close()

    # Patch DB connection function
    def test_db_connection():
        return sqlite3.connect(test_db)

    monkeypatch.setattr("app.get_db_connection", test_db_connection)

    with app.test_client() as client:
        yield client


# ----- TESTS -----

def test_get_all_users(client):
    """Should return all users as JSON."""
    response = client.get("/users")
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 2
    assert data[0][1] in ("alice", "bob")


def test_get_user_by_username(client):
    """Should return a specific user."""
    response = client.get("/users?username=alice")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 1
    assert data[0][1] == "alice"


def test_sql_injection_safe(client):
    """
    Ensures parameterized query prevents SQL injection.
    Injection attempt should return zero rows, not drop table.
    """
    malicious_input = "alice' OR '1'='1"
    response = client.get(f"/users?username={malicious_input}")

    assert response.status_code == 200
    
    data = response.get_json()
    assert data == []  # No injection should succeed


