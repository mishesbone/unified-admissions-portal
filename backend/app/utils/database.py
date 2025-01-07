from app import db
from app.models import User, Institution, Application

# Function to add a new user to the database
def add_user(username, email, password_hash):
    new_user = User(username=username, email=email, password_hash=password_hash)
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        raise e

# Function to get a user by their ID
def get_user_by_id(user_id):
    return User.query.get(user_id)

# Function to get all users from the database
def get_all_users():
    return User.query.all()

# Function to add a new institution to the database
def add_institution(name, location, description):
    new_institution = Institution(name=name, location=location, description=description)
    try:
        db.session.add(new_institution)
        db.session.commit()
        return new_institution
    except Exception as e:
        db.session.rollback()
        raise e

# Function to get all institutions
def get_all_institutions():
    return Institution.query.all()

# Function to add a new application to the database
def add_application(user_id, institution_id, program):
    new_application = Application(user_id=user_id, institution_id=institution_id, program=program)
    try:
        db.session.add(new_application)
        db.session.commit()
        return new_application
    except Exception as e:
        db.session.rollback()
        raise e

# Function to get all applications
def get_all_applications():
    return Application.query.all()

# Function to delete an institution by ID
def delete_institution(institution_id):
    institution = Institution.query.get(institution_id)
    if institution:
        try:
            db.session.delete(institution)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return institution
    else:
        return None

# Function to delete a user by ID
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return user
    else:
        return None

# Function to update user details
def update_user(user_id, new_username=None, new_email=None, new_password_hash=None):
    user = User.query.get(user_id)
    if user:
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_password_hash:
            user.password_hash = new_password_hash
        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        return None
