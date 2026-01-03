from flask import Flask
from flask_cors import CORS
from config import Config, db, migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

CORS(app)

@app.route("/")
def home():
    return {"message": "Superheroes API is running"}

if __name__ == "__main__":
    app.run(port=5555, debug=True)
