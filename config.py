import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_key")
    AUTH_DB_PATH = os.environ.get("AUTH_DB_PATH", "auth.db")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "secure_healthcare")
    MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "patient_records")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"