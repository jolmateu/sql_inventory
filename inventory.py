import sqlite3

class Inventory:
    """ Initializes the articles dictionary"""
    def __init__(self):
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()

    """ Adds an article to the inventory """
    def add_article(self, name, price):
        self.cursor.execute('INSERT INTO items (name, price) VALUES (?, ?)', (name, price))
        self.conn.commit()
        print(f"Item {name} added to inventory")

    """ Deletes an article from the inventory """
    def del_article(self, item_id):
        self.cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        self.conn.commit()
        print(f"The item with ID {item_id} was deleted.")

    """ Updates the quantity of an existing article """
    def sale_item(self, item_id, sell_quantity):
        self.cursor.execute('SELECT quantity FROM inventory WHERE item_id = ?', (item_id,))
        current_stock = self.cursor.fetchone()

        if current_stock and current_stock[0] >= sell_quantity:
            # Reduce the available quantity in 'inventory'
            self.cursor.execute('UPDATE inventory SET quantity = quantity - ? WHERE item_id = ?', (sell_quantity, item_id))
            self.conn.commit()

            # Register the sale in 'ventas'
            self.cursor.execute('INSERT INTO sales (item_id, sell_quantity, sell_date) VALUES (?, ?, CURRENT_DATE)', (item_id, sell_quantity))
            self.conn.commit()
            print(f"{sell_quantity} units of item ID {item_id} have been sold.")
        else:
            print("There is not enough stock to make the sale.")

    """ Displays all articles present in the inventory """
    def shw_inventory(self):
        self.cursor.execute('''
            SELECT a.id, a.name, a.price, COALESCE(i.quantity, 0) AS avalaible_quantity
            FROM items a
            LEFT JOIN inventory i ON a.id = i.item_id
        ''')
        inventory = self.cursor.fetchall()
        print("Inventory:")
        print("ID | Name | Price | Avalaible Quantity")
        for item in inventory:
            print(item)

    def close_conn(self):
        self.conn.close()

    def create_tables(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY(item_id) REFERENCES item(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                sell_quantity INTEGER NOT NULL,
                sell_date DATE NOT NULL,
                FOREIGN KEY(item_id) REFERENCES item(id)
            )
        ''')

        conn.commit()
        conn.close()
