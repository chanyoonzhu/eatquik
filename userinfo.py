import json
import requests

def get_user_address (context):

    userAddress = ''
    deviceId = ''
    consentToken = ''

    try:
        deviceId = context['System']['device']['deviceId'] 
        consentToken = context['System']['user']['permissions']['consentToken']
    except:
        deviceId = ''
        consentToken = ''
    
    if deviceId and consentToken:
    
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
    
    return userAddress
