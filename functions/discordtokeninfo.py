from colorama import Fore, Style
import os
import sys
import time
import requests
from datetime import datetime, timezone
from utils.utils import clear, get_current_time, username, color, get_token_from_file
from utils.titles import title_discordtokeninfo

def discordtokeninfo():
    clear()
    print(getattr(Fore, color) + title_discordtokeninfo + Style.RESET_ALL)
    
    try:
        # Get Discord token from file or input
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
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Information Recovery...{Style.RESET_ALL}")
        
        try:
            # Get user information
            api = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token_discord}).json()
            
            # Check if token is valid
            response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token_discord, 'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                status = "Valid"
            else:
                status = "Invalid"
            
            # Extract user information
            username_discord = api.get('username', "None") + '#' + api.get('discriminator', "None")
            display_name_discord = api.get('global_name', "None")
            user_id_discord = api.get('id', "None")
            email_discord = api.get('email', "None")
            email_verified_discord = api.get('verified', "None")
            phone_discord = api.get('phone', "None")
            mfa_discord = api.get('mfa_enabled', "None")
            country_discord = api.get('locale', "None")
            avatar_discord = api.get('avatar', "None")
            avatar_decoration_discord = api.get('avatar_decoration_data', "None")
            public_flags_discord = api.get('public_flags', "None")
            flags_discord = api.get('flags', "None")
            banner_discord = api.get('banner', "None")
            banner_color_discord = api.get('banner_color', "None")
            accent_color_discord = api.get("accent_color", "None")
            nsfw_discord = api.get('nsfw_allowed', "None")
            
            # Calculate account creation date
            try:
                created_at_discord = datetime.fromtimestamp(((int(api.get('id', 'None')) >> 22) + 1420070400000) / 1000, timezone.utc)
            except:
                created_at_discord = "None"
            
            # Determine Nitro status
            try:
                if api.get('premium_type', 'None') == 0:
                    nitro_discord = 'False'
                elif api.get('premium_type', 'None') == 1:
                    nitro_discord = 'Nitro Classic'
                elif api.get('premium_type', 'None') == 2:
                    nitro_discord = 'Nitro Boosts'
                elif api.get('premium_type', 'None') == 3:
                    nitro_discord = 'Nitro Basic'
                else:
                    nitro_discord = 'False'
            except:
                nitro_discord = "None"
            
            # Get avatar URL
            try:
                avatar_url_discord = f"https://cdn.discordapp.com/avatars/{user_id_discord}/{api['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id_discord}/{api['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id_discord}/{api['avatar']}.png"
            except:
                avatar_url_discord = "None"
            
            # Get linked users
            try:
                linked_users_discord = api.get('linked_users', 'None')
                if isinstance(linked_users_discord, list):
                    linked_users_discord = ' / '.join(linked_users_discord)
                if not linked_users_discord or (isinstance(linked_users_discord, str) and not linked_users_discord.strip()):
                    linked_users_discord = "None"
            except:
                linked_users_discord = "None"
            
            # Get user bio
            try:
                bio_discord = "\n" + api.get('bio', 'None')
                if not bio_discord.strip() or bio_discord.isspace() or bio_discord == "\nNone":
                    bio_discord = "None"
            except:
                bio_discord = "None"
            
            # Get authenticator types
            try:
                authenticator_types_discord = api.get('authenticator_types', 'None')
                if isinstance(authenticator_types_discord, list):
                    authenticator_types_discord = ' / '.join(map(str, authenticator_types_discord))
                else:
                    authenticator_types_discord = str(authenticator_types_discord)
            except:
                authenticator_types_discord = "None"
            
            # Get guilds information
            try:
                guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token_discord})
                if guilds_response.status_code == 200:
                    guilds = guilds_response.json()
                    try:
                        guild_count = len(guilds)
                    except:
                        guild_count = "None"
                    try:
                        owner_guilds = [guild for guild in guilds if guild.get('owner', False)]
                        owner_guild_count = f"({len(owner_guilds)})"
                        owner_guilds_names = []
                        if owner_guilds:
                            for guild in owner_guilds:
                                owner_guilds_names.append(f"{guild['name']} ({guild['id']})")
                            owner_guilds_names = "\n" + "\n".join(owner_guilds_names)
                        else:
                            owner_guilds_names = "None"
                    except:
                        owner_guild_count = "None"
                        owner_guilds_names = "None"
                else:
                    owner_guild_count = "None"
                    guild_count = "None"
                    owner_guilds_names = "None"
            except:
                owner_guild_count = "None"
                guild_count = "None"
                owner_guilds_names = "None"
            
            # Get billing information
            try:
                billing_discord = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token_discord}).json()
                if billing_discord:
                    payment_methods_discord = []
                    
                    for method in billing_discord:
                        if method['type'] == 1:
                            payment_methods_discord.append('CB')
                        elif method['type'] == 2:
                            payment_methods_discord.append("Paypal")
                        else:
                            payment_methods_discord.append('Other')
                    payment_methods_discord = ' / '.join(payment_methods_discord)
                else:
                    payment_methods_discord = "None"
            except:
                payment_methods_discord = "None"
            
            # Get friends information
            try:
                friends = requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token_discord}).json()
                if friends:
                    friends_discord = []
                    for friend in friends:
                        unprefered_flags = [64, 128, 256, 1048704]
                        data = f"{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})"
                        
                        if len('\n'.join(friends_discord)) + len(data) >= 1024:
                            break
                        
                        friends_discord.append(data)
                    
                    if len(friends_discord) > 0:
                        friends_discord = '\n' + ' / '.join(friends_discord)
                    else:
                        friends_discord = "None"
                else:
                    friends_discord = "None"
            except:
                friends_discord = "None"
            
            # Get gift codes
            try:
                gift_codes_response = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token_discord}).json()
                if gift_codes_response:
                    gift_codes = []
                    for code_data in gift_codes_response:
                        name = code_data['promotion']['outbound_title']
                        code = code_data['code']
                        data = f"Gift: {name}\nCode: {code}"
                        gift_codes.append(data)
                    
                    if len(gift_codes) > 0:
                        gift_codes_discord = '\n\n'.join(gift_codes)
                    else:
                        gift_codes_discord = "None"
                else:
                    gift_codes_discord = "None"
            except:
                gift_codes_discord = "None"
            
            # Display all information
            print(f"""
{getattr(Fore, color)}[{get_current_time()}] [+] Status       : {Fore.WHITE}{status}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Token        : {Fore.WHITE}{token_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Username     : {Fore.WHITE}{username_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Display Name : {Fore.WHITE}{display_name_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Id           : {Fore.WHITE}{user_id_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Created      : {Fore.WHITE}{created_at_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Country      : {Fore.WHITE}{country_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Email        : {Fore.WHITE}{email_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Verified     : {Fore.WHITE}{email_verified_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Phone        : {Fore.WHITE}{phone_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Nitro        : {Fore.WHITE}{nitro_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Linked Users : {Fore.WHITE}{linked_users_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Avatar Decor : {Fore.WHITE}{avatar_decoration_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Avatar       : {Fore.WHITE}{avatar_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Avatar URL   : {Fore.WHITE}{avatar_url_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Accent Color : {Fore.WHITE}{accent_color_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Banner       : {Fore.WHITE}{banner_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Banner Color : {Fore.WHITE}{banner_color_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Flags        : {Fore.WHITE}{flags_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Public Flags : {Fore.WHITE}{public_flags_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] NSFW         : {Fore.WHITE}{nsfw_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Multi-Factor Authentication : {Fore.WHITE}{mfa_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Authenticator Type          : {Fore.WHITE}{authenticator_types_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Billing      : {Fore.WHITE}{payment_methods_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Gift Code    : {Fore.WHITE}{gift_codes_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Guilds       : {Fore.WHITE}{guild_count}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Owner Guilds : {Fore.WHITE}{owner_guild_count}{owner_guilds_names}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Bio          : {Fore.WHITE}{bio_discord}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Friend       : {Fore.WHITE}{friends_discord}{getattr(Fore, color)}
            """)
            
        except Exception as e:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error when retrieving information: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
    
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