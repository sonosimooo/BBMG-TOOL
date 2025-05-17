from colorama import Fore, Style
import os
import sys
import time
import json
import requests
import datetime
import base64
from utils.utils import clear, get_current_time, username, color, get_token_from_file
from utils.titles import title_discordserverbackup

def discordserverbackup():
    clear()
    print(getattr(Fore, color) + title_discordserverbackup + Style.RESET_ALL)
    
    # Ask user if they want to backup a server or restore from backup
    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Select an option:{Style.RESET_ALL}")
    print(f"{getattr(Fore, color)}[{get_current_time()}] [1] Backup a Discord server{Style.RESET_ALL}")
    print(f"{getattr(Fore, color)}[{get_current_time()}] [2] Restore a server from backup{Style.RESET_ALL}")
    
    option = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Option > {Style.RESET_ALL}")
    
    # Check if user wants to return to main menu
    if option.upper() == 'B':
        return_to_menu()
    
    if option == '1':
        backup_server()
    elif option == '2':
        restore_server()
    else:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid option. Please try again.{Style.RESET_ALL}")
        time.sleep(2)
        discordserverbackup()

def return_to_menu():
    clear()
    # Return to main menu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
    os.system(f'python "{main_path}"')
    sys.exit()

def get_discord_token():
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
            return_to_menu()
    
    return token

def get_token_for_restore():
    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Select token type:{Style.RESET_ALL}")
    print(f"{getattr(Fore, color)}[{get_current_time()}] [1] Use user token (may have server creation limits){Style.RESET_ALL}")
    print(f"{getattr(Fore, color)}[{get_current_time()}] [2] Use bot token (requires bot with 'applications.commands' scope and 'bot' scope with Administrator permission){Style.RESET_ALL}")
    
    token_type = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Option > {Style.RESET_ALL}")
    
    # Check if user wants to return to main menu
    if token_type.upper() == 'B':
        return_to_menu()
    
    if token_type == '1':
        token = get_discord_token()
        return token, False  # False indicates not a bot token
    elif token_type == '2':
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter your Discord bot token{Style.RESET_ALL}")
        token = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Bot token > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if token.upper() == 'B':
            return_to_menu()
        
        return token, True  # True indicates a bot token
    else:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid option. Using user token by default.{Style.RESET_ALL}")
        token = get_discord_token()
        return token, False

