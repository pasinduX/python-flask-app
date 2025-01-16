from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from app.config import Config

db=None

def create_app():
    global db
    app=Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    client = MongoClient(app.config["MONGO_URI"])
    db = client[app.config["DB_NAME"]]
    
    with app.app_context():
        from app.routes import crud_blueprint
        app.register_blueprint(crud_blueprint,url_prefix="/api")
    return app    