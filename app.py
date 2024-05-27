#!/usr/bin/python3
"""
entry point of my flask app
"""
from models import storage
from models.user import User
from api.views import api_views
from web_routes import web_routes
from flask import Flask, make_response, jsonify
from flask_login import LoginManager
from flask_cors import CORS
from flasgger import Swagger
from get_key import get_key

app = Flask("__name__")
app.config['SECRET_KEY'] = get_key('secret_key')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(api_views)
app.register_blueprint(web_routes)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SWAGGER'] = {
    'title': 'Edukid API',
    'uiversion': 1
}
Swagger(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You are logged in'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