def backup_server():
    try:
        token = get_discord_token()
        
        # Set up headers for API requests
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        # Get user's servers (guilds)
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Fetching your servers...{Style.RESET_ALL}")
        guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
        
        if guilds_response.status_code != 200:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to fetch servers. Status code: {guilds_response.status_code}{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {guilds_response.text}{Style.RESET_ALL}")
            raise Exception("Failed to fetch servers")
        
        guilds = guilds_response.json()
        
        if not guilds:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] No servers found for this token{Style.RESET_ALL}")
            raise Exception("No servers found")
        
        # Display available servers
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Available servers:{Style.RESET_ALL}")
        for i, guild in enumerate(guilds, 1):
            print(f"{getattr(Fore, color)}    {i}. {Fore.WHITE}{guild['name']}{getattr(Fore, color)} (ID: {Fore.WHITE}{guild['id']}{getattr(Fore, color)}){Style.RESET_ALL}")
        
        # Ask user to select a server
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Enter the number of the server to backup{Style.RESET_ALL}")
        server_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Server > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if server_choice.upper() == 'B':
            return_to_menu()
        
        try:
            server_index = int(server_choice) - 1
            if server_index < 0 or server_index >= len(guilds):
                raise ValueError("Invalid server number")
            
            selected_guild = guilds[server_index]
            guild_id = selected_guild['id']
            guild_name = selected_guild['name']
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Selected server: {Fore.WHITE}{guild_name}{getattr(Fore, color)} (ID: {Fore.WHITE}{guild_id}{getattr(Fore, color)}){Style.RESET_ALL}")
            
            # Create backup directory if it doesn't exist
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
            backup_dir = os.path.join(output_dir, 'backups')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Create server-specific directory with timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            server_backup_dir = os.path.join(backup_dir, f"{guild_name.replace(' ', '_')}_{timestamp}")
            if not os.path.exists(server_backup_dir):
                os.makedirs(server_backup_dir)
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting backup process...{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Backup will be saved to: {Fore.WHITE}{server_backup_dir}{getattr(Fore, color)}{Style.RESET_ALL}")
            
            # Backup server information
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Backing up server information...{Style.RESET_ALL}")
            server_info = {
                'id': guild_id,
                'name': guild_name,
                'icon': selected_guild.get('icon'),
                'owner': selected_guild.get('owner', False),
                'permissions': selected_guild.get('permissions'),
                'features': selected_guild.get('features', []),
                'backup_date': timestamp
            }
            
            with open(os.path.join(server_backup_dir, 'server_info.json'), 'w', encoding='utf-8') as f:
                json.dump(server_info, f, indent=4)
            
            # Backup channels
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Backing up channels...{Style.RESET_ALL}")
            channels_response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
            
            if channels_response.status_code == 200:
                channels = channels_response.json()
                with open(os.path.join(server_backup_dir, 'channels.json'), 'w', encoding='utf-8') as f:
                    json.dump(channels, f, indent=4)
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Backed up {Fore.WHITE}{len(channels)}{getattr(Fore, color)} channels{Style.RESET_ALL}")
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to backup channels. Status code: {channels_response.status_code}{Style.RESET_ALL}")
            
            # Backup roles
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Backing up roles...{Style.RESET_ALL}")
            roles_response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=headers)
            
            if roles_response.status_code == 200:
                roles = roles_response.json()
                with open(os.path.join(server_backup_dir, 'roles.json'), 'w', encoding='utf-8') as f:
                    json.dump(roles, f, indent=4)
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Backed up {Fore.WHITE}{len(roles)}{getattr(Fore, color)} roles{Style.RESET_ALL}")
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to backup roles. Status code: {roles_response.status_code}{Style.RESET_ALL}")
            
            # Backup emojis
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Backing up emojis...{Style.RESET_ALL}")
            emojis_response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/emojis', headers=headers)
            
            if emojis_response.status_code == 200:
                emojis = emojis_response.json()
                with open(os.path.join(server_backup_dir, 'emojis.json'), 'w', encoding='utf-8') as f:
                    json.dump(emojis, f, indent=4)
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Backed up {Fore.WHITE}{len(emojis)}{getattr(Fore, color)} emojis{Style.RESET_ALL}")
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to backup emojis. Status code: {emojis_response.status_code}{Style.RESET_ALL}")
            
            # Backup server icon if available
            if selected_guild.get('icon'):
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Backing up server icon...{Style.RESET_ALL}")
                icon_url = f"https://cdn.discordapp.com/icons/{guild_id}/{selected_guild['icon']}.png"
                icon_response = requests.get(icon_url)
                
                if icon_response.status_code == 200:
                    with open(os.path.join(server_backup_dir, 'server_icon.png'), 'wb') as f:
                        f.write(icon_response.content)
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Backed up server icon{Style.RESET_ALL}")
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to backup server icon. Status code: {icon_response.status_code}{Style.RESET_ALL}")
            
            # Backup server banner if available
            if selected_guild.get('banner'):
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Backing up server banner...{Style.RESET_ALL}")
                banner_url = f"https://cdn.discordapp.com/banners/{guild_id}/{selected_guild['banner']}.png"
                banner_response = requests.get(banner_url)
                
                if banner_response.status_code == 200:
                    with open(os.path.join(server_backup_dir, 'server_banner.png'), 'wb') as f:
                        f.write(banner_response.content)
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Backed up server banner{Style.RESET_ALL}")
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to backup server banner. Status code: {banner_response.status_code}{Style.RESET_ALL}")
            
            # Try to backup some members (limited by Discord API)
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Backing up members (limited to first 1000)...{Style.RESET_ALL}")
            members_response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000', headers=headers)
            
            if members_response.status_code == 200:
                members = members_response.json()
                with open(os.path.join(server_backup_dir, 'members.json'), 'w', encoding='utf-8') as f:
                    json.dump(members, f, indent=4)
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Backed up {Fore.WHITE}{len(members)}{getattr(Fore, color)} members{Style.RESET_ALL}")
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to backup members. Status code: {members_response.status_code}{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] This is normal if you don't have the required permissions{Style.RESET_ALL}")
            
            # Create a summary file
            summary = {
                'server_name': guild_name,
                'server_id': guild_id,
                'backup_date': timestamp,
                'backup_items': {
                    'server_info': True,
                    'channels': channels_response.status_code == 200,
                    'roles': roles_response.status_code == 200,
                    'emojis': emojis_response.status_code == 200,
                    'icon': selected_guild.get('icon') is not None and icon_response.status_code == 200 if selected_guild.get('icon') else False,
                    'banner': selected_guild.get('banner') is not None and banner_response.status_code == 200 if selected_guild.get('banner') else False,
                    'members': members_response.status_code == 200
                }
            }
            
            with open(os.path.join(server_backup_dir, 'backup_summary.json'), 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=4)
            
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [+] Backup completed successfully!{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Backup saved to: {Fore.WHITE}{server_backup_dir}{getattr(Fore, color)}{Style.RESET_ALL}")
            
        except ValueError as e:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
    
    print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
    user_input = input()
    
    # Check if user wants to return to main menu
    if user_input.upper() == 'B':
        return_to_menu()
    else:
        return_to_menu()

def restore_server():
    try:
        token, is_bot = get_token_for_restore()
        
        # Set up headers for API requests
        if is_bot:
            headers = {
                'Authorization': f'Bot {token}',
                'Content-Type': 'application/json'
            }
        else:
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
        
        # Get backup directories
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        backup_dir = os.path.join(output_dir, 'backups')
        if not os.path.exists(backup_dir):
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] No backups found. Please create a backup first.{Style.RESET_ALL}")
            raise Exception("No backups found")
        
        backup_folders = [f for f in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, f))]
        
        if not backup_folders:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] No backups found. Please create a backup first.{Style.RESET_ALL}")
            raise Exception("No backups found")
        
        # Display available backups
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Available backups:{Style.RESET_ALL}")
        for i, folder in enumerate(backup_folders, 1):
            # Try to get server name from backup_summary.json
            summary_path = os.path.join(backup_dir, folder, 'backup_summary.json')
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                    server_name = summary.get('server_name', folder)
                    backup_date = summary.get('backup_date', 'Unknown date')
                    print(f"{getattr(Fore, color)}    {i}. {Fore.WHITE}{server_name}{getattr(Fore, color)} (Backup date: {Fore.WHITE}{backup_date}{getattr(Fore, color)}){Style.RESET_ALL}")
            else:
                print(f"{getattr(Fore, color)}    {i}. {Fore.WHITE}{folder}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Ask user to select a backup
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Enter the number of the backup to restore{Style.RESET_ALL}")
        backup_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Backup > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if backup_choice.upper() == 'B':
            return_to_menu()
        
        try:
            backup_index = int(backup_choice) - 1
            if backup_index < 0 or backup_index >= len(backup_folders):
                raise ValueError("Invalid backup number")
            
            selected_backup = backup_folders[backup_index]
            backup_path = os.path.join(backup_dir, selected_backup)
            
            # Check if backup contains necessary files
            required_files = ['server_info.json', 'channels.json', 'roles.json']
            missing_files = [f for f in required_files if not os.path.exists(os.path.join(backup_path, f))]
            
            if missing_files:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Backup is missing required files: {', '.join(missing_files)}{Style.RESET_ALL}")
                raise Exception("Incomplete backup")
            
            # Load backup data
            with open(os.path.join(backup_path, 'server_info.json'), 'r', encoding='utf-8') as f:
                server_info = json.load(f)
            
            with open(os.path.join(backup_path, 'channels.json'), 'r', encoding='utf-8') as f:
                channels = json.load(f)
            
            with open(os.path.join(backup_path, 'roles.json'), 'r', encoding='utf-8') as f:
                roles = json.load(f)
            
            # Ask if user wants to create a new server or use an existing one
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Do you want to create a new server or use an existing one?{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [1] Create a new server{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [2] Use an existing server (WARNING: This will delete all channels and roles in the existing server){Style.RESET_ALL}")
            
            server_option = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Option > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if server_option.upper() == 'B':
                return_to_menu()
            
            if server_option == '2':
                # Get user's servers
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Fetching your servers...{Style.RESET_ALL}")
                guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
                
                if guilds_response.status_code != 200:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to fetch servers. Status code: {guilds_response.status_code}{Style.RESET_ALL}")
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {guilds_response.text}{Style.RESET_ALL}")
                    raise Exception("Failed to fetch servers")
                
                guilds = guilds_response.json()
                
                if not guilds:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] No servers found for this token{Style.RESET_ALL}")
                    raise Exception("No servers found")
                
                # Display available servers
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Available servers:{Style.RESET_ALL}")
                for i, guild in enumerate(guilds, 1):
                    print(f"{getattr(Fore, color)}    {i}. {Fore.WHITE}{guild['name']}{getattr(Fore, color)} (ID: {Fore.WHITE}{guild['id']}{getattr(Fore, color)}){Style.RESET_ALL}")
                
                # Ask user to select a server
                print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Enter the number of the server to use{Style.RESET_ALL}")
                server_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Server > {Style.RESET_ALL}")
                
                # Check if user wants to return to main menu
                if server_choice.upper() == 'B':
                    return_to_menu()
                
                try:
                    server_index = int(server_choice) - 1
                    if server_index < 0 or server_index >= len(guilds):
                        raise ValueError("Invalid server number")
                    
                    selected_guild = guilds[server_index]
                    new_guild_id = selected_guild['id']
                    
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Selected server: {Fore.WHITE}{selected_guild['name']}{getattr(Fore, color)} (ID: {Fore.WHITE}{new_guild_id}{getattr(Fore, color)}){Style.RESET_ALL}")
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] WARNING: All channels and roles in this server will be deleted!{Style.RESET_ALL}")
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Are you sure you want to continue? (Y/N){Style.RESET_ALL}")
                    
                    confirm = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}")
                    if confirm.upper() != 'Y':
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Operation cancelled.{Style.RESET_ALL}")
                        return_to_menu()
                    
                    # Get existing channels to delete them
                    channels_response = requests.get(f'https://discord.com/api/v9/guilds/{new_guild_id}/channels', headers=headers)
                    if channels_response.status_code == 200:
                        existing_channels = channels_response.json()
                        
                        # Delete existing channels
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Removing existing channels...{Style.RESET_ALL}")
                        for channel in existing_channels:
                            delete_response = requests.delete(f'https://discord.com/api/v9/channels/{channel["id"]}', headers=headers)
                            if delete_response.status_code != 200:
                                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to delete channel {channel['name']}{Style.RESET_ALL}")
                    
                    # Get existing roles to delete them
                    roles_response = requests.get(f'https://discord.com/api/v9/guilds/{new_guild_id}/roles', headers=headers)
                    if roles_response.status_code == 200:
                        existing_roles = roles_response.json()
                        
                        # Delete existing roles (except @everyone)
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Removing existing roles...{Style.RESET_ALL}")
                        for role in existing_roles:
                            if role['name'] != '@everyone':
                                delete_response = requests.delete(f'https://discord.com/api/v9/guilds/{new_guild_id}/roles/{role["id"]}', headers=headers)
                                if delete_response.status_code != 204:
                                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to delete role {role['name']}{Style.RESET_ALL}")
                    
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Server prepared for restoration{Style.RESET_ALL}")
                    
                    # Use the existing server
                    new_guild = selected_guild
                    
                except ValueError as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
                    raise Exception("Invalid server selection")
                
            else:
                # Ask for new server name
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Original server name: {Fore.WHITE}{server_info['name']}{getattr(Fore, color)}{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter a name for the new server (or press Enter to use the original name){Style.RESET_ALL}")
                new_server_name = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Server name > {Style.RESET_ALL}")
                
                if not new_server_name:
                    new_server_name = server_info['name']
                
                # Create new server
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Creating new server: {Fore.WHITE}{new_server_name}{getattr(Fore, color)}{Style.RESET_ALL}")
            
            # Prepare icon data if available
            icon_data = None
            icon_path = os.path.join(backup_path, 'server_icon.png')
            if os.path.exists(icon_path):
                with open(icon_path, 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    icon_data = f"data:image/png;base64,{encoded_string}"
            
            # Create server
            create_guild_payload = {
                'name': new_server_name,
                'region': 'us-central',
                'icon': icon_data
            }
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Attempting to create server... This may take a moment.{Style.RESET_ALL}")
            create_response = requests.post('https://discord.com/api/v9/guilds', headers=headers, json=create_guild_payload)
            
            if create_response.status_code != 201:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to create server. Status code: {create_response.status_code}{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {create_response.text}{Style.RESET_ALL}")
                
                # Provide more helpful information based on the error code
                if create_response.status_code == 403:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Permission denied. This could be due to:{Style.RESET_ALL}")
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] - Your account has reached the maximum number of servers you can create{Style.RESET_ALL}")
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] - Your account is not verified with a phone number{Style.RESET_ALL}")
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] - The token does not have the required permissions{Style.RESET_ALL}")
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] - Your account may be temporarily rate-limited by Discord{Style.RESET_ALL}")
                    
                    # Offer alternative method
                    print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Would you like to try an alternative method? (Y/N){Style.RESET_ALL}")
                    alt_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}")
                    
                    if alt_choice.upper() == 'Y':
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Trying alternative method...{Style.RESET_ALL}")
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] This method will create a template and then create a server from it.{Style.RESET_ALL}")
                        
                        # Create a template first
                        template_payload = {
                            'name': f"template_{new_server_name[:20]}",  # Max 30 chars
                            'description': f"Template for {new_server_name}"
                        }
                        
                        # Get an existing guild ID from the user
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter the ID of one of your existing servers to use as base:{Style.RESET_ALL}")
                        existing_guild_id = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Server ID > {Style.RESET_ALL}")
                        
                        # Create template
                        template_response = requests.post(
                            f'https://discord.com/api/v9/guilds/{existing_guild_id}/templates', 
                            headers=headers, 
                            json=template_payload
                        )
                        
                        if template_response.status_code == 201:
                            template_data = template_response.json()
                            template_code = template_data.get('code')
                            
                            # Create guild from template
                            template_guild_payload = {
                                'name': new_server_name
                            }
                            
                            template_guild_response = requests.post(
                                f'https://discord.com/api/v9/guilds/templates/{template_code}', 
                                headers=headers, 
                                json=template_guild_payload
                            )
                            
                            if template_guild_response.status_code == 201:
                                new_guild = template_guild_response.json()
                                new_guild_id = new_guild['id']
                                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Server created successfully using template! ID: {Fore.WHITE}{new_guild_id}{getattr(Fore, color)}{Style.RESET_ALL}")
                                return new_guild, new_guild_id
                            else:
                                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to create server from template. Status code: {template_guild_response.status_code}{Style.RESET_ALL}")
                                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {template_guild_response.text}{Style.RESET_ALL}")
                        else:
                            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to create template. Status code: {template_response.status_code}{Style.RESET_ALL}")
                            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {template_response.text}{Style.RESET_ALL}")
                    
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Try again later or use a different account with fewer servers.{Style.RESET_ALL}")
                elif create_response.status_code == 429:
                    retry_after = create_response.json().get('retry_after', 5)
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Rate limited by Discord. Try again after {retry_after} seconds.{Style.RESET_ALL}")
                
                raise Exception("Failed to create server")
            
            new_guild = create_response.json()
            new_guild_id = new_guild['id']
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Server created successfully! ID: {Fore.WHITE}{new_guild_id}{getattr(Fore, color)}{Style.RESET_ALL}")
            
            # Get default channels to delete them
            channels_response = requests.get(f'https://discord.com/api/v9/guilds/{new_guild_id}/channels', headers=headers)
            if channels_response.status_code == 200:
                default_channels = channels_response.json()
                
                # Delete default channels
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Removing default channels...{Style.RESET_ALL}")
                for channel in default_channels:
                    delete_response = requests.delete(f'https://discord.com/api/v9/channels/{channel["id"]}', headers=headers)
                    if delete_response.status_code != 200:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to delete channel {channel['name']}{Style.RESET_ALL}")
            
            # Create roles (in reverse order to maintain hierarchy)
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Creating roles...{Style.RESET_ALL}")
            role_id_map = {}  # Map old role IDs to new role IDs
            
            # Filter out @everyone role
            filtered_roles = [r for r in roles if r['name'] != '@everyone']
            
            # Sort roles by position (highest first)
            sorted_roles = sorted(filtered_roles, key=lambda r: r['position'], reverse=True)
            
            for role in sorted_roles:
                # Skip managed roles (bot roles, etc.)
                if role.get('managed', False):
                    continue
                
                role_payload = {
                    'name': role['name'],
                    'permissions': role['permissions'],
                    'color': role['color'],
                    'hoist': role.get('hoist', False),
                    'mentionable': role.get('mentionable', False)
                }
                
                role_response = requests.post(f'https://discord.com/api/v9/guilds/{new_guild_id}/roles', headers=headers, json=role_payload)
                
                if role_response.status_code == 200:
                    new_role = role_response.json()
                    role_id_map[role['id']] = new_role['id']
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Created role: {Fore.WHITE}{role['name']}{getattr(Fore, color)}{Style.RESET_ALL}")
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to create role {role['name']}. Status code: {role_response.status_code}{Style.RESET_ALL}")
            
            # Create channels
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Creating channels...{Style.RESET_ALL}")
            
            # Group channels by type and parent
            categories = [c for c in channels if c['type'] == 4]  # 4 = category
            text_channels = [c for c in channels if c['type'] == 0]  # 0 = text
            voice_channels = [c for c in channels if c['type'] == 2]  # 2 = voice
            
            # Create categories first
            category_id_map = {}  # Map old category IDs to new category IDs
            
            for category in categories:
                category_payload = {
                    'name': category['name'],
                    'type': 4,
                    'permission_overwrites': []
                }
                
                # Map role IDs in permission overwrites
                if 'permission_overwrites' in category:
                    for overwrite in category['permission_overwrites']:
                        if overwrite['type'] == 0 and overwrite['id'] in role_id_map:  # 0 = role
                            overwrite['id'] = role_id_map[overwrite['id']]
                            category_payload['permission_overwrites'].append(overwrite)
                
                category_response = requests.post(f'https://discord.com/api/v9/guilds/{new_guild_id}/channels', headers=headers, json=category_payload)
                
                if category_response.status_code == 201:
                    new_category = category_response.json()
                    category_id_map[category['id']] = new_category['id']
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Created category: {Fore.WHITE}{category['name']}{getattr(Fore, color)}{Style.RESET_ALL}")
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to create category {category['name']}. Status code: {category_response.status_code}{Style.RESET_ALL}")
            
            # Create text channels
            for channel in text_channels:
                channel_payload = {
                    'name': channel['name'],
                    'type': 0,
                    'topic': channel.get('topic', ''),
                    'permission_overwrites': []
                }
                
                # Set parent category if applicable
                if 'parent_id' in channel and channel['parent_id'] in category_id_map:
                    channel_payload['parent_id'] = category_id_map[channel['parent_id']]
                
                # Map role IDs in permission overwrites
                if 'permission_overwrites' in channel:
                    for overwrite in channel['permission_overwrites']:
                        if overwrite['type'] == 0 and overwrite['id'] in role_id_map:  # 0 = role
                            overwrite['id'] = role_id_map[overwrite['id']]
                            channel_payload['permission_overwrites'].append(overwrite)
                
                channel_response = requests.post(f'https://discord.com/api/v9/guilds/{new_guild_id}/channels', headers=headers, json=channel_payload)
                
                if channel_response.status_code == 201:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Created text channel: {Fore.WHITE}{channel['name']}{getattr(Fore, color)}{Style.RESET_ALL}")
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to create text channel {channel['name']}. Status code: {channel_response.status_code}{Style.RESET_ALL}")
            
            # Create voice channels
            for channel in voice_channels:
                channel_payload = {
                    'name': channel['name'],
                    'type': 2,
                    'permission_overwrites': []
                }
                
                # Set parent category if applicable
                if 'parent_id' in channel and channel['parent_id'] in category_id_map:
                    channel_payload['parent_id'] = category_id_map[channel['parent_id']]
                
                # Set user limit if applicable
                if 'user_limit' in channel:
                    channel_payload['user_limit'] = channel['user_limit']
                
                # Map role IDs in permission overwrites
                if 'permission_overwrites' in channel:
                    for overwrite in channel['permission_overwrites']:
                        if overwrite['type'] == 0 and overwrite['id'] in role_id_map:  # 0 = role
                            overwrite['id'] = role_id_map[overwrite['id']]
                            channel_payload['permission_overwrites'].append(overwrite)
                
                channel_response = requests.post(f'https://discord.com/api/v9/guilds/{new_guild_id}/channels', headers=headers, json=channel_payload)
                
                if channel_response.status_code == 201:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Created voice channel: {Fore.WHITE}{channel['name']}{getattr(Fore, color)}{Style.RESET_ALL}")
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to create voice channel {channel['name']}. Status code: {channel_response.status_code}{Style.RESET_ALL}")
            
            # Try to restore emojis if available
            emoji_path = os.path.join(backup_path, 'emojis.json')
            if os.path.exists(emoji_path):
                with open(emoji_path, 'r', encoding='utf-8') as f:
                    emojis = json.load(f)
                
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Restoring emojis (this may take a while)...{Style.RESET_ALL}")
                
                emoji_count = 0
                for emoji in emojis:
                    # Skip managed emojis
                    if emoji.get('managed', False):
                        continue
                    
                    # Get emoji image
                    emoji_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.png"
                    if emoji.get('animated', False):
                        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.gif"
                    
                    emoji_response = requests.get(emoji_url)
                    
                    if emoji_response.status_code == 200:
                        # Upload emoji
                        encoded_string = base64.b64encode(emoji_response.content).decode('utf-8')
                        image_data = f"data:image/png;base64,{encoded_string}"
                        
                        emoji_payload = {
                            'name': emoji['name'],
                            'image': image_data
                        }
                        
                        create_emoji_response = requests.post(f'https://discord.com/api/v9/guilds/{new_guild_id}/emojis', headers=headers, json=emoji_payload)
                        
                        if create_emoji_response.status_code == 201:
                            emoji_count += 1
                            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Restored emoji: {Fore.WHITE}{emoji['name']}{getattr(Fore, color)}{Style.RESET_ALL}")
                        else:
                            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to restore emoji {emoji['name']}. Status code: {create_emoji_response.status_code}{Style.RESET_ALL}")
                            # Rate limit check
                            if create_emoji_response.status_code == 429:
                                retry_after = create_emoji_response.json().get('retry_after', 5)
                                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Rate limited. Waiting {retry_after} seconds...{Style.RESET_ALL}")
                                time.sleep(retry_after)
                    else:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to download emoji {emoji['name']}. Status code: {emoji_response.status_code}{Style.RESET_ALL}")
                
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Restored {Fore.WHITE}{emoji_count}{getattr(Fore, color)} emojis{Style.RESET_ALL}")
            
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [+] Server restoration completed successfully!{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] New server ID: {Fore.WHITE}{new_guild_id}{getattr(Fore, color)}{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Note: Some elements like messages, webhooks, and server settings could not be restored due to Discord API limitations.{Style.RESET_ALL}")
            
        except ValueError as e:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
    
    print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
    user_input = input()
    
    # Check if user wants to return to main menu
    if user_input.upper() == 'B':
        return_to_menu()
    else:
        return_to_menu()