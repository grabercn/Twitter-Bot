from asyncio.windows_events import INFINITE
from logging import error
import tweepy
import pyjokes
from credentials import consumer_key, consumer_secret, access_token, access_token_secret
from prompts import wait, prompted, Repeat
import time
from termcolor import colored

# =============== Twitter API =================

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
try:
  api = tweepy.API(auth)
  text = colored('- API OK -', 'green', attrs=[])
  print(text)
except:
  print(colored("- Error - \nAPI connection issue", "red", attrs=[]))

# Create a tweet 
def genTweet():
  try:
    My_joke = pyjokes.get_joke(language="en", category="all")
  except:
    print(colored("- Error - \nError finding joke", "red", attrs=[]))
    my_joke = "error"
  return My_joke


# =================== Main ===================

if Repeat == 0:
  Repeat = INFINITE

for i in range(Repeat):
    
    tweeted = genTweet() # generate a new tweet status
    
    try: 
      api.update_status(status = tweeted) # Create a tweet
    except:
      print(colored("- Error - \nError posting Tweet", "red", attrs=[]))
    
    
    twe = colored('- Tweeted - \n', 'cyan', attrs=[])
    print (twe + "--> " + str(tweeted))
   
   
    time.sleep(wait) # wait for the next tweet
