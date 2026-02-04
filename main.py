from processes.anomalies import run_anomaly_report
from processes.etl import run_etl
from processes.features import feature_report
from utils.database import clean_transactions, setup_database
from utils.logging_config import logger

def main():
  logger.info("Starting the pipeline")
  conn = setup_database()

  run_etl(conn)

  run_anomaly_report(conn)

  clean_transactions(conn)

  feature_report(conn)

if __name__ == "__main__":
  main()
