import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app, flash, redirect, url_for
from functools import wraps
from flask_login import current_user

def send_mail(to,subject,message):
    print(current_app.config['SENDGRID_API_KEY'])
    message = Mail(
        from_email='tommywenjiezhang@gmail.com',
        to_emails=to,
        subject=subject,
        html_content=message)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        print(current_app.config['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.body)




def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('index_bp.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function