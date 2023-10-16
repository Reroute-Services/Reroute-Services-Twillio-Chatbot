from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from chatbot import ChatBot
import os


app = Flask(__name__)

CHAT_SESSIONS = {}


def chat_session_handler(caller_no, to_number, message_body=None):
    if caller_no not in CHAT_SESSIONS:
        body = "You just missed a call from {}".format(caller_no)
        CHAT_SESSIONS[caller_no] = ChatBot()
        response_body = CHAT_SESSIONS[caller_no].chat_agent(body)
        sendMsg(caller_no, to_number, response_body)
    else:
        response_body = CHAT_SESSIONS[caller_no].chat_agent(message_body)
        return response_body


def sendMsg(to_number, from_number, body):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=from_number,
        to=to_number,
        # max_price=0.0075
        )
    
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

    chat_session_handler(caller_no, to_number)

    # sendMsg(caller_no, to_number)

    return str(resp)

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    print("Message: ", request.values)
    from_no = request.form['From']
    to_number = request.form['To']
    message_body = request.form['Body']

    response_msg = chat_session_handler(from_no, to_number, message_body=message_body)

    resp = MessagingResponse()

    # Add a message
    # resp.message("The Robots are coming! Head for the hills!")
    resp.message(response_msg)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
