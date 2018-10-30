from __future__ import print_function
import base64
import json
import requests
import sys

# Workaround to support both python 2 & 3
try:
    import urllib.request, urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse


# client keys
CLIENT = json.load(open('conf.json', 'r+'))
CLIENT_ID = CLIENT['songkick_id']

# search_for_artist
def get_artist_info(name):
    artist_name = name.replace("&", "")
    artist_name = artist_name.replace("#", "")
    artist_name = artist_name.replace("?", "")
    artist_name = artist_name.replace("/", "")
    url = "https://api.songkick.com/api/3.0/search/artists.json?apikey={apikey}&query={query}".format(apikey=CLIENT_ID, query=artist_name)
    resp = requests.get(url)
    result = resp.json()
    if result['resultsPage']['results']['artist'][0]['displayName'] == name:
        return result['resultsPage']['results']['artist'][0]['onTourUntil']
    return "null"

# search for concerts of artist
def get_artist_concerts(artist_id):
    url="https://api.songkick.com/api/3.0/artists/{id}/calendar.json?reason=tracked_artist&apikey={apikey}".format(id=artist_id, apikey=CLIENT_ID)
    resp = requests.get(url)
    return resp.json()