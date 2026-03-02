"""
Iterators
anything that can be looped over
list, tuple, set, dict, file objects
"""

"""
Generator expression
"""
data = [process(x) for x in large_dataset]

"""
Generator function
for memory efficiency
used in streaming apis
"""
def process_stream(data):
    for item in data:
        yield process(item)

"""
Streaming pattern
example
"""
def stream_response():
    for token in tokens:
        yield token
    
"""
Closures
A function remembering variables from its outer scope
"""
def multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

"""
Decorators
function wrappers
example timing wrapper
"""
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Time: {end - start:.4f}s")
        return result
    return wrapper

"""
Built in decorators
static method : method does'nt depend on instance
class method : works with class
property : attribute like access
"""
class User:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

