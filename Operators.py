"""
== vs is
is only for None
== for value comparison
"""
if user_input == "":
    print("Input is empty")

if value is None:
    print("Value is None")

"""
logical operators
and, or, not
"""
if user_input and model_response:
    print("Both user input and model response are present")

"""
avoid vague boolean checks
"""
if flag:
    print("Flag is set to True")

"""
augmented assignment
"""
retry_count = 0
retry_count += 1