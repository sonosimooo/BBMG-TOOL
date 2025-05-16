from colorama import Fore, Style
import os
import sys
import time
import requests
from utils.utils import clear, get_current_time, username, color, get_token_from_file
from utils.titles import title_discordtokenjoiner

def discordtokenjoiner():
    clear()
    print(getattr(Fore, color) + title_discordtokenjoiner + Style.RESET_ALL)
    
    try:
        # Function to join a server with a token
        def joiner(token, invite):
            invite_code = invite.split("/")[-1]
            
            try:
                # Get server name from invite
                response = requests.get(f"https://discord.com/api/v9/invites/{invite_code}")
                if response.status_code == 200:
                    server_name = response.json().get('guild', {}).get('name')
                else:
                    server_name = invite
            except:
                server_name = invite
            
            try:
                # Join the server
                response = requests.post(f"https://discord.com/api/v9/invites/{invite_code}", 
                                       headers={'Authorization': token})
                
                if response.status_code == 200:
                    print(f"{Fore.GREEN}[{get_current_time()}] [+] Status: {Fore.WHITE}Joined{Fore.GREEN} Server: {Fore.WHITE}{server_name}{Style.RESET_ALL}")
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error {response.status_code}{getattr(Fore, color)} Server: {Fore.WHITE}{server_name}{Style.RESET_ALL}")
            except:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error{getattr(Fore, color)} Server: {Fore.WHITE}{server_name}{Style.RESET_ALL}")
        
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
        validityTest = requests.get('https://discordapp.com/api/v6/users/@me', 
                                   headers={'Authorization': token, 'Content-Type': 'application/json'})
        if validityTest.status_code != 200:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid token! Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Token verified successfully!{Style.RESET_ALL}")
        
        # Get server invitation
        invite = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Server Invitation > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if invite.upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Join the server
        joiner(token, invite)
    
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{Style.RESET_ALL}")
    
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