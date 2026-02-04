# Setup

This project uses uv for dependency management. To run with uv:

1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
2. Run `uv sync` in the project folder
3. Run `uv run python main.py`

Alternatively, if you have Python and pandas installed, you can run directly:

`python main.py`

---

# Development Log

## Day 1
- Set up repository and initialized uv project
- Extracted data from CSVs
- Transformed data (type conversions, normalization)
- Created and populated initial tables (customers, transactions)

## Day 2
- Added logging
- Enhanced transformation: convert empty strings to NULL
- Implemented anomaly detection checks
- Created clean_transactions view based on anomaly findings
- Built initial customer feature table
- Discovered duplicate transactions through feature analysis