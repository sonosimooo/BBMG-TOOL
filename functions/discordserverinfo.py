from colorama import Fore, Style
import os
import sys
import time
import requests
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_discordserverinfo

def discordserverinfo():
    clear()
    print(getattr(Fore, color) + title_discordserverinfo + Style.RESET_ALL)
    
    try:
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
        
        # Extract invite code
        try:
            invite_code = invite.split("/")[-1]
        except:
            invite_code = invite
        
        # Get server info from Discord API
        response = requests.get(f"https://discord.com/api/v9/invites/{invite_code}")
        
        if response.status_code == 200:
            api = response.json()
            
            # Extract invitation information
            type_value = api.get('type', "None")
            code_value = api.get('code', "None")
            inviter_info = api.get('inviter', {})
            inviter_id = inviter_info.get('id', "None")
            inviter_username = inviter_info.get('username', "None")
            inviter_avatar = inviter_info.get('avatar', "None")
            inviter_discriminator = inviter_info.get('discriminator', "None")
            inviter_public_flags = inviter_info.get('public_flags', "None")
            inviter_flags = inviter_info.get('flags', "None")
            inviter_banner = inviter_info.get('banner', "None")
            inviter_accent_color = inviter_info.get('accent_color', "None")
            inviter_global_name = inviter_info.get('global_name', "None")
            inviter_banner_color = inviter_info.get('banner_color', "None")
            expires_at = api.get('expires_at', "None")
            flags = api.get('flags', "None")
            
            # Extract server information
            server_info = api.get('guild', {})
            server_id = server_info.get('id', "None")
            server_name = server_info.get('name', "None")
            server_icon = server_info.get('icon', "None")
            server_features = server_info.get('features', "None")
            if server_features != "None":
                server_features = ' / '.join(server_features)
            server_verification_level = server_info.get('verification_level', "None")
            server_nsfw_level = server_info.get('nsfw_level', "None")
            server_descritpion = server_info.get('description', "None")
            server_nsfw = server_info.get('nsfw', "None")
            server_premium_subscription_count = server_info.get('premium_subscription_count', "None")
            
            # Extract channel information
            channel_info = api.get('channel', {})
            channel_id = channel_info.get('id', "None")
            channel_type = channel_info.get('type', "None")
            channel_name = channel_info.get('name', "None")
            
            # Display server information
            print(f"""{getattr(Fore, color)}
    Invitation Information:
    [+] Invitation         : {Fore.WHITE}{invite}{getattr(Fore, color)}
    [+] Type               : {Fore.WHITE}{type_value}{getattr(Fore, color)}
    [+] Code               : {Fore.WHITE}{code_value}{getattr(Fore, color)}
    [+] Expired            : {Fore.WHITE}{expires_at}{getattr(Fore, color)}
    [+] Server ID          : {Fore.WHITE}{server_id}{getattr(Fore, color)}
    [+] Server Name        : {Fore.WHITE}{server_name}{getattr(Fore, color)}
    [+] Channel ID         : {Fore.WHITE}{channel_id}{getattr(Fore, color)}
    [+] Channel Name       : {Fore.WHITE}{channel_name}{getattr(Fore, color)}
    [+] Channel Type       : {Fore.WHITE}{channel_type}{getattr(Fore, color)}
    [+] Server Description : {Fore.WHITE}{server_descritpion}{getattr(Fore, color)}
    [+] Server Icon        : {Fore.WHITE}{server_icon}{getattr(Fore, color)}
    [+] Server Features    : {Fore.WHITE}{server_features}{getattr(Fore, color)}
    [+] Server NSFW Level  : {Fore.WHITE}{server_nsfw_level}{getattr(Fore, color)}
    [+] Server NSFW        : {Fore.WHITE}{server_nsfw}{getattr(Fore, color)}
    [+] Flags              : {Fore.WHITE}{flags}{getattr(Fore, color)}
    [+] Server Verification Level         : {Fore.WHITE}{server_verification_level}{getattr(Fore, color)}
    [+] Server Premium Subscription Count : {Fore.WHITE}{server_premium_subscription_count}{getattr(Fore, color)}
{Style.RESET_ALL}""")
            
            # Display inviter information if available
            if inviter_info:
                print(f"""    {getattr(Fore, color)}Inviter Information:
    [+] ID            : {Fore.WHITE}{inviter_id}{getattr(Fore, color)}
    [+] Username      : {Fore.WHITE}{inviter_username}{getattr(Fore, color)}
    [+] Global Name   : {Fore.WHITE}{inviter_global_name}{getattr(Fore, color)}
    [+] Avatar        : {Fore.WHITE}{inviter_avatar}{getattr(Fore, color)}
    [+] Discriminator : {Fore.WHITE}{inviter_discriminator}{getattr(Fore, color)}
    [+] Public Flags  : {Fore.WHITE}{inviter_public_flags}{getattr(Fore, color)}
    [+] Flags         : {Fore.WHITE}{inviter_flags}{getattr(Fore, color)}
    [+] Banner        : {Fore.WHITE}{inviter_banner}{getattr(Fore, color)}
    [+] Accent Color  : {Fore.WHITE}{inviter_accent_color}{getattr(Fore, color)}
    [+] Banner Color  : {Fore.WHITE}{inviter_banner_color}{getattr(Fore, color)}
    {Style.RESET_ALL}""")
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid invitation URL! Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
    
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