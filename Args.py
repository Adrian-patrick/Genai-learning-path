"""
*args : variable number of positional arguments
**kwargs : variable number of keyword arguments
"""
def example_function(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)
example_function(1, 2, 3, name="Alice", age=30)
