def transform_customers(raw_data: list[tuple]) -> list[tuple]:
  return [
    (
      int(customer_id) if customer_id else None,
      country if country else None,
      signup_date if signup_date else None,
      email if email else None
    )
    for customer_id, country, signup_date, email in raw_data
  ]

def transform_transactions(raw_data: list[tuple]) -> list[tuple]:
  # There were rows without a customer id, but at this point I'll just extract everything
  return [
    (
      int(transaction_id) if transaction_id else None,
      int(customer_id) if customer_id else None,
      float(amount) if amount else None,
      currency.upper() if currency else None,
      timestamp if timestamp else None,
      category if category else None
    )
    for transaction_id, customer_id, amount, currency, timestamp, category in raw_data
  ]