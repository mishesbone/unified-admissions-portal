#run.py
#

# Import the create_app function from app/__init__.py

from app import create_app

# Create the app using the configuration from config.py
app = create_app()

# Run the application if this file is run directly
if __name__ == '__main__':
    app.run(debug=True)  # Set to `False` in production

