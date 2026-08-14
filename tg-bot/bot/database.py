import sqlite3
import os

class Database:
    def __init__(self, db_path="data/bot_data.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                request_type TEXT,
                request_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_user(self, user_id, username, first_name, last_name):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user_exists = cursor.fetchone()
            if user_exists:
                cursor.execute('''
                    UPDATE users SET username = ?, first_name = ?, last_name = ?
                    WHERE user_id = ?
                ''', (username, first_name, last_name, user_id))
            else:
                cursor.execute('''
                    INSERT INTO users (user_id, username, first_name, last_name)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, username, first_name, last_name))
            conn.commit()
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
        finally:
            if conn:
                conn.close()

    def add_request(self, user_id, request_type, request_text):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO requests (user_id, request_type, request_text)
                VALUES (?, ?, ?)
            ''', (user_id, request_type, request_text))
            conn.commit()
        except Exception as e:
            print(f"Ошибка при добавлении запроса: {e}")
        finally:
            if conn:
                conn.close()

    def get_user_stats(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            total_users = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM requests')
            total_requests = cursor.fetchone()[0]
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC LIMIT 5')
            recent_users = cursor.fetchall()
            cursor.execute('''
                SELECT request_type, COUNT(*) as count 
                FROM requests 
                GROUP BY request_type 
                ORDER BY count DESC
            ''')
            popular_requests = cursor.fetchall()
            return {
                'total_users': total_users,
                'total_requests': total_requests,
                'recent_users': recent_users,
                'popular_requests': popular_requests
            }
        except Exception as e:
            print(f"Ошибка при получении статистики: {e}")
            return None
        finally:
            if conn:
                conn.close()

db = Database()