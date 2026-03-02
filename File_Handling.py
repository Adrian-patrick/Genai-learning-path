"""
Context manager (with)
automatically closes file
"""
with open("data.txt", "r", encoding="utf-8") as file:
    data = file.read()

"""
Specifying encoding
"""
with open("data.txt", "r", encoding="utf-8") as file:
    pass
"""
never trust file content
always check
"""
with open("config.json", "r", encoding="utf-8") as file:
    content = file.read()

if not content.strip():
    raise ValueError("Config file is empty.")

"""
handle exceptions around the file
use try and except
"""
try:
    with open("data.txt", "r", encoding="utf-8") as file:
        data = file.read()
except FileNotFoundError:
    raise FileNotFoundError("Data file not found.")

"""
large file processing
"""
with open("large.txt", "r", encoding="utf-8") as file:
    for line in file:
        process(line)

"""
writing files safely
"""
with open("output.txt", "w", encoding="utf-8") as file:
    file.write("Result")

"""
json loading
"""
import json

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

"""
json writing
"""
with open("output.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)