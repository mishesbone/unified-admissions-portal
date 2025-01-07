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

# Function to validate user input for creating an application
def validate_application_data(user_id, institution_id, program):
    """Validates data for creating a new application."""
    if not user_id:
        return False, "User ID is required"
    if not institution_id:
        return False, "Institution ID is required"
    if not validate_not_empty(program):
        return False, "Program name is required"
    return True, "Validation successful"

# Function to validate user input for creating a user
def validate_user_data(username, email, password):
    """Validates data for creating a new user."""
    if not validate_not_empty(username):
        return False, "Username is required"
    if not validate_email(email):
        return False, "Invalid email address"
    if not validate_password(password):
        return False, "Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    return True, "Validation successful"

# Function to validate user input for logging in
def validate_login_data(email, password):
    """Validates data for logging in a user."""
    if not validate_email(email):
        return False, "Invalid email address"
    if not validate_not_empty(password):
        return False, "Password is required"
    return True, "Validation successful"

# Function to validate user input for searching
def validate_search_query(query):
    """Validates search query."""
    if not validate_not_empty(query):
        return False, "Query is required"
    return True, "Validation successful"
        (Institution.location.ilike(f'%{query}%'))
    ).all()
#
#     # Serialize the results
     institutions_data = [{
            'id': institution.id,
            'name': institution.name,
            'location': institution.location,
            'description': institution.description
        } for institution in institutions]

    return jsonify(institutions_data), 200



# Function to validate user input for updating user details
def validate_update_user_data(username, email, password):
    """Validates data for updating user details."""
    if not validate_not_empty(username):
        return False, "Username is required"
    if not validate_email(email):
        return False, "Invalid email address"
    if not validate_password(password):
        return False, "Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    return True, "Validation successful"

# Function to validate user input for updating institution
def validate_update_institution_data(name, location, description):
    """Validates data for updating an institution."""
    if not validate_not_empty(name):
        return False, "Institution name is required"
    if not validate_not_empty(location):
        return False, "Institution location is required"
    if not validate_not_empty(description):
        return False, "Institution description is required"
    return True, "Validation successful"

# Function to validate user input for updating an application
def validate_update_application_data(program):
    """Validates data for updating an application."""
    if not validate_not_empty(program):
        return False, "Program name is required"
    return True, "Validation successful"

# Function to validate user input for deleting an institution
def validate_delete_institution_data(institution_id):
    """Validates data for deleting an institution."""
    if not institution_id:
        return False, "Institution ID is required"
    return True, "Validation successful"

# Function to validate user input for deleting an application
def validate_delete_application_data(application_id):
    """Validates data for deleting an application."""
    if not application_id:
        return False, "Application ID is required"
    return True, "Validation successful"

# Function to validate user input for deleting a user
def validate_delete_user_data(user_id):
    """Validates data for deleting a user."""
    if not user_id:
        return False, "User ID is required"
    return True, "Validation successful"
    (Institution.location.ilike(f'%{query}%'))
    ).all()

#     # Serialize the results
    institutions_data = [{
        'id': institution.id,
        'name': institution.name,
        'location': institution.location,
        'description': institution.description
    } for institution in institutions]

    return jsonify(institutions_data), 200

# # Function to validate user input for updating user details
def validate_update_user_data(username, email, password):
    """Validates data for updating user details."""
    if not validate_not_empty(username):
        return False, "Username is required"
    if not validate_email(email):
        return False, "Invalid email address"
    if not validate_password(password):
        return False, "Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    return True, "Validation successful"

    
