import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-this-to-a-long-random-secret"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///database.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")
    
   
   
   
    
       
       