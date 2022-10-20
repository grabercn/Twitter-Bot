from queue import Empty
from termcolor import colored
import subprocess

text = colored('-Program Started-', 'green', attrs=['reverse', 'blink'])
print(text)

wait = 0
prompted = ""
Repeat = 0
blank = 0 # just a blank var to use as import

def main():
    
    global wait
    global prompted
    global Repeat
    
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
        
        elif do == "remove":
            break
        
        elif "tweet" in do:
            wait = int(do.split(" ")[1])
            prompted = str(do.split(" ")[2])
            Repeat = int(do.split(" ")[3])
            wait = wait * 60
            break
    
        


main()
print("- ok - \n")

