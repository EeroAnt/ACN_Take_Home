from utils.file_reader import get_filenames

ValidationObject = dict[str, str | bool]

def validate_filename(filename) -> str | ValidationObject:
  if filename.endswith('.txt'):
    if '.' in filename[:-4]:
      return { "success": False, "reason": "Invalid filename" }
  else:
    if '.' in filename:
      return { "success": False, "reason": "Invalid filename" }
    filename += '.txt'

  if filename in get_filenames():
    return { "success": False, "reason": "Duplicate filename" }
  
  return filename