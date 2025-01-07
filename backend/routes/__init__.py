#backend/routes/__init__.py
#
from flask import Blueprint
from app.routes.institutions import institutions_bp
from app.routes.students import students_bp
from app.routes.search import search_bp
