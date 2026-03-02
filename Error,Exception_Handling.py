"""
clear fail cases
"""
if not config:
    raise ValueError("Configuration is missing.")

"""
catch fixable errors
"""
try:
    call_api()
except TimeoutError:
    retry()

"""
Specific exceptions
"""
except ValueError:
except TimeoutError:
except ConnectionError:

"""
log + re-raise
"""
try:
    generate_embedding(text)
except Exception as error:
    logger.error(f"Embedding failed: {error}")
    raise

"""
Custom exceptions
domain spceific
"""
class InvalidModelError(Exception):
    pass

"""
retry pattern (important for apis)
"""
attempt = 0
while attempt < 3:
    try:
        return call_model()
    except TimeoutError:
        attempt += 1

raise RuntimeError("Model failed after retries.")
