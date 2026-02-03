import sqlite3

def setup_database(filename: str = "default.db") -> sqlite3.Connection:
  conn = sqlite3.connect(filename)
  create_customer_table(conn)
  create_transactions_table(conn)
  return conn

def create_customer_table(conn: sqlite3.Connection):
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS customers")
  cur.execute("""
    CREATE TABLE customers (
      customer_id INTEGER PRIMARY KEY,
      country TEXT,
      signup_date TEXT,
      email TEXT
    )
    """)
  conn.commit()
  
def populate_customers_table(conn: sqlite3.Connection, customers: list[tuple]):
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO customers (customer_id, country, signup_date, email)
        VALUES (?, ?, ?, ?)
    """, customers)
    conn.commit()

def create_transactions_table(conn: sqlite3.Connection):
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS transactions")
  cur.execute("""
    CREATE TABLE transactions (
      transaction_id INTEGER PRIMARY KEY,
      customer_id INTEGER,
      amount REAL,
      currency TEXT,
      timestamp TEXT,
      category TEXT,
      FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
  """)
  conn.commit()
