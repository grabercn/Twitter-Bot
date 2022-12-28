# Twitter Bot Main - Main File containing all functions and main loop
# - Author: @chrismslist
# - Date: 10/22/2022
# - Version: 0.5 beta
# - To do: fix sentence structure, add more jokes, add more quotes, add more tweets, add more features
# + implement blacklist 

# issues:
# fix multi commenting on same run
# improve error handeling
# fix follow random not being random
# already favorite tweet error
# duplicate tweet post error

# =============== Imports =================
from array import array
from datetime import datetime
from random import randint, random
from termcolor import colored # pre import colored

text = colored('-Program Intializing-', 'blue', attrs=['reverse', 'blink'])
print(text)


from asyncio.windows_events import INFINITE
from ctypes import ArgumentError
from email.mime import image
from logging import error
from queue import Empty
from tkinter import PhotoImage
import tweepy
import pyjokes
from credentials import consumer_key, consumer_secret, access_token, access_token_secret, user_id, nasa_api
import time
from termcolor import colored
from tqdm import tqdm
import os
from os import sys

# =============== Imports End =================

# =============== Init Chat Bot Vars =================
global chatbot
#global trainer

# =============== Helper Functions ===============
def curTime(): # get current time and return it (str)
  now = datetime.now()
  return now.strftime("%H:%M:%S")

def initChatBot():
  from chatgpt_wrapper import ChatGPT

  global chatbot
  
  chatbot = ChatGPT()
  
  """
  global chatbot
  global trainer
  
  from chatterbot import ChatBot
  from chatterbot.trainers import ChatterBotCorpusTrainer

  chatbot = ChatBot('Ron Obvious')

  # Create a new trainer for the chatbot
  trainer = ChatterBotCorpusTrainer(chatbot)

  # Train the chatbot based on the english corpus
  trainer.train("chatterbot.corpus.english")
  """

def getChatBotResponse(question):
  global chatbot
  
  try:
    chatbot
  except NameError:
    print("Chatbot not initialized, initializing now...\nThis May Take A While... \n")
    initChatBot()
    
  return str(chatbot.ask(question))
  
  """
  try:
    chatbot
  except NameError: 
    print("Chatbot not initialized, initializing now...\nThis May Take A While... \n")
    initChatBot()
    initChatBot()
  return str(chatbot.get_response(question))
  """

def getPromptedParam(prompted): # get prompted param and return it (str)
  try:
    return prompted.split(" ")[1]
  except IndexError:
    print(colored("- Error - \nInvalid Prompt", "red", attrs=[]))
    return "Error"
  
def range_with_status(total): # range with status for prog bar
    """ iterate from 0 to total and show progress in console """
    n=0
    while n<total:
        done = '#'*(n+1)
        todo = '-'*(total-n-1)
        s = '<{0}>'.format(done+todo)
        if not todo:
            s+='\n'        
        if n>0:
            s = '\r'+s
        print(s, end='')
        yield n
        n+=1
        
def waitDef(wait): # set wait time depending on input and return (int)
  try:
    wait = int(wait)
  except TypeError:
    print("wait time is string")
    time = getPromptedParam(wait)
    wait = wait.split(" ")[0]
    
    if wait == "Error":
      return 0
    elif wait == "hours":
      return int(time) * 3600
    elif wait == "minutes":
      return int(time) * 60
    elif wait == "seconds":
      return int(time)
    elif wait == "days":
      return int(time) * 86400
    else:
      return int(time)
  
  return wait*60


def twitterRates():
    stats = api.rate_limit_status()  #stats['resources'].keys()
    for akey in stats['resources'].keys():
        if type(stats['resources'][akey]) == dict:
            for anotherkey in stats['resources'][akey].keys():
                if type(stats['resources'][akey][anotherkey]) == dict:
                    #print(akey, anotherkey, stats['resources'][akey][anotherkey])
                    limit = (stats['resources'][akey][anotherkey]['limit'])
                    remaining = (stats['resources'][akey][anotherkey]['remaining'])
                    used = limit - remaining
                    if used != 0:
                        print("Twitter API used", used, ": Remaining queries", remaining,"for query type", anotherkey)
                    else:
                        pass
                else:
                    pass  #print("Passing")  #stats['resources'][akey]
        else:
            print(akey, stats['resources'][akey])
            print(stats['resources'][akey].keys())
            limit = (stats['resources'][akey]['limit'])
            remaining = (stats['resources'][akey]['remaining'])
            used = limit - remaining
            if used != 0:
                print("Twitter API:", used, "requests used,", remaining, "remaining, for API queries to", akey)
                pass
  

# =============== Helper Functions End ===============


# =============== Prompt Function ===============

