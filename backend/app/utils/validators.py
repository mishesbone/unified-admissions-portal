import re
from werkzeug.security import check_password_hash

# Function to validate email format
def validate_email(email):
    """Validates email address using regex."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    return False

# Function to validate password strength
def validate_password(password):
    """Validates password strength."""
    if len(password) < 8:
        return False  # Password must be at least 8 characters
    if not re.search(r'[A-Z]', password):  # At least one uppercase letter
        return False
    if not re.search(r'[a-z]', password):  # At least one lowercase letter
        return False
    if not re.search(r'[0-9]', password):  # At least one number
        return False
    if not re.search(r'[@$!%*?&]', password):  # At least one special character
        return False
    return True

# Function to compare password with its hashed value
def validate_password_match(stored_password_hash, password):
    """Validates if the given password matches the stored password hash."""
    return check_password_hash(stored_password_hash, password)

# Function to validate that a string is not empty
def validate_not_empty(value):
    """Validates that a string is not empty."""
    return bool(value.strip())

# Function to validate user input for creating an institution
def validate_institution_data(name, location, description):
    """Validates data for creating a new institution."""
    if not validate_not_empty(name):
        return False, "Institution name is required"
    if not validate_not_empty(location):
        return False, "Institution location is required"
    if not validate_not_empty(description):
        return False, "Institution description is required"
    return True, "Validation successful"

# Function to validate program name (for application)
def validate_program_name(program):
    """Validates program name input for application."""
    if not validate_not_empty(program):
        return False, "Program name is required"
    return True, "Validation successful"
