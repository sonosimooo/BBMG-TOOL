from colorama import Fore, Style
import os
import sys
import time
import requests
import json
import threading
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_webhookspammer

def webhookspammer():
    clear()
    print(getattr(Fore, color) + title_webhookspammer + Style.RESET_ALL)
    
    try:
        # Get webhook URL
        webhook_url = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Webhook URL > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if webhook_url.upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Verify webhook
        try:
            webhook_check = requests.get(webhook_url)
            if webhook_check.status_code != 200:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid webhook URL! Returning to menu...{Style.RESET_ALL}")
                time.sleep(2)
                clear()
                # Return to main menu
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Webhook verified successfully!{Style.RESET_ALL}")
        except:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid webhook URL! Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Get message to spam
        message = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Message > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if message.upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
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
        username_webhook = "SimoTools Webhook Spammer"
        avatar_webhook = "https://i.imgur.com/4M34hi2.png"
        
        # Function to send webhook
        def send_webhook():
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                'content': message,
                'username': username_webhook,
                'avatar_url': avatar_webhook
            }
            try:
                response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
                response.raise_for_status()
                print(f"{Fore.GREEN}[{get_current_time()}] [+] Message: {Fore.WHITE}{message}{Fore.GREEN} Status: {Fore.WHITE}Sent{Fore.GREEN}{Style.RESET_ALL}")
            except:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [-] Message: {Fore.WHITE}{message}{getattr(Fore, color)} Status: {Fore.WHITE}Rate Limit{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Function to create and manage threads
        def request():
            threads = []
            try:
                for _ in range(int(threads_number)):
                    t = threading.Thread(target=send_webhook)
                    t.start()
                    threads.append(t)
            except:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error creating threads!{Style.RESET_ALL}")
            
            for thread in threads:
                thread.join()
        
        # Main loop for webhook spamming
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting webhook spammer with {threads_number} threads{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press Ctrl+C to stop the process{Style.RESET_ALL}")
        
        try:
            attempts = 0
            while True:
                attempts += 1
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
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Webhook spammer stopped by user.{Style.RESET_ALL}")
    
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