"""
guard clauses
validating early
"""
if not user:
    raise ValueError("User not found")

"""
removing unnecessary else
"""
if not valid:
    return False
process()

"""
explicit check
"""
if temperature is None:
    raise ValueError("Temperature is required")

"""
using in for multi condition checks
"""
if role in ["admin", "editor"]:
    grant_access()

"""
chaining comparisons
"""
if 0 <= temperature <= 1:
    print("Temperature is valid")

"""
failsafes
"""
if not config:
    raise ValueError("Configuration is missing")
