def extract_from_csv(filepath: str) -> list[tuple]:

  results = []

  with open(filepath, "r") as file:
    for line in file.readlines()[1:]:
      results.append(tuple(line.strip().split(",")))

  return results