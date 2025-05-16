from colorama import Fore, Style
import os
import sys
import time
import requests
import threading
from utils.utils import clear, get_current_time, username, color, get_token_from_file
from utils.titles import title_tokenblockfriend

def tokenblockfriend():
    clear()
    print(getattr(Fore, color) + title_tokenblockfriend + Style.RESET_ALL)
    
    try:
        # Get user's Discord token from file or input
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
        
        # Verify token
        r = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
        if r.status_code == 200:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Token verified successfully!{Style.RESET_ALL}")
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid token! Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Function to block friends
        def BlockFriends(token, friends):
            for friend in friends:
                try:
                    requests.put(f'https://discord.com/api/v9/users/@me/relationships/'+friend['id'], 
                                headers={'Authorization': token}, 
                                json={"type": 2})
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Status: {Fore.WHITE}Blocked{getattr(Fore, color)} | User: {Fore.WHITE}{friend['user']['username']}#{friend['user']['discriminator']}{getattr(Fore, color)}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error: {str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Get friend list
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Fetching friend list...{Style.RESET_ALL}")
        friend_id = requests.get("https://discord.com/api/v9/users/@me/relationships", 
                                headers={'Authorization': token}).json()
        
        if not friend_id:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] No friends found.{Style.RESET_ALL}")
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue...{Style.RESET_ALL}")
            input()
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Confirm action
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Found {len(friend_id)} friends.{Style.RESET_ALL}")
        confirm = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Are you sure you want to block all friends? (y/n) > {Style.RESET_ALL}")
        
        if not confirm.lower() in ['y', 'yes']:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Operation cancelled. Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Start blocking friends
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting to block friends...{Style.RESET_ALL}")
        
        processes = []
        for friend_chunk in [friend_id[i:i+3] for i in range(0, len(friend_id), 3)]:
            t = threading.Thread(target=BlockFriends, args=(token, friend_chunk))
            t.start()
            processes.append(t)
        
        for process in processes:
            process.join()
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] All friends have been blocked!{Style.RESET_ALL}")
    
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