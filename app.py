import os

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from mailchimp3 import MailChimp

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

def mailchimp_client():
    user = os.environ.get('MAILCHIMP_USER', 'no_user')
    secret = os.environ.get('MAILCHIMP_SECRET', 'no-secret')
    enabled = os.environ.get('MAILCHIMP_ENABLE', 'false').lower()[0] == 't'
    return MailChimp(user, secret, enabled)

MAILCHIMP_LIST = os.environ.get('MAILCHIMP_LIST', 'nolist')
MAILCHIMP = mailchimp_client()

app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/subscribed')
def subscribed():
    return render_template('subscribed.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """ Add or update member of list """
    try:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form['email']
        result = MAILCHIMP.lists.update_members(list_id=MAILCHIMP_LIST, data={
            'update_existing': True,
            'members': [{
                'email_address': email,
                'status': 'subscribed',
                'merge_fields': {
                    'FNAME': fname,
                    'LNAME': lname,
                    'email_address': email,
                }
            }],
        })
    except Exception as err:
        print '\n======= ERROR ======\n', err
        return redirect(url_for('home'))

    return redirect(url_for('subscribed'))
