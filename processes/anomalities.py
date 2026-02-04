import sqlite3

AnomalyResult = dict[str, list[tuple]]

def check_anomalities(conn: sqlite3.Connection) -> tuple[AnomalyResult, AnomalyResult]:
  customer_anomalities = {}
  transaction_anomalities = {}

  customer_columns = ["customer_id", "country", "signup_date", "email"]
  relevant_transaction_columns = ["transaction_id", "customer_id", "amount", "currency", "timestamp"]

  cur = conn.cursor()
  for column in customer_columns:
    cur.execute(
      f"""
        SELECT *
        FROM customers
        WHERE {column} IS NULL;
      """
    )
    customer_anomalities[column] = cur.fetchall()
  
  for column in relevant_transaction_columns:
    cur.execute(
      f"""
        SELECT *
        FROM transactions
        WHERE {column} IS NULL;
      """
    )
    transaction_anomalities[column] = cur.fetchall()

  return customer_anomalities, transaction_anomalities