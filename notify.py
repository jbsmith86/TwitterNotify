from __future__ import unicode_literals
import requests
import urllib
import urllib2
import json
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1
from urlparse import parse_qs

SENDHUB_API_KEY = ""
SENDHUB_USERNAME = ""
SENDHUB_CONTACT = ""

OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""
OAUTH_CONSUMER_KEY = ""
OAUTH_CONSUMER_SECRET = ""

def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]
    
    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url
    
    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret

def get_oauth():
    oauth = OAuth1(OAUTH_CONSUMER_KEY,
                client_secret=OAUTH_CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def setup_list(filepath):
		newfile = open(filepath, 'U')
		wordlist = newfile.read().splitlines()
		return [i.lower() for i in wordlist]


def send_text_msg(msg):
	request = urllib2.build_opener()
	returnedpage = request.open('https://api.sendhub.com/v1/contacts/?username=' + SENDHUB_USERNAME + '&api_key=' + SENDHUB_API_KEY).read()
	contactid = str(json.loads(returnedpage)['objects'][0]['id'])
	jsonmsg = json.dumps({ 'contacts' : contactid, 'text' : msg })
	responsecode = requests.post('https://api.sendhub.com/v1/messages/', params={'api_key': SENDHUB_API_KEY, 'username': SENDHUB_USERNAME}, data=json.dumps({'contacts': [SENDHUB_CONTACT],'text': msg}), headers={'content-type': 'application/json'})

if  __name__ =='__main__':
	oauth = get_oauth()
	url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
	jsontimeline = requests.get(url, auth=oauth).json()
	alertwords = setup_list('words.list')
	for tweet in jsontimeline:
		try:
			for word in alertwords:
				if word in tweet.lower():
					send_text_msg(tweet['user']['screen_name'].encode('utf-8') + " - " + tweet['text'].encode('utf-8'))
		except:
			pass