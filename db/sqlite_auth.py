import sqlite3
from werkzeug.security import generate_password_hash


def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db(db_path):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            linked_patient_id TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_user(db_path, username, password, role, linked_patient_id=None):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO users (username, password_hash, role, active, linked_patient_id)
        VALUES (?, ?, ?, 1, ?)
    """, (username, password_hash, role, linked_patient_id))

    conn.commit()
    conn.close()


def get_user_by_username(db_path, username):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()
    return user


def get_user_by_id(db_path, user_id):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user


def get_all_users(db_path):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users ORDER BY id ASC")
    users = cursor.fetchall()

    conn.close()
    return users


def toggle_user_active(db_path, user_id):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT active FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        new_value = 0 if row["active"] == 1 else 1
        cursor.execute("UPDATE users SET active = ? WHERE id = ?", (new_value, user_id))
        conn.commit()

    conn.close()


def seed_default_users(db_path):
    existing_patient = get_user_by_username(db_path, "patient1")
    existing_clinician = get_user_by_username(db_path, "clinician1")
    existing_admin = get_user_by_username(db_path, "admin1")

    if existing_patient is None:
        create_user(db_path, "patient1", "patientpass", "patient", "P001")
    if existing_clinician is None:
        create_user(db_path, "clinician1", "clinicianpass", "clinician")
    if existing_admin is None:
        create_user(db_path, "admin1", "adminpass", "admin")