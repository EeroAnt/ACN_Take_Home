def read_doc(filepath: str) -> str:
  with open(filepath, "r") as file:
    return file.read()