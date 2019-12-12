
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import requests as r
import re

app = Flask(__name__)


@app.route("/bot", methods=['GET', 'POST'])
def incoming_sms():

    body_text = request.values.get('Body', None).lower().split()

    resp = MessagingResponse()

    if all(each in ['hello', 'hi', 'welcome', 'howdy', 'speak', 'hey'] for each in body_text):

        quote_ = '\U0001f44b Welcome to this SMS-based document retrieval service for the 2019 General Rate Case. \n\n \u2705 Please request files using the format \'Please send me file 2019XXX\' where \'XXX\' is a number between 000 and 518.' + ' \n\n \u2705 For the index of all files that can be requested, visit: https://github.com/grantaguinaldo/grc/blob/master/misc/grc_2019_file_index.csv'
        resp.message(quote_)

    elif 'file' in body_text:

        conn_string = 'https://grc-api.herokuapp.com/api?fileidx=' + [(each) for each in body_text if each.isdigit()][0]

        r_ = r.get(conn_string)
        if r_.status_code == 200:
            data = r_.json()['file_url']['0']
            resp.message(data)

        else:
            quote_ = 'I could not retrieve your document at this time, sorry.'
            resp.message(quote_)

    elif 'bye' in body_text:
        resp.message("Goodbye thanks for stopping by.")

    else:
        resp.message("I don't understand what you are asking for.")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
