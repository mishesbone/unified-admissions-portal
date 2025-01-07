# This file can be left empty to mark the 'utils' directory as a package,
# or you can import utility functions and classes here to make them globally accessible.

from .utils import hash_password, verify_password
from .email import send_email

# Now, functions from utils and email modules can be accessed directly from 'utils'.
