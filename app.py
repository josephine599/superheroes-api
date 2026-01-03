from flask import Flask
from flask_cors import CORS
from config import Config, db, migrate
from routes import api



app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api)

db.init_app(app)
migrate.init_app(app, db)

from models import Hero, Power, HeroPower

CORS(app)

@app.route("/")
def home():
    return {"message": "Superheroes API is running"}

if __name__ == "__main__":
    app.run(port=5555, debug=True)
