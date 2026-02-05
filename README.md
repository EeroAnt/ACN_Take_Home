# Setup

This project uses uv for dependency management. To run with uv:

1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
2. Run `uv sync` in the project folder
3. Run `uv run python main.py`

Alternatively, if you have Python and pandas installed, you can run directly:

`python main.py`

To run and test the "API": 

1. Start it locally `uv run uvicorn api:app`
2. Visit http://localhost:8000/docs for an interactive demo

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

## Day 3
- Added Churning risk analysis and revised the feature tables
- Structured the code and its outputs more
- Make a mock up RAG Q&A pipeline
- Host it locally with uvicorn and FastAPI
- Save the feature table and churning risk data from part 2 to csv's
- Start working on the notebook