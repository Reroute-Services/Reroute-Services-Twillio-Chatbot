from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import os


app = Flask(__name__)


def sendMsg(to_number, from_number):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Hey! This is Ben From Reroute Services.",
                        from_=from_number,
                        to=to_number)

    print(message.sid)


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a 'Hello world' message"""
    # Start our TwiML response
    # print(type(request.values))
    caller_no = request.form['From']
    to_number = request.form['To']
    # print(request.values)
    resp = VoiceResponse()

    # Read a message aloud to the caller
    # resp.say("Hello! This is a Test Call for Reroute Services!", voice='Polly.Amy')
    # resp.say("Hello! This is a Test Call for Reroute Services!")
    resp.say("Now Hanging Up!")
    resp.hangup()

    sendMsg(caller_no, to_number)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
