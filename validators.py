import re
from pydantic import field_validator

# validate password
def validate_password_strength(v: str) -> str:
    if len(v) < 4:
        raise ValueError('Password must be at least 4 characters long')
    if not re.search(r'[A-Z]', v):
        raise ValueError('Password must contain at least one uppercase letter, a special character and a number')
    if not re.search(r'[0-9]', v):
        raise ValueError('Password must contain at least one uppercase letter, a special character and a number')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
        raise ValueError('Password must contain at least one uppercase letter, a special character and a number')
    return v

# validate title and description 
def validate_whitespace(v: str, field_name: str) -> str:
    if not v or not v.strip():
        raise ValueError(f'{field_name} cannot be empty or contain only whitespace')
    return v.strip()

#validate minimum length after trimming whitespace
def validate_min_length(v: str, min_length: int, field_name: str) -> str:
    if len(v) < min_length:
        raise ValueError(f'{field_name} must be at least {min_length} characters long')
    return v