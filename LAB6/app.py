# app.py
from flask import Flask, jsonify

from models.database import db
from flask_swagger_ui import get_swaggerui_blueprint
from models.electro_scooter import ElectroScooter

from models.electro_scooter import ElectroScooter
def create_app():
    app = Flask(__name__)

    # Configure SQLAlchemy to use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

    db.init_app(app)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app-name': 'Electro Scooter API'
        }
    )

    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

    return app

if __name__ == "__main__":
    app = create_app()
    import routes
    app.run()