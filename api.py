from fastapi import FastAPI
from processes.rag import retrieve, generate_response

app = FastAPI()

@app.post("/ask")
def ask(query: str):
    context = retrieve()
    response = generate_response(context)
    return {"query": query, "response": response}