from flask import Flask
from app.webhook.routes import webhook
from .extensions import mongo

# Creating our flask app
def create_app():
    app = Flask(__name__)

    # registering all the blueprints

    app.register_blueprint(webhook)

    app.config["MONGO_URI"] = "mongodb://localhost:27017/techstax"

    mongo.init_app(app)

    return app
