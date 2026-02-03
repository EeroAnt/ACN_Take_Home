from utils.database import populate_customers_table, setup_database
from utils.extractions import extract_from_csv
from utils.transformations import transform_customers, transform_transactions

def main():
    conn = setup_database()
    customers = extract_from_csv("data/customers.csv")
    customers_transformed = transform_customers(customers)
    populate_customers_table(conn, customers_transformed)
    transactions = extract_from_csv("data/transactions.csv")
    transactions_transformed = transform_transactions(transactions)

if __name__ == "__main__":
    main()
