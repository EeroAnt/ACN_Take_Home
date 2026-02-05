import pandas as pd
import sqlite3

def feature_report(conn: sqlite3.Connection) -> pd.DataFrame:
  feature_df = get_feature_dataframe(conn)
  churning_risk_df = get_churning_risk_df(conn)
  preview_features(feature_df, churning_risk_df)
    

def get_feature_dataframe(conn: sqlite3.Connection) -> pd.DataFrame:
  return pd.read_sql_query(
    """
      SELECT 
          customer_id,
          COUNT(*) as transaction_count,
          ROUND(AVG(amount), 2) as avg_amount,
          ROUND(MAX(amount), 2) as max_amount,
          ROUND(MIN(amount), 2) as min_amount,
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

def get_churning_risk_df(conn: sqlite3.Connection) -> pd.DataFrame:
  return pd.read_sql_query(
    """
      SELECT 
          customer_id,
          COUNT(*) as transaction_count,
          SUM(amount) as total_spent,
          ROUND(
              (JULIANDAY(MAX(timestamp)) - JULIANDAY(MIN(timestamp))) / NULLIF(COUNT(*) - 1, 0), 
              1
          ) as avg_days_between_transactions,
          ROUND(JULIANDAY('2020-12-31') - JULIANDAY(MAX(timestamp))) as days_since_last_transaction
      FROM clean_transactions
      GROUP BY customer_id
      HAVING transaction_count > 4
    """,
    conn
  )

def preview_features(feature_df: pd.DataFrame, churning_risk_df: pd.DataFrame) -> None:
  show_top_ten(feature_df, "avg_days_between_transactions", True)
  show_top_ten(feature_df, "total_spent", False)
  show_top_ten(feature_df, "transaction_count", False)
  show_top_ten(feature_df, "max_amount", False)
  show_top_ten(churning_risk_df, "days_since_last_transaction", False)

def show_top_ten(df: pd.DataFrame, column: str, ascending: bool) -> None:
  sorted_df = df.sort_values(column, ascending=ascending)
  print(f"\nShowing top 10 of {column} {'ascending' if ascending else 'descending'}")
  print(sorted_df.head(10).to_string())