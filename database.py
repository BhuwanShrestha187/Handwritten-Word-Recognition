import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, gmail TEXT, verified INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedback 
                 (id INTEGER PRIMARY KEY, user_id INTEGER, rating INTEGER, comment TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY, user_id INTEGER, image TEXT, text TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # New tables for settings functionality
    c.execute('''CREATE TABLE IF NOT EXISTS user_preferences 
                 (user_id INTEGER PRIMARY KEY, analytics INTEGER, notifications INTEGER, language TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_2fa 
                 (user_id INTEGER PRIMARY KEY, enabled INTEGER, secret TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions 
                 (id INTEGER PRIMARY KEY, user_id INTEGER, session_id TEXT, 
                  ip_address TEXT, device_info TEXT, last_active DATETIME)''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()