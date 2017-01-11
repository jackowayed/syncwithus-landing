import os

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from mailchimp3 import MailChimp

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

def mailchimp_client():
    user = os.environ.get('MAILCHIMP_USER')
    secret = os.environ.get('MAILCHIMP_SECRET')
    enabled = os.environ.get('MAILCHIMP_ENABLE', 'false').lower()[0] == 't'
    return MailChimp(user, secret, enabled)

MAILCHIMP_LIST = os.environ.get('MAILCHIMP_LIST')
MAILCHIMP = mailchimp_client()

app = create_app()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    MAILCHIMP.lists.members.create(MAILCHIMP_LIST, {
        'email_address': email,
        'status': 'subscribed'
    })
    return "ok " + email
