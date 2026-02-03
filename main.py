from utils.extractions import extract_from_csv

def main():

    customers = extract_from_csv("data/customers.csv")
    transactions = extract_from_csv("data/transactions.csv")

if __name__ == "__main__":
    main()
