import sqlite3

from utils.logging_config import logger


AnomalyResult = dict[str, list[tuple]]

def run_anomality_report(conn: sqlite3.Connection) -> None:
  
  customer_anomalities, transaction_anomalities = check_basic_anomalities(conn)
  report_basic_anomalities(customer_anomalities, transaction_anomalities)

  timing_anomalities = check_timing_anomalities(conn)
  report_timing_anomalities(timing_anomalities)

def check_basic_anomalities(conn: sqlite3.Connection) -> tuple[AnomalyResult, AnomalyResult]:
  customer_anomalities = {}
  transaction_anomalities = {}

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
    customer_anomalities[column] = cur.fetchall()
  
  for column in transaction_columns:
    cur.execute(
      f"""
        SELECT *
        FROM transactions
        WHERE {column} IS NULL;
      """
    )
    transaction_anomalities[column] = cur.fetchall()

  return customer_anomalities, transaction_anomalities

def report_basic_anomalities(customer_anomalities: AnomalyResult, transaction_anomalities: AnomalyResult):
  for item in customer_anomalities:
    if customer_anomalities[item]:
      logger.info(f"Found {len(customer_anomalities[item])} NULL values in customers table column {item}")

  for item in transaction_anomalities:
    if transaction_anomalities[item]:
      logger.info(f"Found {len(transaction_anomalities[item])} NULL values in customers table column {item}")

def check_timing_anomalities(conn: sqlite3.Connection) -> AnomalyResult:
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

def report_timing_anomalities(timing_anomalities):
  logger.info(f"{len(timing_anomalities['Transactions before signup'])} transactions found where timestamp precedes users signup")