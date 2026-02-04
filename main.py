from utils.database import populate_customers_table, populate_transactions_table, setup_database
from utils.extractions import extract_from_csv
from utils.logging_config import logger
from utils.transformations import transform_customers, transform_transactions

def main():
    logger.info("Starting the pipeline")
    conn = setup_database()
    logger.info("Database setup done.")

    customers = extract_from_csv("data/customers.csv")
    logger.info(f"Extracted {len(customers)} customers")
    customers_transformed = transform_customers(customers)
    logger.info("Customer data transformed")
    populate_customers_table(conn, customers_transformed)
    logger.info("Customer data loaded to database")

    transactions = extract_from_csv("data/transactions.csv")
    logger.info(f"Extracted {len(customers)} transactions")
    transactions_transformed = transform_transactions(transactions)
    logger.info("Transaction data transformed")
    populate_transactions_table(conn, transactions_transformed)
    logger.info("Transaction data loaded to database")

if __name__ == "__main__":
    main()
