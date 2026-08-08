import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-this-to-a-long-random-secret"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///database.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "kodumeleng7@gmail.com"
    MAIL_PASSWORD = "mmuwybdtkyslstmb"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME