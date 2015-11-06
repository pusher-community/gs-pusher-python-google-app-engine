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

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
  auth = p.authenticate(
          channel=request.form['channel_name'],
          socket_id=request.form['socket_id'],
          custom_data={
            u'user_id': u'1'
          }
  )
  return json.dumps(auth)

@app.route("/webhook", methods=['POST'])
def pusher_webhook():
  webhook = p.validate_webhook(
    key=request.headers.get('X-Pusher-Key'),
    signature=request.headers.get('X-Pusher-Signature'),
    body=request.data
  )

  events = webhook['events']
  
  for event in webhook['events']:
    if event['name'] == "channel_occupied":
      print("Channel occupied: %s" % event["channel"])
    elif event['name'] == "channel_vacated":
      print("Channel vacated: %s" % event["channel"])

  return "ok"


if __name__ == "__main__":
    app.run(debug=True)