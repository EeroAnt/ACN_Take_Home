import os

def read_doc(filepath: str) -> str:
  with open(filepath, "r") as file:
    return file.read()

def get_filenames():
    folder_path = "./data/documents/"
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]