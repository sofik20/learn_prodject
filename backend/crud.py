from database import get_connection


def get_all_products():
    """Получить список всех продуктов"""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_product_by_id(product_id: int):
    """Получить продукт по ID"""
    conn = get_connection()
    row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_product(data: dict):
    """Создать новый продукт"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO products (name, category, price, quantity, farm, organic)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            data["name"],
            data["category"],
            data["price"],
            data["quantity"],
            data["farm"],
            int(data["organic"])  # bool -> int (True=1, False=0)
        )
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_product(product_id: int, data: dict):
    """Полностью обновить продукт (PUT)"""
    conn = get_connection()
    conn.execute(
        """UPDATE products 
           SET name=?, category=?, price=?, quantity=?, farm=?, organic=?
           WHERE id=?""",
        (
            data["name"],
            data["category"],
            data["price"],
            data["quantity"],
            data["farm"],
            int(data["organic"]),
            product_id
        )
    )
    conn.commit()
    conn.close()


def delete_product(product_id: int):
    """Удалить продукт по ID"""
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()