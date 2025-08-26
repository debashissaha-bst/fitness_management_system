from flask import Flask
from .extensions import mongo, jwt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    CORS(app)
    mongo.init_app(app)
    jwt.init_app(app)

    from .auth.routes import auth_bp
    from .routes import meal_plans_bp, badges_bp, challenges_bp, preferences_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(meal_plans_bp, url_prefix='/api')
    app.register_blueprint(badges_bp, url_prefix='/api')
    app.register_blueprint(challenges_bp, url_prefix='/api')
    app.register_blueprint(preferences_bp, url_prefix='/api')

    return app
