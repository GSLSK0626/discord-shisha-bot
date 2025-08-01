from flask import g
import sqlite3
import os
from config import DB_NAME

DATABASE = 'shisha.db'

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    if not os.path.exists(DATABASE):
        with get_db() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            c.execute('''
                CREATE TABLE shisha_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TEXT,
                    shop_name TEXT,
                    main_flavor TEXT,
                    sub_flavor TEXT,
                    comment TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()

def create_user(username, password_hash):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return c.lastrowid

def get_user(username):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        return c.fetchone()

def add_shisha_log(user_id, date, shop_name, main_flavor, sub_flavor, comment):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO shisha_logs (user_id, date, shop_name, main_flavor, sub_flavor, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, date, shop_name, main_flavor, sub_flavor, comment))
        conn.commit()

def get_shisha_logs(user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM shisha_logs WHERE user_id = ? ORDER BY date DESC", (user_id,))
        return c.fetchall()

def delete_shisha_log(log_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM shisha_logs WHERE id = ?", (log_id,))
        conn.commit()

def update_shisha_log(log_id, date, shop_name, main_flavor, sub_flavors, comment):
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''
            UPDATE shisha_logs
            SET date = ?, shop_name = ?, main_flavor = ?, sub_flavor = ?, comment = ?
            WHERE id = ?
        ''', (date, shop_name, main_flavor, sub_flavors, comment, log_id))
        conn.commit()