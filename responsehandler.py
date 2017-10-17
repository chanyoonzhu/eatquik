import json

def handle_response (response):
    
    businesses = response['businesses']
    # select restaurants
    restaurants = select_restaurants (businesses)
    return restaurants

def select_restaurants (raw_data):
    # add selecting rules
    return raw_data