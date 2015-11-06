import pusher, pusher.gae

import os
import cgi
from flask import Flask, render_template, request
import json

import logging

app = Flask(__name__)

app_id = os.environ.get('PUSHER_APP_ID')
key = os.environ.get('PUSHER_APP_KEY')
secret = os.environ.get('PUSHER_APP_SECRET')

p = pusher.Pusher(
  app_id=app_id,
  key=key,
  secret=secret,
  backend=pusher.gae.GAEBackend
)

@app.route("/")
def show_index():
    return render_template('index.html')

@app.route("/notification", methods=['POST'])
def trigger_notification():
	message =  cgi.escape(request.form['message'])
	p.trigger('notifications', 'new_notification', {'message': message})
	return "Notification triggered!"

if __name__ == "__main__":
    app.run(debug=True)