import sqlite3

def setup_database(filename: str = "default.db") -> sqlite3.Connection:
  conn = sqlite3.connect(filename)
  create_customer_table(conn)
  return conn

def create_customer_table(conn: sqlite3.Connection):
  cur = conn.cursor()
  cur.execute("""
    CREATE TABLE IF NOT EXISTS customers
      (
        customer_id INTEGER PRIMARY KEY,
        country TEXT,
        signup_date TEXT,
        email TEXT
              )
    """)
  
def populate_customers_table(conn: sqlite3.Connection, customers: list[tuple]):
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO customers (customer_id, country, signup_date, email)
        VALUES (?, ?, ?, ?)
    """, customers)
    conn.commit()