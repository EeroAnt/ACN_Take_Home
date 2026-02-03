def extract_from_csv(filepath: str) -> list[tuple]:

  results = []

  with open(filepath, "r") as file:
    for line in file.readlines():
      results.append(tuple(line.strip().split(",")))

  return results