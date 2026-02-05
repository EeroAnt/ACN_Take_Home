import pandas as pd
import sqlite3

from utils.logging_config import logger


def feature_report(conn: sqlite3.Connection) -> pd.DataFrame:
  logger.info("Creating and previewing feature tables")
  feature_df = get_feature_dataframe(conn)
  churning_risk_df = get_churning_risk_df(conn)
  preview_features(feature_df, churning_risk_df)
  logger.info("Saving the data to csv for downstream use")
  save_feature_tables(feature_df, churning_risk_df)
    

def get_feature_dataframe(conn: sqlite3.Connection) -> pd.DataFrame:
  return pd.read_sql_query(
    """
      SELECT 
          customer_id,
          COUNT(*) as transactions,
          ROUND(AVG(amount), 2) as avg_spent,
          ROUND(MAX(amount), 2) as max_spent,
          ROUND(MIN(amount), 2) as min_spent,
          SUM(amount) as total_spent,
          MIN(timestamp) as first_transaction,
          MAX(timestamp) as last_transaction,
          ROUND(
              (JULIANDAY(MAX(timestamp)) - JULIANDAY(MIN(timestamp))) / NULLIF(COUNT(*) - 1, 0), 
              1
          ) as purchase_interval
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
          COUNT(*) as transactions,
          SUM(amount) as total_spent,
          ROUND(
              (JULIANDAY(MAX(timestamp)) - JULIANDAY(MIN(timestamp))) / NULLIF(COUNT(*) - 1, 0), 
              1
          ) as purchase_interval,
          ROUND(JULIANDAY('2020-12-31') - JULIANDAY(MAX(timestamp))) as days_since_last_transaction
      FROM clean_transactions
      GROUP BY customer_id
      HAVING transactions > 4
    """,
    conn
  )

def preview_features(feature_df: pd.DataFrame, churning_risk_df: pd.DataFrame) -> None:
  print()
  show_top_ten(feature_df, "purchase_interval", True)
  show_top_ten(feature_df, "total_spent", False)
  show_top_ten(feature_df, "transactions", False)
  show_top_ten(feature_df, "max_spent", False)
  show_top_ten(churning_risk_df, "days_since_last_transaction", False)

def show_top_ten(df: pd.DataFrame, column: str, ascending: bool) -> None:
  sorted_df = df.sort_values(column, ascending=ascending)
  print(f"Showing top 10 of {column} {'ascending' if ascending else 'descending'}")
  print(sorted_df.head(10).to_string())
  print()

def save_feature_tables(feature_df: pd.DataFrame, churning_risk_df: pd.DataFrame) -> None:
  feature_df.to_csv("data/customer_features.csv", index=False)
  churning_risk_df.to_csv("data/churning_risks.csv", index=False)