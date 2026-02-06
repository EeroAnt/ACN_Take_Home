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

# Assumptions:

 - Transactions category not a required field, missing values acceptable
 - Transactions before signup are data errors, not backdated entries
 - Exchange rates are static, not date-adjusted.

# Trade-offs

|Decision|Pros|Cons|
|--|--|--|
|SQLite|Quick setup, simple, lightweight|Not suited for concurrent writes, no network access|
|Only preview the data|Quick implementation, demonstrates the logic|Does not support deeper analysis as is|
|Single main.py entrypoint|Easy to run, the whole script takes a second to finish|Less flexible for running parts independently|
|Mocked RAG|Quick to implement, hopefully easy to follow|Not the actual implementation|

# If I had more time

For the LLM-pipeline part, an actual RAG could be implemented and an LLM API could be called for the responses. Then my API would kind of serve as this "Chat with your own content" like service. Of course it would not be very handy to use through the uvicorn's interactive `/docs` endpoint, so a better UI could be in place.

For the Data engineering part, I think I would like to implement some flagging. Collect the faulty data for future inspection, and the customer ids of bigger customers in risk of churning.

I would also add unit tests for the transformation and anomaly detection logic.

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
- Made a mock RAG Q&A pipeline
- Hosted it locally with uvicorn and FastAPI
- Saved the feature table and churning risk data from part 2 to csv's
- Started working on the notebook

## Day 4
- Expanded the API
- Expanded the "RAG"
- Worked on documentation and presentation