from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

# App Config
app = Flask(__name__, )
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


# Database
from config import secret
app.secret_key = secret
migrate = Migrate(app, db)


# Controllers
from app.user.controller import bp as user_bp
app.register_blueprint(user_bp)
from app.search.controller import bp as search_bp
app.register_blueprint(search_bp)
from app.ussd.controller import bp as ussd_bp
app.register_blueprint(ussd_bp)

# Error handlers
from .error_handlers import *