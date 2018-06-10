import sqlite3

# class SQLiteMethods:
#     def __init__(self):
#         self.connection = sqlite3.connect('xmpl-coffee-shop-db.db',
#         detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#         self.cursor = self.connection.cursor()


def select_items(table):
    conn = sqlite3.connect(
        # 'xmpl-coffee-shop-db.db',
        'web/db.sqlite3',
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(table))
    items = c.fetchall()
    conn.close()
    return items


def select_sizes(coffee_id):
    conn = sqlite3.connect(
        'web/db.sqlite3',
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("""
    SELECT *
    FROM bot_size
    WHERE coffee_id = {}
    """.format(coffee_id))
    sizes = c.fetchall()
    conn.close()
    return sizes


def insert_order(sql_query):
    conn = sqlite3.connect(
        'web/db.sqlite3',
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("INSERT INTO bot_orders(user_id, coffee_id, syrup_id, cost, ordered_at, size_id) \
     VALUES (?, ?, ?, ?, ?, ?);", sql_query)
    conn.commit()
    conn.close()


def last_order(user_id):
    conn = sqlite3.connect(
        'web/db.sqlite3',
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("""
    SELECT bot_coffee.name, bot_syrup.name, bot_size.size, user_id, bot_orders.coffee_id, \
    syrup_id, (bot_syrup.cost+bot_size.cost), size_id
    FROM bot_orders
    INNER JOIN bot_coffee on (bot_coffee.id = bot_orders.coffee_id)
    INNER JOIN bot_syrup on (bot_syrup.id = bot_orders.syrup_id)
    INNER JOIN bot_size on (bot_size.id = bot_orders.size_id)
    WHERE user_id = ?
    ORDER BY ordered_at desc
    LIMIT 1
    """, user_id)
    l_order = c.fetchone()
    conn.close()
    return l_order
