import sqlite3

# class SQLiteMethods:
#     def __init__(self):
#         self.connection = sqlite3.connect('xmpl-coffee-shop-db.db',
#         detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#         self.cursor = self.connection.cursor()


def select_items(table):
    conn = sqlite3.connect('xmpl-coffee-shop-db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(table))
    items = c.fetchall()
    conn.close()
    return items


def insert_order(sql_query):
    conn = sqlite3.connect('xmpl-coffee-shop-db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("INSERT INTO orders(user_id, coffee_id, syrup_id, cost, ordered_at) VALUES (?, ?, ?, ?, ?);", sql_query)
    conn.commit()
    conn.close()


def last_order(user_id):
    conn = sqlite3.connect('xmpl-coffee-shop-db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("""
    SELECT coffee_name, syrup_name, cost
    FROM orders 
    INNER JOIN menu_coffee on menu_coffee.id = orders.coffee_id 
    INNER JOIN menu_syrup on menu_syrup.id = orders.syrup_id 
    WHERE user_id = ? 
    ORDER BY ordered_at desc 
    LIMIT 1
    """, user_id)
    l_order = c.fetchone()
    conn.close()
    return l_order
