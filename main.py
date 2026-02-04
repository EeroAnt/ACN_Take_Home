from processes.anomalities import check_anomalities
from processes.etl import run_etl
from utils.database import setup_database
from utils.logging_config import logger

def main():
  logger.info("Starting the pipeline")
  conn = setup_database()

  run_etl(conn)

  customer_anomalities, transaction_anomalities = check_anomalities(conn)

  for item in customer_anomalities:
    logger.info(f"Found {len(customer_anomalities[item])} anomalities in customers table column {item}")

  for item in transaction_anomalities:
    logger.info(f"Found {len(transaction_anomalities[item])} anomalities in customers table column {item}")

if __name__ == "__main__":
  main()
