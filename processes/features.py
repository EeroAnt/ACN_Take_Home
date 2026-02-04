import pandas as pd
import sqlite3

def feature_report(conn: sqlite3.Connection) -> pd.DataFrame:
  df = get_dataframe(conn)
  preview_features(df)
    

def get_dataframe(conn: sqlite3.Connection) -> pd.DataFrame:
  return pd.read_sql_query(
    """
      SELECT 
          customer_id,
          COUNT(*) as transaction_count,
          AVG(amount) as avg_amount,
          SUM(amount) as total_spent,
          MIN(timestamp) as first_transaction,
          MAX(timestamp) as last_transaction,
          ROUND(
              (JULIANDAY(MAX(timestamp)) - JULIANDAY(MIN(timestamp))) / NULLIF(COUNT(*) - 1, 0), 
              1
          ) as avg_days_between_transactions
      FROM clean_transactions
      GROUP BY customer_id
    """,
    conn
  )

def preview_features(df: pd.DataFrame) -> None:
  show_top_ten(df, "avg_days_between_transactions", True)
  show_top_ten(df, "total_spent", False)
  show_top_ten(df, "transaction_count", False)
  show_top_ten(df, "avg_amount", False)

def show_top_ten(df: pd.DataFrame, column: str, ascending: bool) -> None:
  sorted_df = df.sort_values(column, ascending=ascending)
  print(f"\nShowing top 10 of {column} {'ascending' if ascending else 'descending'}")
  print(sorted_df.head(10).to_string())