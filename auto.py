from credentials import consumer_key, consumer_secret, access_token, access_token_secret

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
    
    
    
    
Twitter()

