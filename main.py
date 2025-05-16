import os
import sys
import time
import random
from colorama import Fore, Style
from datetime import datetime


# import from utils
from utils.utils import clear, get_current_time, username, color, check_for_updates, versione
from utils.titles import title_1page, title_2page, title_update

# import from functions
from functions.ipscanner import ipscanner
from functions.ippinger import ippinger
from functions.emailtracker import emailtracker
from functions.phonelookup import phonelookup
from functions.phishingattack import phishingattack
from functions.ipgenerator import ipgenerator
from functions.websitescannervulnerability import websitescannervulnerability
from functions.usernametracker import usernametracker
from functions.discordaccnuker import discordaccnuker
from functions.discordtokenlogin import discordtokenlogin
from functions.discordtokeninfo import discordtokeninfo
from functions.discordtokengrabber import discordtokengrabber
from functions.nitrogenerator import nitrogenerator
from functions.tokenblockfriend import tokenblockfriend
from functions.webhookspammer import webhookspammer
from functions.botservernuker import botservernuker
from functions.tokenmassdm import tokenmassdm
from functions.discordserverinfo import discordserverinfo
from functions.discordtokenjoiner import discordtokenjoiner
from functions.discordserverraid import discordserverraid

def check_update():
    clear()
    print(getattr(Fore, color) + title_update + Style.RESET_ALL)
    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Checking for updates...{Style.RESET_ALL}")
    
    update_available, latest_version = check_for_updates()
    
    if update_available:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Update available!{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Current version: {Fore.WHITE}v{versione}{getattr(Fore, color)}{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Latest version: {Fore.WHITE}v{latest_version}{getattr(Fore, color)}{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Please update to the latest version for new features and bug fixes.{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Download the latest version from: {Fore.WHITE}https://github.com/SimoTools/SimoTools/releases/latest{getattr(Fore, color)}{Style.RESET_ALL}")
        
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue with current version or 'U' to exit...{Style.RESET_ALL}")
        user_input = input()
        
        if user_input.upper() == 'U':
            sys.exit()
    else:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] You are using the latest version: {Fore.WHITE}v{versione}{getattr(Fore, color)}{Style.RESET_ALL}")
        time.sleep(2)
    
    # Continue to main menu
    main()

def main(page=1):
    clear()
    if page == 1:
        print(Fore.LIGHTMAGENTA_EX + title_1page + Style.RESET_ALL)
    elif page == 2:
        print(Fore.LIGHTMAGENTA_EX + title_2page + Style.RESET_ALL)
    
    choice = input(getattr(Fore, color) + f"@{username} > " + Style.RESET_ALL)
    gestione(choice, page)

def gestione(choice, page):
    # Navigation between pages
    if choice.upper() == 'N' and page == 1:  # Go to page 2
        main(2)
        return
    elif choice.upper() == 'B' and page == 2:  # Back to page 1
        main(1)
        return
    
    # Handle options common to both pages
    if choice == '1':
        ipscanner()
    elif choice == '2':
        ippinger()
    elif choice == '3':
        emailtracker()
    elif choice == '4':
        phonelookup()
    elif choice == '5':
        phishingattack()
    elif choice == '6':
        ipgenerator()
    elif choice == '7':
        websitescannervulnerability()
    elif choice == '8':
        usernametracker()
    # Handle options specific to page 2
    elif choice == '9':
        discordaccnuker()
    elif choice == '10':
        discordtokengrabber()
    elif choice == '11':
        discordtokenlogin()
    elif choice == '12':
        discordtokeninfo()
    elif choice == '13':
        nitrogenerator()
    elif choice == '14':
        tokenblockfriend()
    elif choice == '15':
        webhookspammer()
    elif choice == '16':
        botservernuker()
    elif choice == '17':
        tokenmassdm()
    elif choice == '18':
        discordserverinfo()
    elif choice == '19':
        discordtokenjoiner()
    elif choice == '20':
        discordserverraid()
    else:
        # If the option is not valid, return to current page
        main(page)


check_update()