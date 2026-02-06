from random import random

from utils.file_reader import get_filenames, read_doc
from utils.logging_config import logger

def run_rag_demo():
  logger.info("1. User inputs a query")
  logger.info("2. User input would be vectorized with an embedding model")
  embedding = vectorize()
  logger.info("3. This vector would be used to query a vector database with cosine similarity")
  logger.info("4. top-k best matches over a threshold value are returned for context")
  context = retrieve(embedding, top_k=2, threshold=0.6)
  logger.info("5. Users query and context are passed to an LLM")
  logger.info("6. LLM is prompted to base its response to the given context")
  response = generate_response(context)
  logger.info("7. The user receives the response:")
  print()
  print(response)


def retrieve(vector: list[float], top_k: int, threshold: float) -> dict:
  # I created a mock embedding, by randomizing a float between 0 and 1 for each
  # file in the directory. Instead of implementing a cosine similarity and vectorizing the
  # documents, I decided to treat each float as the cosine similarity value for each 
  # corresponding file. 
  context = {}
  filenames = get_filenames()
  scores = {}
  # Give each filename their mock cosine similarity value
  for idx, filename in enumerate(filenames):
    scores[filename] = vector[idx]
  # Sort the filenames by said values
  top_results = sorted(scores, key=scores.get, reverse=True)
  # Get top-k results that are over the threshold value 
  for result in top_results[:top_k]:
    if scores[result] > threshold:
      context[result] = read_doc(f"./data/documents/{result}")
  return context

def generate_response(context) -> str:
  response = "Hi! I'm your happy assistant!\n"
  if context:
    response += "I'm basing my helpful response to the following contents:\n"
    for item in context:
      response +=f"\n{item}\n{context[item]}\n"
  else:
    response += "This time we did not find what you were looking for."
  
  return response

def vectorize(query: str = "This is a query.") -> list[float]:
  embedding = []
  logger.info(f"Vectorizing query: {query}")
  files = get_filenames()
  for _ in files:
    embedding.append(random())
  return embedding
