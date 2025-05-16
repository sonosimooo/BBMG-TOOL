import os
import sys
import time
import random
from colorama import Fore, Style
from datetime import datetime


# import from utils
from utils.utils import clear, get_current_time, username, color, check_for_updates, update_repository, versione
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
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Attempting to update automatically using Git...{Style.RESET_ALL}")
        
        # Try to update using Git
        success, message = update_repository()
        
        if success:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] {message}{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Please restart the application to use the updated version.{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press any key to exit...{Style.RESET_ALL}")
            input()
            sys.exit()
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] {message}{Style.RESET_ALL}")
            
            # Check if the error is related to local changes
            if "local changes" in message.lower() or "would be overwritten by merge" in message.lower():
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] You have local changes that would be lost during update.{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Options:{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [1] Force update (your changes will be lost){Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [2] Exit and update manually{Style.RESET_ALL}")
                
                choice = input(f"{getattr(Fore, color)}[{get_current_time()}] Choose an option (1/2): {Style.RESET_ALL}")
                
                if choice == "1":
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Forcing update...{Style.RESET_ALL}")
                    
                    # Force update by resetting and pulling
                    try:
                        import subprocess
                        # Reset to HEAD
                        subprocess.run(['git', 'reset', '--hard', 'HEAD'], 
                                     check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        # Pull latest changes
                        subprocess.run(['git', 'pull'], 
                                     check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Repository successfully updated to the latest version.{Style.RESET_ALL}")
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Please restart the application to use the updated version.{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to force update: {str(e)}{Style.RESET_ALL}")
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Please update manually from: {Fore.WHITE}https://github.com/sonosimooo/BBMG-TOOL/releases/latest{getattr(Fore, color)}{Style.RESET_ALL}")
                    
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press any key to exit...{Style.RESET_ALL}")
                    input()
                    sys.exit()
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Please update manually from: {Fore.WHITE}https://github.com/sonosimooo/BBMG-TOOL/releases/latest{getattr(Fore, color)}{Style.RESET_ALL}")
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Please update manually from: {Fore.WHITE}https://github.com/sonosimooo/BBMG-TOOL/releases/latest{getattr(Fore, color)}{Style.RESET_ALL}")
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Update is required to continue.{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press any key to exit...{Style.RESET_ALL}")
            input()
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
