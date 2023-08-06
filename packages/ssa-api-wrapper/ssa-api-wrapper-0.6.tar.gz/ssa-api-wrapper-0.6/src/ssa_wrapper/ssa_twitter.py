import requests
import json

def latesttweet():
    url = 'https://phoneguyapi.herokuapp.com/ssa/latesttweet'
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data
