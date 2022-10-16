from asyncio.windows_events import INFINITE
from ctypes import ArgumentError
from email.mime import image
from logging import error
from queue import Empty
from tkinter import PhotoImage
import tweepy
import pyjokes
from credentials import consumer_key, consumer_secret, access_token, access_token_secret, user_id, nasa_api
from prompts import wait, prompted, Repeat
import time
from termcolor import colored

# =============== Helper Functions ===============
def getPromptedParam():
  try:
    return prompted.split(" ")[1]
  except IndexError:
    print(colored("- Error - \nInvalid Prompt", "red", attrs=[]))
    return "Error"
     
      
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
  if prompted == "joke": # Generate a tweet using py jokes
    try:
      My_joke = pyjokes.get_joke(language="en", category="all")
    except:
      print(colored("- Error - \nError finding joke", "red", attrs=[]))
      my_joke = "error"
    return My_joke, Empty
  
  elif prompted == "quote": # Generate a tweet using tweet generator
    #try:
    from tweet_generator import tweet_generator
    twitter_bot = tweet_generator.PersonTweeter(user_id,consumer_key,consumer_secret,access_token,access_token_secret)
    random_tweet = twitter_bot.generate_random_tweet()
    #except:
      #print(colored("- Error - \nError finding quote", "red", attrs=[]))
      #random_tweet = "error: "+str(time.time())
    return random_tweet, Empty
  
  elif prompted == "nasa": # Generate a tweet using nasa api
    from nasaapi import Client
      
    nasa = Client(nasa_api)
    
    return nasa.nivl.search("earth")
  
  
  
  elif prompted == "folder": # Generate a tweet using dalle api
    import glob, random
    
    file_path_type = [getPromptedParam()]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    
    return random_image, file_path_type
  
  elif prompted == "sentence":
    import random

    gvn_names=["Me", "I", "you", "He", "She", "They", "We","Lukas","Seyour64","Andrew"]
    gvn_verbs=["was","is","tried","had fun","did not have fun","enjoyed","fucked"]
    gvn_nouns=["eating.", "writing", "watching a movie", "reading.", "sleeping.", "dancing.","beating.","breaking.","fucking.","sliding.","cumming."]

    p =(random.choice(gvn_names))
    q =(random.choice(gvn_verbs))
    r =(random.choice(gvn_nouns))

    return (str(p+" "+q+" "+r)), Empty


# =================== Main ===================

if Repeat == 0:
  Repeat = INFINITE

for i in range(Repeat):
    
    tweeted, tweeted2 = genTweet() # generate a new tweet status
    
    if type(tweeted) != str:
      api.update_status_with_media(filename=tweeted2, file=tweeted,status="Status") # Create a tweet with media
    
    try: 
      api.update_status(status = tweeted) # Create a tweet
    except:
      print(colored("- Error - \nError posting Tweet", "red", attrs=[]))
    
    
    twe = colored('- Tweeted - \n', 'cyan', attrs=[])
    print (twe + "--> " + str(tweeted))
   
   
    time.sleep(wait) # wait for the next tweet
