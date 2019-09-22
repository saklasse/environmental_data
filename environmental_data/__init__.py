from flask import Flask
from environmental_data.main.controllers import main
from environmental_data.main.controllers import db
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = secrets.DB_CONNECTION_STRING
app.register_blueprint(main, url_prefix='/')

db.init_app(app)
