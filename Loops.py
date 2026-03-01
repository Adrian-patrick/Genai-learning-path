"""
basic for loops
"""
for chunk in document_chunks:
    process(chunk)

"""
enumerate when position is required
"""
for index, chunk in enumerate(document_chunks):
    process(chunk, index)

"""
Guard clauses in loops
"""
for item in data:
    if not item:
        continue
    if len(item) > 100:
        continue
    process(item)

"""
handling errors in loops
"""
for item in data:
    try:
        process(item)
    except Exception as e:
        logging.error(f"Error processing item {item}: {e}")

"""
retry mechanism using while loop
"""
attempt = 0
max_retries = 3
while attempt < max_retries:
    try:
        return call_api()
    except Exception:
        attempt += 1