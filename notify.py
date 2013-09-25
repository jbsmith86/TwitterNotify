from __future__ import unicode_literals
import requests
import urllib
import urllib2
import json
import time
from requests_oauthlib import OAuth1
from urlparse import parse_qs

#Sendhub info
SENDHUB_API_KEY = ""
SENDHUB_USERNAME = ""
SENDHUB_CONTACT = ""

#Twitter/Oauth keys
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""
OAUTH_CONSUMER_KEY = ""
OAUTH_CONSUMER_SECRET = ""

#filepath constants
WORDLIST_FILEPATH = "words.list"
LASTID_FILEPATH = "lastid.txt"
EXCLUDE_USERLIST_FILEPATH = "exclude.txt"

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

def get_list(filepath):
    newfile = open(filepath, 'U')
    wordlist = newfile.read().splitlines()
    return [i.lower() for i in wordlist]

def get_lastid(filepath):
    idfile = open(filepath, 'r')
    lastid = idfile.read()
    idfile.close()
    return long(lastid)

def save_lastid(lastid, filepath):
    idfile = open(filepath, 'w')
    idfile.write(str(lastid) + '\n')
    idfile.close()

def get_tweets_since(lastid):
    oauth = get_oauth()
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    params = {'since_id' : lastid}
    return requests.get(url, auth=oauth, params=params).json()

def get_inital_tweets():
    oauth = get_oauth()
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    return requests.get(url, auth=oauth).json()

def send_text_msg(msg):
    request = urllib2.build_opener()
    returnedpage = request.open('https://api.sendhub.com/v1/contacts/?username=' + SENDHUB_USERNAME + '&api_key=' + SENDHUB_API_KEY).read()
    contactid = str(json.loads(returnedpage)['objects'][0]['id'])
    jsonmsg = json.dumps({ 'contacts' : contactid, 'text' : msg })
    responsecode = requests.post('https://api.sendhub.com/v1/messages/', params={'api_key': SENDHUB_API_KEY, 'username': SENDHUB_USERNAME}, data=json.dumps({'contacts': [SENDHUB_CONTACT],'text': msg}), headers={'content-type': 'application/json'})

if  __name__ =='__main__':

    try:
        jsontimeline = get_tweets_since(get_lastid(LASTID_FILEPATH))
    except IOError:
        jsontimeline = get_inital_tweets()

    alertwords = get_list(WORDLIST_FILEPATH)
    excludedusers = get_list(EXCLUDE_USERLIST_FILEPATH)

    while(True):
        
        for tweet in jsontimeline:
            try:
                for word in alertwords:
                    if word.lower() in tweet['text'].encode('utf-8').lower():
                        if tweet['user']['screen_name'].encode('utf-8') not in alertwords:
                            send_text_msg(tweet['user']['screen_name'].encode('utf-8') + " - " + tweet['text'].encode('utf-8'))
            except:
                pass
        try:
            save_lastid(jsontimeline[0]['id'], LASTID_FILEPATH)
        except IndexError:
            pass
        time.sleep(90)
        jsontimeline = get_tweets_since(get_lastid(LASTID_FILEPATH))