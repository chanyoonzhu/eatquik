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
from fuzzymatching import match_fuzzy_string
from postmatesapi import get_delivery_info
from yelpcall import business_match_api
from yelpcall import transaction_api

"""
global variable for nearby restaurants
"""
# response = business_match_api("Los+Compadres+Taco+Truck", 'San Francisco', 'CA', 'US')
# print(response)

# response = transaction_api('401 W Brooks St, Norman, OK, US 73019')
# print(response)

# restaurants = get_restaurants_list('buger king', '303 Wadsack Dr, Norman', 0)
# print(restaurants)

# restaurant_namelist = []
# restaurant_infocus = None

# restaurants = get_restaurants_list('restaurant','401 W Brooks St, Norman, OK, US 73019', 49)
# for restaurant in restaurants:
#     restaurant_namelist.append(restaurant['name'])
#     print(restaurant['name'] + ' ')
# fuzzy_restaurant = "coriander cafe"
# result = match_fuzzy_string(fuzzy_restaurant, restaurant_namelist)
# print('result: ' + str(result) + 'fuzzy string: ' + str(fuzzy_restaurant))
# for restaurant in restaurants:
#     if restaurant['name'] == result:
#         restaurant_infocus = restaurant
# output_text = restaurant_infocus['name'] + ' . rating .' + str(restaurant_infocus['rating'])
# output_text = restaurant_infocus['phone']
# print (output_text)
# address='303 Wadsack Dr, Norman, OK'
# pickup_address = ''
# address_lines = restaurant_infocus['location']['display_address']
# for line in address_lines:
#     pickup_address += (line + ' ')
# response = get_delivery_info(pickup_address, address)
# delivery_time = response['duration']
# output_text = 'estimated delivery time is ' + str(delivery_time) + ' minutes'
# print(output_text)


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


# pickup_address = "1241 Alameda Street, Norman, OK 73071"
# dropoff_address = "303 Wadsack Dr, Norman, OK 73072"
# response = get_delivery_info(pickup_address, dropoff_address)
# delivery_time = response['duration'] + ' minutes'
# print(delivery_time)




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

    if intent_name == 'GetNearbyRestaurants' or intent_name == 'GetMoreRestaurants':

        address = get_user_address(context)
        output_text = ""

        if address:

            restaurants = get_restaurants_list('restaurant', address, 20)
            if intent_name == 'GetNearbyRestaurants':
                restaurants = restaurants[0:11]
            elif intent_name == 'GetMoreRestaurants':
                restaurants = restaurants[11:]
                
            if restaurants:
                
                formatted_text = ''
                
                for restaurant in restaurants:
                    output_text += restaurant['name'] + ' .' 
                    formatted_text += restaurant['name'] + "\n"

                if intent_name == 'GetNearbyRestaurants':
                    output_text += "To ask for more information for a restaurant, Say . tell me more about with the name of the restaurant" \
                            "Or you can ask for its phone number or address or if it is open. To hear more restaurant options, say . more restaurants. "
                elif intent_name == 'GetMoreRestaurants':
                    output_text += "To ask for more information for a restaurant, Say . tell me more about with the name of the restaurant" \
                            "Or you can ask for its phone number or address or if it is open. "

                card = {
                    "type": "Standard",
                    "title": "restaurants",
                    "text": formatted_text,
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

            else:
                # fallback response (restaurants not found)
                session_attributes = {}
                card_title = ''
                reprompt_text = ''
                should_end_session = True
                speech_output = 'Sorry. Eatquik cannot find any restaurants within 5 miles of where you are. '

                return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        
            
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

    elif intent_name == 'GetRestaurantInfo' or intent_name == 'GetRestaurantCategory' or \
        intent_name == 'GetRestaurantNumber' or \
        intent_name == 'GetRestaurantStatus' or \
        intent_name == 'GetRestaurantAddress' or \
        intent_name == 'GetDeliveryTime': 

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

            restaurants = get_restaurants_list('restaurant', address, 49)
                
            if restaurants:

                for item in restaurants:
                    restaurant_namelist.append(item['name'])

                # fuzzy matching with restaurant name list
                restaurant = match_fuzzy_string(fuzzy_restaurant, restaurant_namelist)

                if restaurant: 

                    for item in restaurants:
                        if item['name'] == restaurant:
                            restaurant_infocus = item

                    if intent_name == 'GetRestaurantInfo':
                        categories = restaurant_infocus['categories']
                        category_list = ''
                        for category in categories:
                            category_list += category['title'] + '. .'
                        output_text = (restaurant_infocus['name']  + ' . '
                                        + category_list
                                        + ' . rating . ' + str(restaurant_infocus['rating']) 
                                        + '. and is open now .' if (restaurant_infocus['is_closed'] == False) else '. and is closed now .')
                    elif intent_name == 'GetRestaurantCategory':
                        categories = restaurant_infocus['categories']
                        for category in categories:
                            output_text += category['title'] + '. .'
                    elif intent_name == 'GetRestaurantNumber':
                        output_text = 'The phone number for ' + restaurant_infocus['name'] + ' is '
                        phone_num = restaurant_infocus['phone']
                        phone_digits = list(phone_num)
                        phone_digits.pop(0) # get rid of + before country code
                        for digit in phone_digits:
                            output_text += (digit + ' ')
                    elif intent_name == 'GetRestaurantStatus':
                        output_text = restaurant_infocus['name']
                        output_text += '. is now open .' if (restaurant_infocus['is_closed'] == False) else '. is closed .'
                    elif intent_name == 'GetRestaurantAddress':
                        output_text = restaurant_infocus['name'] + " . is located at . "
                        address_lines = restaurant_infocus['location']['display_address']
                        for line in address_lines:
                            output_text += (line + " . ")
                    elif intent_name == 'GetDeliveryTime':
                        # code for postmates
                        pickup_address = ''
                        address_lines = restaurant_infocus['location']['display_address']
                        for line in address_lines:
                            pickup_address += (line + ' ')
                        response = get_delivery_info(pickup_address, address)
                        delivery_time = response['duration']
                        output_text = 'estimated delivery time is ' + str(delivery_time) + ' minutes according to postmate'

                    session_attributes = {}
                    card_title = "restaurant info: " #+ restaurant_infocus
                    reprompt_text = ""
                    should_end_session = False
                    speech_output = output_text
                
                    return build_response(session_attributes, build_speechlet_response(
                        card_title, speech_output, reprompt_text, should_end_session))

                else:
                    # no matching restaurant    
                    session_attributes = {}
                    card_title = ''
                    reprompt_text = ''
                    should_end_session = False
                    speech_output = 'Sorry. The restaurant you asked for is not in this area. '\
                                    'Please choose a restaurant from the list of nearby restaurants we provided and ask again. ' \
                                    'To listen to the list of restaurants nearby. Say. . what are the restaurants nearby. '

                    return build_response(session_attributes, build_speechlet_response(
                    card_title, speech_output, reprompt_text, should_end_session))

            else:
                # fallback response (list of restaurants not found)
                session_attributes = {}
                card_title = ''
                reprompt_text = ''
                should_end_session = True
                speech_output = 'Sorry. The restaurant you asked for is not in this area. '\
                                'Please choose a restaurant from the list of nearby restaurants we provided and ask again. ' \
                                'To listen to the list of restaurants nearby. Say. . what are the restaurants nearby. '

                return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        
            
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

    elif intent_name == 'EndSession':
        session_attributes = {}
        card_title = 'Good Bye!'
        reprompt_text = ''
        should_end_session = True
        speech_output = 'Good bye!'

        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
    handle_session_end_request()


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

