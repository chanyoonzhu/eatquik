import json
import requests
from yelpcall import query_api
from yelpcall import query_match_api
from responsehandler import handle_response

def get_restaurants_list (term, address, limit):
      
    """
    restaurant info
    """
    if term == 'restaurant':
        response = query_api(term, address, limit)
    else:
        response = query_match_api(term, address)
    restaurants = handle_response(response)
        
    if restaurants:
        return restaurants
    else:
        return None
