def exchange_to_eur(amount: float, currency: str) -> float:

  if currency == "EUR":
    return amount

  rates = {
    "NOK" : 0.087,
    "SEK" : 0.094
  }
  return round(amount * rates[currency], 2)