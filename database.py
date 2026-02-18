import sqlite3

def create_database():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_chat(user_msg, bot_msg):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chat_logs (user_message, bot_response) VALUES (?, ?)",
        (user_msg, bot_msg)
    )

    conn.commit()
    conn.close()
    
def get_all_logs():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chat_logs")
    logs = cursor.fetchall()

    conn.close()
    return logs

