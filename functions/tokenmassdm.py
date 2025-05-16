from colorama import Fore, Style
import os
import sys
import time
import requests
import threading
from utils.utils import clear, get_current_time, username, color, get_token_from_file
from utils.titles import title_tokenmassdm

def tokenmassdm():
    clear()
    print(getattr(Fore, color) + title_tokenmassdm + Style.RESET_ALL)
    
    try:
        # Function to send DMs to multiple users
        def MassDM(token_discord, channels, Message):
            for channel in channels:
                for user in [x["username"]+"#"+x["discriminator"] for x in channel["recipients"]]:
                    try:
                        requests.post(f"https://discord.com/api/v9/channels/{channel['id']}/messages", 
                                     headers={'Authorization': token_discord}, 
                                     data={"content": f"{Message}"})
                        print(f'{getattr(Fore, color)}[{get_current_time()}] [+] Status: {Fore.WHITE}Sent{getattr(Fore, color)} User: {Fore.WHITE}{user}{getattr(Fore, color)}{Style.RESET_ALL}')
                    except Exception as e:
                        print(f'{getattr(Fore, color)}[{get_current_time()}] [!] Status: {Fore.WHITE}Error: {e}{getattr(Fore, color)}{Style.RESET_ALL}')
        
        # Get user's Discord token from file or input
        file_token = get_token_from_file()
        if file_token:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Token loaded from file{Style.RESET_ALL}")
            token_discord = file_token
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Token not found in file. Enter your Discord token{Style.RESET_ALL}")
            token_discord = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Token > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if token_discord.upper() == 'B':
                clear()
                # Return to main menu
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
        
        # Verify token
        validityTest = requests.get('https://discordapp.com/api/v6/users/@me', 
                                   headers={'Authorization': token_discord, 'Content-Type': 'application/json'})
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
        
        # Get message to send
        try:
            message = str(input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Message > {Style.RESET_ALL}"))
            
            # Check if user wants to return to main menu
            if message.upper() == 'B':
                clear()
                # Return to main menu
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
        except:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid message! Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Get number of repetitions
        try:
            repetition = int(input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Number of Repetitions > {Style.RESET_ALL}"))
            if repetition <= 0:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid number! Using default value (1).{Style.RESET_ALL}")
                repetition = 1
        except:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid number! Using default value (1).{Style.RESET_ALL}")
            repetition = 1
        
        # Get channel IDs
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Fetching DM channels...{Style.RESET_ALL}")
        channelIds = requests.get("https://discord.com/api/v9/users/@me/channels", 
                                 headers={'Authorization': token_discord}).json()
        
        if not channelIds:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] No DM channels found! Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Found {len(channelIds)} DM channels.{Style.RESET_ALL}")
        
        # Confirm action
        confirm = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Are you sure you want to send mass DMs? (y/n) > {Style.RESET_ALL}")
        
        if not confirm.lower() in ['y', 'yes']:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Operation cancelled. Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Start sending mass DMs
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting to send mass DMs...{Style.RESET_ALL}")
        
        number = 0
        for i in range(repetition):
            number += 1
            processes = []
            
            if not channelIds:
                break
                
            for channel_chunk in [channelIds[i:i+3] for i in range(0, len(channelIds), 3)]:
                t = threading.Thread(target=MassDM, args=(token_discord, channel_chunk, message))
                t.start()
                processes.append(t)
            
            for process in processes:
                process.join()
                
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Finished batch #{number}.{Style.RESET_ALL}")
            time.sleep(0.5)
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Mass DM completed!{Style.RESET_ALL}")
    
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