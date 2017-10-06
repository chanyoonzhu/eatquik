"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""



from __future__ import print_function

import env
import requests
import json
from yelpcall import query_api


query_api('restaurant', '303 Wadsack Dr, Norman, Oklahoma')

# --------------- Helpers that build all of the responses ----------------------
#url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&type=restaurant&keyword=cruise&key=AIzaSyBOimD8S4Ifw8o1XBEEFO7YKylK9d0sSJk'
#r = requests.get(url)

userAddress = ''
"""
'card': {
    'type': 'Simple',
    'title': "SessionSpeechlet - " + title,
    'content': "SessionSpeechlet - " + output
},
"""


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        "card": {
          "type": "AskForPermissionsConsent",
          "permissions": [
            "read::alexa:device:all:address"
          ]
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    # speech_output = r.json()['results'][0]['name']
    speech_output = "Welcome to Eatquick"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session, context):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    if intent_name == 'GetNearbyRestaurants':
        deviceId = ''
        consentToken = ''

        try:
            deviceId = context['System']['device']['deviceId'] 
            consentToken = context['System']['user']['permissions']['consentToken']
        except:
            deviceId = ''
            consentToken = ''
        
        if not (deviceId and consentToken):
            # user permission not granted, send out prompt message and a new permission card
            session_attributes = {}
            card_title = ''
            reprompt_text = ''
            should_end_session = True
            speech_output = 'eatquick cannot function without address information. '\
            'To permit access to address information, enable eatquick again, and consent to provide address information in the Alexa app.'

            return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
        
        else:
        
            deviceId = context['System']['device']['deviceId'] 
            consentToken = context['System']['user']['permissions']['consentToken']
        
            URL =  "https://api.amazonalexa.com/v1/devices/{}/settings" \
                "/address".format(deviceId)
            HEADER = {'Accept': 'application/json',
                    'Authorization': 'Bearer {}'.format(consentToken)}
            response = requests.get(URL, headers=HEADER)
            
            if response.status_code == 200:
                response = response.json()
                userAddress = response['addressLine1']
                userAddress += ','.join(filter(None, (response['city'], response['stateOrRegion'])))
                userAddress = userAddress.replace(' ', '+')

            session_attributes = {}
            card_title = "device info"
            reprompt_text = ""
            should_end_session = True
        
            speech_output = userAddress
        
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
    else:
        session_attributes = {}
        card_title = "device info"
        reprompt_text = ""
        should_end_session = True
    
        #speech_output = "device id: " + deviceId + "consent token: " + consentToken
        speech_output = "device id: consent token "
    
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        """
        code
        """
        # userAddress = get_user_address(event['context']['system'])
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'],event['context'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