def Prompts():
  
  global prompted
  global Repeat
  global wait
  global Error
  
  text = colored('-Program Started-', 'green', attrs=['reverse', 'blink'])
  print(text) # print prog started text

  while True:
    try:
        do = input("What would you like to do? ")
    except:
        print("Error: "+str(do))
        break
    
    
    if do == "tweet":
        try:
            wait = str(input("Time (m) between tweets: "))
            wait = waitDef(wait)
        except Exception as e:
            print(colored("- Error - \n"+str(e), "red", attrs=[]))
            wait = 1

        try:
            prompted = str(input("Prompt (joke, quote): "))
        except:
            print(colored("- Error - \nInvalid Prompt", "red", attrs=[]))
            prompted = "joke"
            

        try:
            Repeat = int(input("Repeat: "))
        except:
            print(colored("- Error - \nInvalid Repeat", "red", attrs=[]))
            Repeat = 1
        break
    
    elif do == "api":
        Twitter()
    
    elif do == "limits":
      twitterRates()
    
    elif do == "error":
      if (Error != ""):
        print(colored("- Error at "+curTime()+" - \n"+str(Error), "red", attrs=[]))
        Error = ""
      else:
        print("--> No recent errors")
    
    elif "tweet" in do:
        wait = int(do.split(" ")[1])
        prompted = str(do.split(" ")[2])
        Repeat = int(do.split(" ")[3])
        wait = wait * 60
        break
    
    elif do == "auto":
      auto()
      
    elif do == "exit":
        exit()
    
  main()
  print("- ok - \n")
  Prompts()

# =============== Prompt Function End ===============


# =============== Twitter API =================
def Twitter():
  global Error
  global api
  
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  # Create API object
  try:
    api = tweepy.API(auth, wait_on_rate_limit=True)
    api.verify_credentials()
    text = colored('- API OK -', 'green', attrs=[])
    print(text)
  except Exception as e:
    Error = e
    print(colored("- Error - \nAPI Connection Issue: type 'error' for details", "red", attrs=[]))

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
    
    file_path_type = [getPromptedParam(prompted)]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    
    return random_image, file_path_type
  
  elif prompted == "sentence": # Generate a tweet sentence random
    import random
    from random import randint

    gvn_names=["John","Grace","Freddy Fazbear","Donald J Trump","Barack Obama","Joey Spats","Seyour64","Andrew NoVatsney","John McAffee","Joseph","Dan","Dan Beard","Dan Bread",
               "Danny","Pickachu","Charizard","Elon Musk","Jeff Bezos"]
    gvn_verbs=["had fun"]
    gvn_nouns=["writing"]

    na1 =(random.choice(gvn_names))
    na2 = (random.choice(gvn_names))
    ve1 =(random.choice(gvn_verbs))
    ve2 = (random.choice(gvn_verbs))
    no1 =(random.choice(gvn_nouns))
    no2 = (random.choice(gvn_nouns))

    rand = randint(1, 1)
    if rand == 1:
      return (str(na1+" "+ve1+" "+no1+".")), Empty
    
  elif prompted == "name": # Generate a tweet using name generator
      import names
      return str(names.get_full_name()), Empty
  
  elif prompted == "chatbot":
    import random
    
    bot_choices = ["tell me a short joke", "give me a short quote", "tell me a interesting but short fact"]
    a = random.choice(bot_choices)
    
    return getChatBotResponse(a), Empty
    
      

# =================== Main ===================

def main():
  
  global api
  global Error
  global Repeat
  global wait
  global prompted
  
  if Repeat == 0:
    Repeat = INFINITE

  for i in range(Repeat):
      
      tweeted, tweeted2 = genTweet() # generate a new tweet status
      
      if type(tweeted) != str:
        api.update_status_with_media(filename=tweeted2, file=tweeted,status="Status") # Create a tweet with media
      
      try: 
        api.update_status(status = tweeted) # Create a tweet
      except Exception as e:
        print(colored("- Error - \nError posting Tweet "+str(i+1)+"/"+str(Repeat), "red", attrs=[]))
        Error = e
      
      
      twe = colored('- Tweeted '+str(i+1)+"/"+str(Repeat)+" -\n", 'cyan', attrs=[])
      print (twe + "--> " + str(tweeted))
    
    
      for i in tqdm(range(int(wait))):
        time.sleep(1)
  
  prompted = ""
  return
  
