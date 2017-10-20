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
import pprint
from userinfo import get_user_address
from restaurantslist import get_restaurants_list
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

"""
global variable for nearby restaurants
"""
# restaurants_obj = None
# restaurant_namelist = []
# restaurant_infocus = None

# response = query_api('restaurant', '303 Wadsack Dr, Norman, Oklahoma')
# restaurants = handle_response(response)
# restaurants_obj = restaurants
# for restaurant in restaurants:
#     restaurant_namelist.append(restaurant['name'])
# result = process.extractOne("John John Milk Tea", restaurant_namelist)[0]
# for restaurant in restaurants_obj:
#     if restaurant['name'] == result:
#         restaurant_infocus = restaurant
# output_text = restaurant_infocus['name'] + ' . rating .' + str(restaurant_infocus['rating'])
# print (output_text)

# restaurants = get_restaurants_list('401 W Brooks St, Norman, OK, US 73019')
# for restaurant in restaurants:
#     print(restaurant['name'] + '\n')


# card = {
#     "type": "Standard",
#     "title": "restaurants",
#     "text": restaurants[0]['name'] + "\n",
#     "image": {
#         "smallImageUrl": "http://s3-media2.fl.yelpcdn.com/bphoto/MmgtASP3l_t4tPCL1iAsCg/o.jpg",
#         "largeImageUrl": "http://s3-media2.fl.yelpcdn.com/bphoto/MmgtASP3l_t4tPCL1iAsCg/o.jpg"
#     }
# }

# obj = build_card_response(card, "haha", " ", True)
# print(obj['outputSpeech']['text'])

# postmates_key = "ZWZmY2RhOTItZWNjMy00ZGI2LWI5NTQtZjhkOTE0ZTA5NGQ5Og=="
# customer_id = "cus_Kf3bMZuhfEUbQV"
# pickup_address = "2363 Van Ness Ave, San Francisco, CA"
# dropoff_address = "690 5th St, San Francisco, CA"
# url_params = {
#     "pickup_address": pickup_address.replace(' ', '+'),
#     "dropoff_address": dropoff_address.replace(' ', '+')
# }
# url =  "https://api.postmates.com/v1/customers/{}/delivery_quotes".format(customer_id)
# headers = {'Accept': 'application/json',
#         'Authorization': 'Basic {}'.format(postmates_key)}
# response = requests.post(url, data = url_params, headers=headers)
# print(response.json())


# --------------- Helpers that build all of the responses ----------------------
#url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&type=restaurant&keyword=cruise&key=AIzaSyBOimD8S4Ifw8o1XBEEFO7YKylK9d0sSJk'
#r = requests.get(url)

def build_ask_permission_response(title, output, reprompt_text, should_end_session):
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

def build_card_response(card, output, reprompt_text, should_end_session):
    response = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    response['card'] = card

    return response

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
       'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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
    return build_response(session_attributes, build_ask_permission_response(
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

        address = get_user_address(context)
        output_text = ""

        if address:

            restaurants = get_restaurants_list(address)
                
            if restaurants:

                for restaurant in restaurants:
                    output_text += restaurant['name'] + ' .'

                """
                todo - after testing, delete next line and use commented line right above
                """
                # output_text = restaurants[0]['name']  

                card = {
                    "type": "Standard",
                    "title": "restaurants",
                    "text": "\n",
                    "image": {
                        "smallImageUrl": "https://s3-media2.fl.yelpcdn.com/bphoto/MmgtASP3l_t4tPCL1iAsCg/o.jpg",
                        "largeImageUrl": "https://s3-media2.fl.yelpcdn.com/bphoto/MmgtASP3l_t4tPCL1iAsCg/o.jpg"
                    }
                }

                session_attributes = {}
                reprompt_text = ""
                should_end_session = False
                speech_output = output_text

                return build_response(session_attributes, build_card_response(card, speech_output, reprompt_text, should_end_session))

            #else:
                # fallback response (restaurants not found)
        
            
        else:
            # user permission not granted, send out prompt message and a new permission card
            session_attributes = {}
            card_title = ''
            reprompt_text = ''
            should_end_session = True
            speech_output = 'eatquick cannot function without address information. '\
            'To permit access to address information, enable eatquick again, and consent to provide address information in the Alexa app.'

            return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

    elif intent_name == 'GetRestaurantInfo':
        # string from Alexa literal string
        fuzzy_restaurant = intent['slots']['restaurant']['value']
        # stores nearby restaurants
        restaurant_namelist = []
        # stores restaurant user asks for
        restaurant_infocus = None
        output_text = ""

        """
        get restaurants
        """
        address = get_user_address(context)

        if address:

            restaurants = get_restaurants_list(address)
                
            if restaurants:

                # initialize restaurant name list
                for item in restaurants:
                    restaurant_namelist.append(item['name'])

                # fuzzy matching with restaurant name list
                restaurant = process.extractOne(fuzzy_restaurant, restaurant_namelist)[0]
                for item in restaurants:
                    if item['name'] == restaurant:
                        restaurant_infocus = item
                output_text = restaurant_infocus['name'] + ' . rating .' + str(restaurant_infocus['rating']) #+ restaurant_infocus['is_closed'] == False

                session_attributes = {}
                card_title = "restaurant info: " #+ restaurant_infocus
                reprompt_text = ""
                should_end_session = False
                speech_output = output_text
            
                return build_response(session_attributes, build_speechlet_response(
                    card_title, speech_output, reprompt_text, should_end_session))
                

            #else:
                # fallback response (restaurants not found)
        
            
        else:
            # user permission not granted, send out prompt message and a new permission card
            session_attributes = {}
            card_title = ''
            reprompt_text = ''
            should_end_session = True
            speech_output = 'eatquick cannot function without address information. '\
            'To permit access to address information, enable eatquick again, and consent to provide address information in the Alexa app.'

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

