import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from .models import db
from .routes import movies_bp


load_dotenv()

def create_app():
    app = Flask(__name__)

  
    db_uri = os.getenv('INVENTORY_DATABASE_URL')

    if not db_uri:
        # Help yourself debug: if it's missing, show exactly where the app is looking
        raise RuntimeError(
            f"SQLALCHEMY_DATABASE_URI is not set. "
            f"Current Working Dir: {os.getcwd()}"
        )

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(movies_bp, url_prefix='/api')

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    with app.app_context():
        db.create_all()

    return app