def auto():
  
  import random
  
  global prompted
  global wait
  global api
  global Error
  global Repeat
  
  actions = []
  lastAction = []

  # Run the program repeatedly - loop start
  while True:
    
    choice = 6 #randint(1,8)
    print("Action:"+str(choice))
    
    if choice == 1: # decide randomly on what to tweet then tweet it
      prompt = 5 #randint(1,4)
      if prompt == 1:
        prompted = "joke"
      elif prompt == 2:
        prompted = "quote"
      elif prompt == 3:
        prompted = "sentence"
      elif prompt == 4:
        prompted = "name"
      elif prompt == 5:
        prompted = "chatbot"
        
      #actions.append("Tweeted a random "+prompted)
      
      Repeat = 1
      wait = 0
      main()
      
    if choice == 2: # follow back people who follow you
      for follower in tweepy.Cursor(api.get_followers).items():
        if not follower.following:
            actions.append(f"Followed {follower.name} back")
            follower.follow()
            
    if choice == 3: # respond to mentions
      actions.append("Retrieving mentions")
    for tweet in tweepy.Cursor(api.mentions_timeline, tweet_mode="extended").items():
        if not tweet.favorited:
            actions.append(f"Favoriting {tweet.id} - {tweet.full_text}")
            tweet.favorite()
        if not tweet.user.following and tweet.user.screen_name != "FoodNetworke":
            actions.append(f"Following {tweet.user.name}")
            tweet.user.follow()
        if not tweet.in_reply_to_status_id:
            actions.append(f"Answering {tweet.id} - {tweet.text}")
            api.update_status(
                status = f"@{tweet.user.screen_name} Thanks for the mention!",
                in_reply_to_status_id = tweet.id,
            )
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in ["joke", "jokes"]):
            actions.append((f"Answering to {tweet.user.name}"))

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status="@" + tweet.user.screen_name + " " + choice(["love you","johhny appleseed could do better"]),
                in_reply_to_status_id=tweet.id,
            )
            
    if choice == 4: # retweet tweets from timeline
      
      for tweet in (tweepy.Cursor(api.home_timeline).items(randint(1,5))):
        try:
          tweet.retweet()
          actions.append(f"Retweeted {tweet.text} from timeline")
        except:
          pass
          
    if choice == 5: # like tweets from timeline
      for tweet in (tweepy.Cursor(api.home_timeline).items(randint(1,5))):
        if not tweet.favorited:
          tweet.favorite()
          actions.append(f"Liked {tweet.text} from timeline")
        else:
          pass
          
          
    if choice == 6: # comment on tweets from timeline
       for tweet in (tweepy.Cursor(api.home_timeline).items(randint(1,5))):
         if not tweet.in_reply_to_status_id:
            #prompted = "sentence"
            
            tweetText = getChatBotResponse(tweet.text)
            
            api.update_status(
                status = f"@{tweet.user.screen_name} {tweetText}",
                in_reply_to_status_id = tweet.id,
            )
            actions.append(f"Commented on {tweet.text} from timeline")
            break
    
    if choice ==7 : # follow random people
      tweets = list(tweepy.Cursor(api.search_users, q="a", tweet_mode='extended').items(randint(1,100)))
      random.shuffle(tweets)
      for tweet in tweets:
        try:
          tweet.follow()
          actions.append(f"Followed {tweet.name} randomly")
          break
        except:
          pass
    
    if choice == 8: # dm followers
      prompted = "joke"
      for follower in tweepy.Cursor(api.get_followers).items():
        if follower.following:
            send = randint(1,3)
            if send == 1:
              actions.append(f"DM'd {follower.name} (follower) randomly")
              api.send_direct_message(recipient_id = follower.id, text = str(genTweet()[0]))
              break
    
    """
    if choice == 9: # dm random people
      prompted = "joke"
      tweets = list(tweepy.Cursor(api.search_users, q="a", tweet_mode='extended').items(randint(1,20)))
      random.shuffle(tweets)
      for tweet in tweets:
        try:
          actions.append(f"DM'd {tweet.name} randomly")
          api.send_direct_message(recipient_id = tweet.id, text = str(genTweet()[0]))
          break
        except:
          pass
      """
      

    try:
      if lastAction != actions[len(actions)-1]:
        print(colored("Latest Action:"+str(actions[len(actions)-1]), 'green'))
      else:
        print(colored("Latest Action: No New Actions", 'yellow'))
      lastAction = actions[len(actions)-1]
    except IndexError:
      print(colored("No actions yet", 'yellow'))
      
    # save actions to a file and wait for a random amount of time  
    try:
      fullpath = os.path.join(os.path.dirname(sys.argv[0]), 'autoLog.txt')
      list_file = open(fullpath, "a")
      
      inc = 0
      for action in actions:
        inc = inc + 1
        if inc == 1:
          list_file.write("#################### New Session ("+curTime()+") #################### \n")
        list_file.write((str(inc))+". "+action+" ("+curTime()+") \n")
      list_file.close() 
    except UnicodeEncodeError:
      print(colored("File write error (most likely invalid unicode char)","red"))
    
      
    sleep = randint(1,200)
    
    for i in tqdm(range(int(sleep))):
        time.sleep(1)
    
            

  

wait = 0 # init global wait var
prompted = "" # init global prompt var
Repeat = 0 # init global repeat var
Error = "" # init global error var
api = "" # init global api var

Twitter() # call twitter API
Prompts() # call prompts function to start program
