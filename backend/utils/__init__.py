# This file can be left empty to mark the 'utils' directory as a package,
# or you can import utility functions and classes here to make them globally accessible.

# Import the functions from the utils and email modules
from .utils import hash_password, verify_password

from .email import send_email

# Now, functions from utils and email modules can be accessed directly from 'utils'.
# For example, to hash a password, you can call 
utils.hash_password(password)

# or to send an email, you can call
utils.send_email(subject, recipient, body)



