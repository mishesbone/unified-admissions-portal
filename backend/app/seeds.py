from app import create_app, db
from app.models import User, Institution, Application
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create a sample user
    new_user = User(username='johndoe', email='johndoe@example.com', password_hash=generate_password_hash('password123'))
    db.session.add(new_user)
    db.session.commit()

    # Create a sample institution
    new_institution = Institution(name='University of Example', location='Example City', description='A prestigious institution')
    db.session.add(new_institution)
    db.session.commit()

    # Create a sample application
    new_application = Application(user_id=new_user.id, institution_id=new_institution.id, program='Computer Science')
    db.session.add(new_application)
    db.session.commit()

    print("Sample data has been added.")
