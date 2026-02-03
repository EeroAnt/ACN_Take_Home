def transform_customers(raw_data: list[tuple]) -> list[tuple]:
    return [
        (int(customer_id), country, signup_date, email)
        for customer_id, country, signup_date, email in raw_data
    ]