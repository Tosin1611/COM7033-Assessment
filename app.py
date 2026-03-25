from flask import Flask
from config import Config
from db.sqlite_auth import init_auth_db, seed_default_users
from db.mongo_records import init_mongo_records
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from routes.clinician_routes import clinician_bp
from routes.admin_routes import admin_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    init_auth_db(app.config["AUTH_DB_PATH"])
    seed_default_users(app.config["AUTH_DB_PATH"])
    init_mongo_records(
        app.config["MONGO_URI"],
        app.config["MONGO_DB_NAME"],
        app.config["MONGO_COLLECTION"]
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(clinician_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)