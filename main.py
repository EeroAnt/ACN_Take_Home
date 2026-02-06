from time import time

from processes.anomalies import run_anomaly_report
from processes.etl import run_etl
from processes.features import feature_report
from processes.rag import run_rag_demo
from utils.database import clean_transactions, setup_database
from utils.logging_config import logger

def main():
  logger.info("=== Part 1: ETL ===")
  conn = setup_database()
  run_etl(conn)

  logger.info("=== Part 2: Feature Engineering ===")
  run_anomaly_report(conn)
  clean_transactions(conn)
  feature_report(conn)

  logger.info("=== Part 3: LLM Pipeline ===")
  run_rag_demo()

if __name__ == "__main__":
  start = time()
  main()
  logger.info(f"The run finished in {time()-start:.2f} seconds")
