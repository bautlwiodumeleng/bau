import cloudinary
from flask import current_app


def configure_cloudinary():
    cloudinary.config(
        cloud_name=current_app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=current_app.config["CLOUDINARY_API_KEY"],
        api_secret=current_app.config["CLOUDINARY_API_SECRET"],
        secure=True
    )
    
    
    
    if ($env:CLOUDINARY_CLOUD_NAME) "dlicjwc"
if ($env:CLOUDINARY_API_KEY)  "427467312848427" 
if ($env:CLOUDINARY_API_SECRET)  "CBypz_sxAZhn7A-ofotE2uvVpBI" 