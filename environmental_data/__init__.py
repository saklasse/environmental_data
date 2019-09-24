from flask import Flask, g, abort
from flask_babel import Babel
from environmental_data.main.controllers import main
from environmental_data.main.controllers import db
import secrets
import environmental_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = secrets.DB_CONNECTION_STRING
app.config.from_object('config.DevelopmentConfig')
babel = Babel(app)
db.init_app(app)

@babel.localeselector
def get_locale():
    return g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])

@babel.timezoneselector
def get_timezone():
    user = g.get('user', None)
    if user is not None:
        return user.timezone
    
@app.url_defaults
def set_language_code(endpoint, values):
    if 'lang_code' in values or not g.get('lang_code', None):
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code
        
@app.url_value_preprocessor
def get_lang_code(endpoint, values):
    if values is not None:
        g.lang_code = values.pop('lang_code', None)
        
@app.before_request
def ensure_lang_support():
    lang_code = g.get('lang_code', None)
    if lang_code and lang_code not in app.config['SUPPORTED_LANGUAGES'].keys():
        return abort(404)
    
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(main, url_prefix='/<lang_code>/')
