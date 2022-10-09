from termcolor import colored
import subprocess

text = colored('-Program Started-', 'blue', attrs=['reverse', 'blink'])
print(text)

try:
    wait = int(input("Time (m) between tweets: "))
except:
    print(colored("- Error - \nInvalid Time", "red", attrs=[]))
    wait = 0

try:
    prompted = str(input("Prompt (joke, quote): "))
except:
    print(colored("- Error - \nInvalid Prompt", "red", attrs=[]))
    prompted = "error"

try:
    Repeat = int(input("Repeat: "))
except:
    print(colored("- Error - \nInvalid Repeat", "red", attrs=[]))
    Repeat = 1

wait = wait * 60


print('- ok -\n')
