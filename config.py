import os

class Config:
    SECRET_KEY = "change-this-to-a-long-random-secret"

    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    