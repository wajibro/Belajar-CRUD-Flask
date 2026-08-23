import os
import importlib
from flask import Flask
from supabase import create_client, Client
from app.config import Config

supabase = create_client(Config.DB_URL, Config.DB_KEY)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.main import main_bp

    app.register_blueprint(main_bp)

    return app