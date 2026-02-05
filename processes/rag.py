from random import sample, randint

from utils.file_reader import read_doc
from utils.logging_config import logger

def run_rag_demo():
  logger.info("1. User inputs a query")
  logger.info("2. User input would be vectorized with an embedding model")
  logger.info("3. This vector would be used to query a vector database with cosine similarity")
  logger.info("4. top-k best matches over a threshold value are returned for context")
  context = retrieve()
  logger.info("5. Users query and context are passed to an LLM")
  logger.info("6. LLM is prompted to base its response to the given context")
  response = generate_response(context)
  logger.info("7. The user receives the response:")
  print()
  print(response)


def retrieve() -> dict:
  # I'm going to simulate a vector search (top-2, with a threshold value) of an
  # arbitrary user input by choosing 0-2 documents at random to retrieve as context.
  result = {}
  filenames = ["customer_support_faq.txt", "fraud_guidelines.txt" ,"product_policy.txt"]
  mock_threshold_functionality = randint(0,2)
  mock_vector_search_result = sample(filenames, mock_threshold_functionality)
  for filename in mock_vector_search_result:
    result[filename] = read_doc(f"./data/documents/{filename}")
  return result

def generate_response(context) -> str:
  response = "Hi! I'm your happy assistant!\n"
  if context:
    response += "I'm basing my helpful response to the following contents:\n"
    for item in context:
      response +=f"\n{item}\n{context[item]}\n"
  else:
    response += "This time we did not find what you were looking for."
  
  return response
