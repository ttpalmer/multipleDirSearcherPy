from colorama import init, Fore, Back, Style
from datetime import datetime
import time

def log(tag,text):
    now = datetime.now()
    dt = now.strftime("%b-%d-%Y %H:%M:%S")
    if tag == "i":
        print (Fore.YELLOW + dt + " [ INFO ] " + text)
    elif tag == "e":
        print (Fore.RED +dt + " [ ERROR ] " + text)
    elif tag == 's':
        print (Fore.GREEN +dt + " [ SUCCESS ] " + text)
    elif tag == 'm':
        print (Fore.CYAN  + text)