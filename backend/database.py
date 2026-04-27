import sqlite3

DB_NAME = "farm_shop.db"


def get_connection():
    """Создаёт подключение к базе данных"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Создаёт таблицу products, если её нет"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            farm TEXT NOT NULL,
            organic INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()