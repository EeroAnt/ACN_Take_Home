import sqlite3

from utils.currency_exchange import exchange_to_eur
from utils.logging_config import logger


AnomalyResult = dict[str, list[tuple]]

def run_anomaly_report(conn: sqlite3.Connection) -> None:
  
  customer_anomalies, transaction_anomalies = check_basic_anomalies(conn)
  report_basic_anomalies(customer_anomalies, transaction_anomalies)

  timing_anomalies = check_timing_anomalies(conn)
  report_timing_anomalies(timing_anomalies)

  duplicate_ids = check_duplicate_ids(conn)
  if duplicate_ids['Duplicate ids']:  
    report_duplicate_ids(duplicate_ids)

    duplicates = check_duplicates(conn)
    report_duplicates(duplicates, duplicate_ids)
  

def check_basic_anomalies(conn: sqlite3.Connection) -> tuple[AnomalyResult, AnomalyResult]:
  customer_anomalies = {}
  transaction_anomalies = {}

  customer_columns = ["customer_id", "country", "signup_date", "email"]
  transaction_columns = ["transaction_id", "customer_id", "amount", "currency", "timestamp", "category"]

  cur = conn.cursor()
  for column in customer_columns:
    cur.execute(
      f"""
        SELECT
          customer_id
        FROM customers
        WHERE {column} IS NULL;
      """
    )
    customer_anomalies[column] = cur.fetchall()
  
  for column in transaction_columns:
    cur.execute(
      f"""
        SELECT
          amount,
          currency
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
      if item != "currency":
        report_value(transaction_anomalies, item)


def check_timing_anomalies(conn: sqlite3.Connection) -> AnomalyResult:
  cur = conn.cursor()
  cur.execute(
    """
      SELECT
        transactions.amount,
        transactions.currency,
        transactions.timestamp,
        customers.signup_date
      FROM transactions
      INNER JOIN customers
      ON transactions.customer_id = customers.customer_id
      WHERE transactions.timestamp < customers.signup_date
    """
  )
  return {"Transactions before signup" : cur.fetchall()}

def report_timing_anomalies(timing_anomalies):
  logger.info(f"{len(timing_anomalies['Transactions before signup'])} transactions found where timestamp precedes users signup")
  report_value(timing_anomalies, 'Transactions before signup')


def report_value(anomalyresult: AnomalyResult, key: str) -> None:
  total = sum(
      exchange_to_eur(row[0], row[1]) 
      for row in anomalyresult[key]
      if row[1] is not None
  )
  logger.info(f"Total value: {round(total, 2)} EUR")

def check_duplicate_ids(conn: sqlite3.Connection) -> AnomalyResult:
  cur = conn.cursor()
  cur.execute(
    """
      SELECT transaction_id, count(*) as duplicates
      FROM transactions
      GROUP BY transaction_id
      HAVING COUNT(*) > 1
    """
  )
  return {"Duplicate ids" : cur.fetchall()}

def report_duplicate_ids(duplicate_ids: AnomalyResult) -> None:
  logger.info(f"Found {len(duplicate_ids['Duplicate ids'])} duplicated transaction ids")
  logger.info("Getting deeper comparison")

def check_duplicates(conn: sqlite3.Connection) -> AnomalyResult:
  cur = conn.cursor()
  cur.execute(
    """
      SELECT transaction_id, customer_id, amount, currency, timestamp, category, COUNT(*)
      FROM transactions
      GROUP BY transaction_id, customer_id, amount, currency, timestamp, category
      HAVING COUNT(*) > 1
    """
  )
  return {"Duplicates" : cur.fetchall()}

def report_duplicates(duplicates: AnomalyResult, duplicate_ids: AnomalyResult) -> None:
  logger.info(f"Found {len(duplicates['Duplicates'])} duplicated transactions")
  if len(duplicates['Duplicates']) == len(duplicate_ids['Duplicate ids']):
    logger.info("All the duplicates are exact matches and can be filtered via 'GROUP BY transaction_id'")
  else:
    logger.info("The duplicates are not exact matches. Requires more analysis")