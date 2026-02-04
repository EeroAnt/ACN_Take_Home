import sqlite3

from utils.logging_config import logger


AnomalyResult = dict[str, list[tuple]]

def run_anomaly_report(conn: sqlite3.Connection) -> None:
  
  customer_anomalies, transaction_anomalies = check_basic_anomalies(conn)
  report_basic_anomalies(customer_anomalies, transaction_anomalies)

  timing_anomalies = check_timing_anomalies(conn)
  report_timing_anomalies(timing_anomalies)

def check_basic_anomalies(conn: sqlite3.Connection) -> tuple[AnomalyResult, AnomalyResult]:
  customer_anomalies = {}
  transaction_anomalies = {}

  customer_columns = ["customer_id", "country", "signup_date", "email"]
  transaction_columns = ["transaction_id", "customer_id", "amount", "currency", "timestamp", "category"]

  cur = conn.cursor()
  for column in customer_columns:
    cur.execute(
      f"""
        SELECT *
        FROM customers
        WHERE {column} IS NULL;
      """
    )
    customer_anomalies[column] = cur.fetchall()
  
  for column in transaction_columns:
    cur.execute(
      f"""
        SELECT *
        FROM transactions
        WHERE {column} IS NULL;
      """
    )
    transaction_anomalies[column] = cur.fetchall()

  return customer_anomalies, transaction_anomalies

def report_basic_anomalies(customer_anomalies: AnomalyResult, transaction_anomalies: AnomalyResult):
  for item in customer_anomalies:
    if customer_anomalies[item]:
      logger.info(f"Found {len(customer_anomalies[item])} NULL values in customers table column {item}")

  for item in transaction_anomalies:
    if transaction_anomalies[item]:
      logger.info(f"Found {len(transaction_anomalies[item])} NULL values in transactions table column {item}")


def check_timing_anomalies(conn: sqlite3.Connection) -> AnomalyResult:
  cur = conn.cursor()
  cur.execute(
    """
      SELECT * FROM transactions
      INNER JOIN customers
      ON transactions.customer_id = customers.customer_id
      WHERE transactions.timestamp < customers.signup_date
    """
  )
  return {"Transactions before signup" : cur.fetchall()}

def report_timing_anomalies(timing_anomalies):
  logger.info(f"{len(timing_anomalies['Transactions before signup'])} transactions found where timestamp precedes users signup")