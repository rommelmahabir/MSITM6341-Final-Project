"""
app.py - creates the Flask app and connects all the pieces.

Run from the project folder:
    python3 app.py        (Windows: python app.py)
Then open http://127.0.0.1:5001 in a browser.
"""

import os

from dotenv import load_dotenv
from flask import Flask

from data import db
from routes.api import api_bp
from routes.pages import pages_bp

# Read settings from .env into environment variables.
# If .env is missing, this does nothing and the defaults below are used.
load_dotenv()

# Folder this file lives in, so the database lands in the project folder
# no matter which folder you run the command from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app(test_config=None):
    """Build and return the Flask app (the 'app factory' pattern)."""
    app = Flask(__name__)

    # Settings: from .env if present, otherwise safe development defaults
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-change-me")
    db_file = os.getenv("DATABASE_PATH", "trip_planner.db")
    app.config["DATABASE"] = os.path.join(BASE_DIR, db_file)

    # Tests pass their own settings (for example, a throwaway database)
    if test_config:
        app.config.update(test_config)

    # Wire up the layers
    db.init_app(app)                                  # data layer: tables ready
    app.register_blueprint(pages_bp)                  # HTML pages at /
    app.register_blueprint(api_bp, url_prefix="/api") # JSON routes at /api/...

    return app


if __name__ == "__main__":
    app = create_app()
    # Port 5001, not Flask's default 5000: on Macs, AirPlay Receiver uses 5000.
    app.run(debug=True, port=5001)