import json
import requests
from yelpcall import query_api
from responsehandler import handle_response

def get_restaurants_list (address):
      
    """
    restaurant info
    """
    response = query_api('restaurant', address)
    restaurants = handle_response(response)
        
    if restaurants:
        return restaurants
    else:
        return None
