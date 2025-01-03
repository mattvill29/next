import sqlite3

connection = sqlite3.connect('inventory.db')
cursor = connection.cursor()

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    connection.commit()

def fetch_products():
    cursor.execute('SELECT * FROM Products')
    return cursor.fetchall()

def insert_product(id, name, stock):
    cursor.execute('INSERT INTO Products (id, name, stock) VALUES (?, ?, ?)', (id, name, stock))
    connection.commit()

def delete_product(id):
    cursor.execute('DELETE FROM Products WHERE id = ?', (id,))
    connection.commit()

def update_product(name, stock, id):
    cursor.execute('UPDATE Products SET name = ?, stock = ? WHERE id = ?', (name, stock, id))
    connection.commit()

def id_exist(id):
    cursor.execute('SELECT id FROM Products WHERE id = ?', (id,))
    return cursor.fetchone() is not None

create_table()
