import sqlite3
from datetime import datetime, timedelta

DB_FILE = "members.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            expires_at TEXT,
            payment_id TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_member(
    user_id,
    username,
    payment_id,
    membership_days
):

    conn = get_connection()

    cursor = conn.cursor()

    expires_at = (
        datetime.utcnow()
        + timedelta(days=membership_days)
    )

    cursor.execute("""
        INSERT OR REPLACE INTO members
        (user_id, username, expires_at, payment_id)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        username,
        expires_at.isoformat(),
        payment_id
    ))

    conn.commit()
    conn.close()

    return expires_at


def get_membership(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT expires_at
        FROM members
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    conn.close()

    if not result:
        return None

    return datetime.fromisoformat(result[0])
