import os
import sys
import time
import requests
from colorama import Fore, Style
from datetime import datetime

# import from utils
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_emailtracker

def emailtracker():
    clear()
    print(getattr(Fore, color) + title_emailtracker + Style.RESET_ALL)
    
    try:
        email = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Email > {Style.RESET_ALL}")
        
        # Controlla se l'utente vuole tornare al menu principale
        if email.upper() == 'B':
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Checking email: {Fore.WHITE}{email}{Style.RESET_ALL}")
        
        # Funzioni per verificare l'email su vari servizi
        def check_instagram(email):
            try:
                session = requests.Session()
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Origin': 'https://www.instagram.com',
                    'Connection': 'keep-alive',
                    'Referer': 'https://www.instagram.com/'
                }

                data = {"email": email}

                response = session.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
                if response.status_code != 200:
                    return f"Error: {response.status_code}"

                token = session.cookies.get('csrftoken')
                if not token:
                    return "Error: Token Not Found."

                headers["x-csrftoken"] = token
                headers["Referer"] = "https://www.instagram.com/accounts/emailsignup/"

                response = session.post(
                    url="https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
                    headers=headers,
                    data=data
                )
                if response.status_code == 200:
                    if "Another account is using the same email." in response.text or "email_is_taken" in response.text:
                        return True
                    return False
                return f"Error: {response.status_code}"
            except Exception as e:
                return f"Error: {e}"

        def check_twitter(email):
            try:
                session = requests.Session()
                response = session.get(
                    url="https://api.twitter.com/i/users/email_available.json",
                    params={"email": email}
                )
                if response.status_code == 200:
                    return response.json()["taken"]
                return f"Error: {response.status_code}"
            except Exception as e:
                return f"Error: {e}"

        def check_spotify(email):
            try:
                session = requests.Session()
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                }
                
                params = {'validate': '1', 'email': email}
                response = session.get('https://spclient.wg.spotify.com/signup/public/v1/account',
                        headers=headers,
                        params=params)
                if response.status_code == 200:
                    status = response.json()["status"]
                    return status == 20
                return f"Error: {response.status_code}"
            except Exception as e:
                return f"Error: {e}"
        
        # Esegui i controlli
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Checking services...{Style.RESET_ALL}")
        
        # Instagram
        instagram_result = check_instagram(email)
        if isinstance(instagram_result, bool):
            if instagram_result:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Instagram: {Fore.GREEN}Account found{Style.RESET_ALL}")
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [-] Instagram: {Fore.RED}No account found{Style.RESET_ALL}")
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Instagram: {Fore.YELLOW}{instagram_result}{Style.RESET_ALL}")
        
        # Twitter
        twitter_result = check_twitter(email)
        if isinstance(twitter_result, bool):
            if twitter_result:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Twitter: {Fore.GREEN}Account found{Style.RESET_ALL}")
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [-] Twitter: {Fore.RED}No account found{Style.RESET_ALL}")
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Twitter: {Fore.YELLOW}{twitter_result}{Style.RESET_ALL}")
        
        # Spotify
        spotify_result = check_spotify(email)
        if isinstance(spotify_result, bool):
            if spotify_result:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Spotify: {Fore.GREEN}Account found{Style.RESET_ALL}")
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [-] Spotify: {Fore.RED}No account found{Style.RESET_ALL}")
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Spotify: {Fore.YELLOW}{spotify_result}{Style.RESET_ALL}")
        
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Email check completed{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
        user_input = input()
        
        if user_input.upper() == 'B':
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        else:
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
            
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
        user_input = input()
        
        if user_input.upper() == 'B':
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        else:
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()