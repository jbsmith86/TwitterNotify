import requests
import urllib
import urllib2
import json
from requests_oauthlib import OAuth1
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

SENDHUB_API_KEY = ""
SENDHUB_USERNAME = ""
SENDHUB_CONTACT = ""

OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""
OAUTH_CONSUMER_KEY = ""
OAUTH_CONSUMER_SECRET = ""

def get_oauth():
    oauth = OAuth1(OAUTH_CONSUMER_KEY,
                client_secret=OAUTH_CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def sendtextmsg(msg):
	request = urllib2.build_opener()
	returnedpage = request.open('https://api.sendhub.com/v1/contacts/?username=' + SENDHUB_USERNAME + '&api_key=' + SENDHUB_API_KEY).read()
	contactid = str(json.loads(returnedpage)['objects'][0]['id'])
	jsonmsg = json.dumps({ 'contacts' : contactid, 'text' : msg })
	responsecode = requests.post('https://api.sendhub.com/v1/messages/', params={'api_key': SENDHUB_API_KEY, 'username': SENDHUB_USERNAME}, data=json.dumps({'contacts': [SENDHUB_CONTACT],'text': msg}), headers={'content-type': 'application/json'})


oauth = get_oauth()
url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
jsontimeline = requests.get(url, auth=oauth).json()
