from server import mail
from flask import current_app, render_template
from  flask_mail import Message

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )

    mail.send(msg)

if __name__ == '__main__':
    send_email('wenjie.zhang.developer@gmail.com','hello', render_template('activate.html'))
