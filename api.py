from fastapi import FastAPI
from processes.rag import generate_response, retrieve, vectorize
from utils.filename_validation import validate_filename

app = FastAPI()

@app.post("/ask")
def ask(query: str, top_k: int, threshold: float):
  embedding = vectorize(query)
  context = retrieve(embedding, top_k, threshold)
  response = generate_response(query, context)
  return {"query": query, "response": response}

@app.post("/upload")
def upload(filename: str, content: str):
  validated_filename = validate_filename(filename)
  if type(validated_filename) == str:
    with open(f"./data/documents/{validated_filename}", "w") as file:
      file.write(content)
    return { "status": 200 }
  else:
    return { "status": 403, "details": validated_filename["reason"] }