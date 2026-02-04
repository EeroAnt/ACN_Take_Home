import sqlite3

from utils.logging_config import logger

def setup_database(filename: str = "default.db") -> sqlite3.Connection:
  conn = sqlite3.connect(filename)
  cleanup_database(conn)
  create_customer_table(conn)
  create_transactions_table(conn)
  logger.info("Database setup done.")
  return conn

def cleanup_database(conn: sqlite3.Connection) -> None:
  cur = conn.cursor()
  cur.execute("DROP TABLE IF EXISTS customers")
  cur.execute("DROP TABLE IF EXISTS transactions")
  cur.execute("DROP VIEW IF EXISTS clean_transactions")

def create_customer_table(conn: sqlite3.Connection) -> None:
  cur = conn.cursor()
  cur.execute("""
    CREATE TABLE customers (
      customer_id INTEGER PRIMARY KEY,
      country TEXT,
      signup_date TEXT,
      email TEXT
    )
    """)
  conn.commit()
  
def populate_customers_table(conn: sqlite3.Connection, customers: list[tuple]) -> None:
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO customers (customer_id, country, signup_date, email)
        VALUES (?, ?, ?, ?)
    """, customers)
    conn.commit()

def create_transactions_table(conn: sqlite3.Connection) -> None:
  cur = conn.cursor()
  cur.execute("""
    CREATE TABLE transactions (
      transaction_id INTEGER,
      customer_id INTEGER,
      amount REAL,
      currency TEXT,
      timestamp TEXT,
      category TEXT,
      FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
  """)
  conn.commit()

def populate_transactions_table(conn: sqlite3.Connection, transactions: list[tuple]) -> None:
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO transactions (transaction_id, customer_id, amount, currency, timestamp, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, transactions)
    conn.commit()

def clean_transactions(conn: sqlite3.Connection) -> None:
  cur = conn.cursor()
  cur.execute(
    """
      CREATE VIEW clean_transactions AS
      SELECT
        transaction_id,
        transactions.customer_id customer_id,
        amount,
        currency,
        timestamp,
        category
      FROM transactions
      INNER JOIN customers
      ON transactions.customer_id = customers.customer_id
      WHERE currency IS NOT NULL
        AND transactions.customer_id IS NOT NULL
        AND transactions.timestamp >= customers.signup_date
      GROUP BY transaction_id
    """
  )