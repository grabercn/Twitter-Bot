from termcolor import colored
import subprocess

text = colored('-Program Started-', 'blue', attrs=['reverse', 'blink'])
print(text)

wait = 0
prompted = ""
Repeat = 0

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
        
main()

print('- ok -\n')
