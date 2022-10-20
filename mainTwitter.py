from datetime import datetime
from termcolor import colored # pre import colored
# Notify prog run via main file
text = colored('-Program Intializing-', 'blue', attrs=['reverse', 'blink'])
print(text)

# imports ---------------------------------
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
# imports end -------------------------------

# =============== Helper Functions ===============
def curTime():
  now = datetime.now()
  return now.strftime("%H:%M:%S")
  

def getPromptedParam():
  try:
    return prompted.split(" ")[1]
  except IndexError:
    print(colored("- Error - \nInvalid Prompt", "red", attrs=[]))
    return "Error"
  
def range_with_status(total):
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

# =============== Helper Functions End ===============


# =============== Prompt Function ===============

def Prompts():
  
  global prompted
  global Repeat
  global wait
  global Error
  
  print(text)

  while True:
    try:
        do = input("What would you like to do? ")
    except:
        print("Error: "+str(do))
        break
    
    
    if do == "tweet":
        try:
            wait = int(input("Time (m) between tweets: "))
            wait = wait * 60
        except:
            print(colored("- Error - \nInvalid Time", "red", attrs=[]))
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
    api = tweepy.API(auth)
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
    
    file_path_type = [getPromptedParam()]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    
    return random_image, file_path_type
  
  elif prompted == "sentence": # Generate a tweet sentence random
    import random
    from random import randint

    gvn_names=["John","Grace","Freddy Fazbear","Donald J Trump","Barack Obama","Joey Spats","Seyour64","Andrew NoVatsney","John McAffee","Joseph","Dan","Dan Beard","Dan Bread"]
    gvn_verbs=["tried","had fun","did not have fun","enjoyed","fucked","thoroughly enjoyed","was ecstatic","tried to jump",
               "eventually ended up","loved","was eloped when","got wet","got eaten when trying","'s first time","has never",
               "sometimes like/s to take nice walks. On these walks, sometimes there are a bunch of weird people in suits",
               "smacked,","licked","hugged","smothered","got saucy","meated","creamed","melted"]
    gvn_nouns=["eating", "writing", "watching a movie", "reading", "sleeping", "dancing","beating","breaking","fucking","sliding","cumming","dating"]

    na1 =(random.choice(gvn_names))
    na2 = (random.choice(gvn_names))
    ve1 =(random.choice(gvn_verbs))
    ve2 = (random.choice(gvn_verbs))
    no1 =(random.choice(gvn_nouns))
    no2 = (random.choice(gvn_nouns))

    rand = randint(1,10)
    if rand == 1:
      return (str(na1+" "+ve1+" "+no1+".")), Empty
    if rand == 2:
      return (str(na1+" "+ve1+" "+no1+" while "+na2+" was "+no2+".")), Empty
    if rand == 3:
      return (str(na1+" and "+na2+" "+ve1+" "+no1+" while "+no2+".")), Empty
    if rand == 4:
      return (str(na1+" + "+na2+" were "+no1+" together while "+no2+".")), Empty
    if rand == 5:
      return (str(no1+" while "+na1+" is "+no2+" is "+random.choice(["hard.","sad.","frustrating.","cute.","lovely.","despicable.","sickening.","hot.","sexy."]))), Empty
    if rand == 6:
      return (str("Remember when "+na1+" and "+na2+" were "+no1+"?")), Empty
    if rand == 7:
      return (str("Have you ever tried "+no1+" while "+no2+"?")), Empty
    if rand == 8:
      return (str("Image if "+na1+" and "+na2+" hated each other.")), Empty
    if rand == 9:
      return (str("Does "+na1+" know that "+na2+" and me "+na2+" are lovers?")), Empty
    if rand == 10:
      return (str("Sometimes the best times are when me and "+na1+" "+random.choice(["hold hands","fuck","cry","enjoy life","destroy a box of cerial","get wet"])+".")), Empty
      




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
        print(colored("- Error - \nError posting Tweet "+str(i)+"/"+str(Repeat), "red", attrs=[]))
        Error = e
      
      
      twe = colored('- Tweeted '+str(i+1)+"/"+str(Repeat)+" -\n", 'cyan', attrs=[])
      print (twe + "--> " + str(tweeted))
    

      for i in range_with_status(wait):
        time.sleep(0.1)

  prompted = ""
  Prompts()
  
  

wait = 0 # init global wait var
prompted = "" # init global prompt var
Repeat = 0 # init global repeat var
Error = "" # init global error var
api = "" # init global api var

text = colored('-Program Started-', 'green', attrs=['reverse', 'blink'])

Twitter() # call twitter API
Prompts() # call prompts function to start program
