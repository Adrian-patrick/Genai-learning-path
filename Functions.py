"""
high order functions
functions that can take other functions as arguments or return functions as results
"""

"""
passing functions as arguments
"""
def apply_operation(a: int, b: int, operation):
    return operation(a, b)

"""
returning functions
"""
def create_multiplier(factor: int):
    def multiplier(x: int) -> int:
        return x * factor
    return multiplier

"""
readability and clarity
"""
valid_prompts = list(filter(lambda p: len(p) > 10, prompts))

"""
lambda functions
transformation example
"""
lowered = list(map(lambda s: s.lower(), strings))

"""
industry example
"""
def process_data(data, transform_fn):
    return [transform_fn(item) for item in data]

process_data(data, lambda x: x.strip())
process_data(data, lambda x: x.lower())