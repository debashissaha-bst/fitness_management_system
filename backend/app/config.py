import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/fitness_companion")