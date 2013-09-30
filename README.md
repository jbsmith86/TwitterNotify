TwitterNotify
=============

App that sends you texts of tweets you are interested in or need to see

##Requirements  

This app requires a Twitter account - www.twitter.com  
A free account from sendhub to send txt notifications is also required - www.sendhub.com

##Installation

You must have python 2.7 and pip installed.  
python - http://www.python.org/download/releases/2.7.5/  
pip - https://pypi.python.org/pypi/pip  
  
Use pip to install the following libraries:
```bash
pip install requests
pip install requests_oauthlib
```

Create a text file with a list of words you would like to track and rename or "words.list" or change the WORDLIST_FILEPATH constant to your filename

Optionally you can add a text file named "exclude.txt" with Twitter usernames you would like to exclude from tracking
