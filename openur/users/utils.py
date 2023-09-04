# Desc: Utility functions for the users package
# users/utils.py

import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from openur import mail
from flask import current_app as app


def _save_picture(form_picture):
    # Create a unique filename
    picture_fn = f"{secrets.token_hex(8)}{os.path.splitext(form_picture.filename)[1]}"
    
    # Check if a file with the same name exists; if so, generate a new name
    while os.path.exists(os.path.join(app.root_path, 'static/profile_pics', picture_fn)):
        picture_fn = f"{secrets.token_hex(8)}{os.path.splitext(form_picture.filename)[1]}"
    
    # Define the path for the picture
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    # Resize and save the picture
    output_size = (125, 125)
    with Image.open(form_picture) as img:
        img.thumbnail(output_size)
        img.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='muslimbekisakov@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

Shall you think something is wrong, ignore this email and no changes will be made.
'''
    mail.send(msg)