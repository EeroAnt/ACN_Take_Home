def extract_from_csv(filepath: str) -> list[tuple]:

  results = []

  with open(filepath, "r") as file:
    # both csv's in the task had headers, thus hardcoded [1:]
    for line in file.readlines()[1:]:
      results.append(tuple(line.strip().split(",")))

  return results