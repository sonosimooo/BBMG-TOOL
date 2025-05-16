from colorama import Fore, Style
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
import re
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_usernametracker

def usernametracker():
    clear()
    print(getattr(Fore, color) + title_usernametracker + Style.RESET_ALL)
    
    try:
        # Set up variables
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        headers = {"User-Agent": user_agent}
        number_site = 0
        number_found = 0
        sites_and_urls_found = []
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Selected User-Agent: {Fore.WHITE}{user_agent}{getattr(Fore, color)}{Style.RESET_ALL}")
        target_username = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Username > {Style.RESET_ALL}").lower()
        
        # Check if user wants to return to main menu
        if target_username.upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Searching for username: {Fore.WHITE}{target_username}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Define sites to check
        sites = {
            "Steam": {
                "url": f"https://steamcommunity.com/id/{target_username}",
                "method": "get",
                "verification": "username",
                "except": None
            },
            "Telegram": {
                "url": f"https://t.me/{target_username}",
                "method": "get",
                "verification": "username",
                "except": [f"if you have telegram, you can contact @{target_username} right away.", f"resolve?domain={target_username}", f"telegram: contact @{target_username}"]
            },
            "TikTok": {
                "url": f"https://www.tiktok.com/@{target_username}",
                "method": "get",
                "verification": "username",
                "except": [f"\\u002f@{target_username}\""]
            },
            "Instagram": {
                "url": f"https://www.instagram.com/{target_username}",
                "method": "get",
                "verification": "username",
                "except": None
            },
            "Paypal": {
                "url": f"https://www.paypal.com/paypalme/{target_username}",
                "method": "get",
                "verification": "username",
                "except": [f"slug_name={target_username}", f"\"slug\":\"{target_username}\"", f"2F{target_username}&amp"]
            },
            "GitHub": {
                "url": f"https://github.com/{target_username}",
                "method": "get",
                "verification": "status",
                "except": None
            },
            "Twitter": {
                "url": f"https://twitter.com/{target_username}",
                "method": "get",
                "verification": "status",
                "except": None
            },
            "Facebook": {
                "url": f"https://www.facebook.com/{target_username}",
                "method": "get",
                "verification": "username",
                "except": None
            },
            "YouTube": {
                "url": f"https://www.youtube.com/@{target_username}",
                "method": "get",
                "verification": "username",
                "except": None
            },
            "Twitch": {
                "url": f"https://www.twitch.tv/{target_username}",
                "method": "get",
                "verification": "username",
                "except": None
            },
            "Reddit": {
                "url": f"https://www.reddit.com/user/{target_username}",
                "method": "get",
                "verification": "username",
                "except": None
            },
            "Pinterest": {
                "url": f"https://www.pinterest.com/{target_username}",
                "method": "get",
                "verification": "username",
                "except": [f"[\\\"username\\\",\\\"{target_username}\\\"]"]
            },
            "Snapchat": {
                "url": f"https://www.snapchat.com/add/{target_username}",
                "method": "get",
                "verification": "status",
                "except": None
            },
            "Linktree": {
                "url": f"https://linktr.ee/{target_username}",
                "method": "get",
                "verification": "status",
                "except": None
            }
        }
        
        # Check each site
        for site_name, site_data in sites.items():
            number_site += 1
            try:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Checking {site_name}...{Style.RESET_ALL}")
                
                if site_data["method"] == "get":
                    response = requests.get(site_data["url"], headers=headers, timeout=5)
                    
                    if site_data["verification"] == "status":
                        if response.status_code == 200:
                            if site_data["except"] is not None:
                                content_lower = response.text.lower()
                                found = True
                                for exception in site_data["except"]:
                                    if exception.lower() in content_lower:
                                        found = False
                                        break
                                if found:
                                    number_found += 1
                                    sites_and_urls_found.append((site_name, site_data["url"]))
                                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] {Fore.GREEN}Found on {site_name}: {site_data['url']}{getattr(Fore, color)}{Style.RESET_ALL}")
                            else:
                                number_found += 1
                                sites_and_urls_found.append((site_name, site_data["url"]))
                                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] {Fore.GREEN}Found on {site_name}: {site_data['url']}{getattr(Fore, color)}{Style.RESET_ALL}")
                    
                    elif site_data["verification"] == "username":
                        if target_username.lower() in response.text.lower():
                            if site_data["except"] is not None:
                                content_lower = response.text.lower()
                                found = True
                                for exception in site_data["except"]:
                                    if exception.lower() in content_lower:
                                        found = False
                                        break
                                if found:
                                    number_found += 1
                                    sites_and_urls_found.append((site_name, site_data["url"]))
                                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] {Fore.GREEN}Found on {site_name}: {site_data['url']}{getattr(Fore, color)}{Style.RESET_ALL}")
                            else:
                                number_found += 1
                                sites_and_urls_found.append((site_name, site_data["url"]))
                                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] {Fore.GREEN}Found on {site_name}: {site_data['url']}{getattr(Fore, color)}{Style.RESET_ALL}")
            
            except Exception as e:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [-] {Fore.RED}Error checking {site_name}: {str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Summary
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Search completed!{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Sites checked: {Fore.WHITE}{number_site}{getattr(Fore, color)}{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Profiles found: {Fore.WHITE}{number_found}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        if number_found > 0:
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Summary of profiles found:{Style.RESET_ALL}")
            for site_name, url in sites_and_urls_found:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] {Fore.GREEN}{site_name}: {url}{getattr(Fore, color)}{Style.RESET_ALL}")
        
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
    
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
        user_input = input()
        
        # Check if user wants to return to main menu after an error
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