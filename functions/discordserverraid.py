from colorama import Fore, Style
import os
import sys
import time
import requests
import random
import threading
from utils.utils import clear, get_current_time, username, color, get_token_from_file
from utils.titles import title_discordserverraid

def discordserverraid():
    clear()
    print(getattr(Fore, color) + title_discordserverraid + Style.RESET_ALL)
    
    try:
        # Function to raid a channel with a message
        def raid(tokens, channels, message):
            try:
                token = random.choice(tokens)
                channel = random.choice(channels)
                response = requests.post(
                    f"https://discord.com/api/channels/{channel}/messages", 
                    data={'content': message}, 
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7', 
                        'Authorization': token
                    }
                )
                response.raise_for_status()
                print(f"{Fore.GREEN}[{get_current_time()}] [+] Message: {Fore.WHITE}{message_sensur}{Fore.GREEN} Channel: {Fore.WHITE}{channel}{Fore.GREEN} Status: {Fore.WHITE}Sent{Style.RESET_ALL}")
            except Exception as e:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Message: {Fore.WHITE}{message_sensur}{getattr(Fore, color)} Channel: {Fore.WHITE}{channel}{getattr(Fore, color)} Status: {Fore.WHITE}Error{Style.RESET_ALL}")
        
        # Get tokens
        tokens = []
        
        # First try to get token from file
        file_token = get_token_from_file()
        if file_token:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Token loaded from file{Style.RESET_ALL}")
            tokens.append(file_token)
        
        # Ask if user wants to add more tokens
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Do you want to add more tokens? (y/n){Style.RESET_ALL}")
        add_more = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}")
        
        if add_more.lower() in ['y', 'yes']:
            while True:
                token = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Token (or 'done' to finish) > {Style.RESET_ALL}")
                
                if token.lower() == 'done':
                    break
                
                if token.upper() == 'B':
                    clear()
                    # Return to main menu
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                    os.system(f'python "{main_path}"')
                    sys.exit()
                
                # Verify token
                try:
                    r = requests.get('https://discord.com/api/v8/users/@me', 
                                    headers={'Authorization': token, 'Content-Type': 'application/json'})
                    if r.status_code == 200:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Token verified successfully!{Style.RESET_ALL}")
                        tokens.append(token)
                    else:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid token! Try again.{Style.RESET_ALL}")
                except:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error verifying token! Try again.{Style.RESET_ALL}")
        
        if not tokens:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] No valid tokens provided. Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Get channels
        channels = []
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter channel IDs to raid{Style.RESET_ALL}")
        
        while True:
            channel = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Channel ID (or 'done' to finish) > {Style.RESET_ALL}")
            
            if channel.lower() == 'done':
                break
            
            if channel.upper() == 'B':
                clear()
                # Return to main menu
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
            
            channels.append(channel)
        
        if not channels:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] No channels provided. Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Get message to spam
        message = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Spam Message > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if message.upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Create a shortened version of the message for display
        message_len = len(message)
        if message_len > 10:
            message_sensur = message[:10] + "..."
        else:
            message_sensur = message
        
        # Get number of threads
        try:
            threads_number = int(input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Threads Number (recommended: 2, 4) > {Style.RESET_ALL}"))
        except:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid number. Using default value of 2.{Style.RESET_ALL}")
            threads_number = 2
        
        # Check if user wants to return to main menu
        if str(threads_number).upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Function to create and manage threads
        def request():
            threads = []
            try:
                for _ in range(int(threads_number)):
                    t = threading.Thread(target=raid, args=(tokens, channels, message))
                    t.start()
                    threads.append(t)
            except Exception as e:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error creating threads: {str(e)}{Style.RESET_ALL}")
            
            for thread in threads:
                thread.join()
        
        # Start raiding
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting raid with {len(tokens)} tokens on {len(channels)} channels{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press Ctrl+C to stop the raid{Style.RESET_ALL}")
        
        raid_count = 0
        try:
            while True:
                raid_count += 1
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Raid cycle #{raid_count}{Style.RESET_ALL}")
                request()
                
                # Ask if user wants to continue after each cycle
                print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue raiding or type 'B' to return to menu...{Style.RESET_ALL}")
                user_input = input()
                
                if user_input.upper() == 'B':
                    clear()
                    # Return to main menu
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                    os.system(f'python "{main_path}"')
                    sys.exit()
        
        except KeyboardInterrupt:
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Raid stopped by user.{Style.RESET_ALL}")
    
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