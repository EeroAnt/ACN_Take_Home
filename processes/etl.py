import sqlite3

from utils.database import populate_customers_table, populate_transactions_table
from utils.extractions import extract_from_csv
from utils.logging_config import logger
from utils.transformations import transform_customers, transform_transactions


def run_etl(conn: sqlite3.Connection) -> None:
  customers = extract_from_csv("data/customers.csv")
  logger.info(f"Extracted {len(customers)} customers")
  customers_transformed = transform_customers(customers)
  logger.info("Customer data transformed")
  populate_customers_table(conn, customers_transformed)
  logger.info("Customer data loaded to database")

  transactions = extract_from_csv("data/transactions.csv")
  logger.info(f"Extracted {len(transactions)} transactions")
  transactions_transformed = transform_transactions(transactions)
  logger.info("Transaction data transformed")
  populate_transactions_table(conn, transactions_transformed)
  logger.info("Transaction data loaded to database")