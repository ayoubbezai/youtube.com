import sqlite3
import os

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nickname TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )
    ''')
    
    # Create notes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users (username)
    )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, password, nickname, role='user'):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO users (username, password, nickname, role) VALUES (?, ?, ?, ?)',
        (username, password, nickname, role)
    )
    
    conn.commit()
    conn.close()
    
    return True

def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    user = cursor.execute(
        'SELECT * FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    
    conn.close()
    
    if user:
        return dict(user)
    return None

def create_note(username, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO notes (username, content) VALUES (?, ?)',
        (username, content)
    )
    
    note_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return note_id

def get_note_by_id(note_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM notes WHERE id = {note_id}"
    
    try:
        note = cursor.execute(query).fetchone()
        conn.close()
        
        if note:
            return dict(note)
        return None
    except:
        conn.close()
        return None
    
def get_user_notes(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    notes = cursor.execute(
        'SELECT * FROM notes WHERE username = ? ORDER BY created_at DESC',
        (username,)
    ).fetchall()
    
    conn.close()
    
    return [dict(note) for note in notes]
