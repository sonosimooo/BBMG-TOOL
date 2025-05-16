import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import concurrent.futures
from colorama import Fore, Style
from datetime import datetime

# import from utils
from utils.utils import clear, get_current_time, username, color
from utils.titles import phishing_attack

def phishingattack():
    clear()
    print(getattr(Fore, color) + phishing_attack + Style.RESET_ALL)
    
    try:
        # Crea la directory di output se non esiste
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "phishing")
        os.makedirs(output_dir, exist_ok=True)
        
        # User agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        headers = {"User-Agent": user_agent}
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Selected User-Agent: {Fore.WHITE}{user_agent}{Style.RESET_ALL}")
        website_url = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Website Url > {Style.RESET_ALL}")
        
        # Controlla se l'utente vuole tornare al menu principale
        if website_url.upper() == 'B':
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Aggiungi https:// se non presente
        if "https://" not in website_url and "http://" not in website_url:
            website_url = "https://" + website_url
        
        # Funzione per recuperare CSS e JS
        def css_and_js(html_content, base_url):
            soup = BeautifulSoup(html_content, 'html.parser')

            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] CSS recovery...{Style.RESET_ALL}")
            css_links = soup.find_all('link', rel='stylesheet')
            all_css = []
            css_urls = [urljoin(base_url, link['href']) for link in css_links if 'href' in link.attrs]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                css_futures = {executor.submit(requests.get, url, headers=headers, timeout=5): url for url in css_urls}
                for future in concurrent.futures.as_completed(css_futures):
                    try:
                        css_response = future.result()
                        if css_response.status_code == 200:
                            all_css.append(css_response.text)
                        else:
                            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error retrieving CSS: {css_response.status_code}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error retrieving CSS: {str(e)}{Style.RESET_ALL}")
            
            if all_css:
                style_tag = soup.new_tag('style')
                style_tag.string = "\n".join(all_css)
                if soup.head:
                    soup.head.append(style_tag)
                for link in css_links:
                    link.decompose()

            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Javascript recovery...{Style.RESET_ALL}")
            script_links = soup.find_all('script', src=True)
            all_js = []
            js_urls = [urljoin(base_url, script['src']) for script in script_links if 'src' in script.attrs]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                js_futures = {executor.submit(requests.get, url, headers=headers, timeout=5): url for url in js_urls}
                for future in concurrent.futures.as_completed(js_futures):
                    try:
                        js_response = future.result()
                        if js_response.status_code == 200:
                            all_js.append(js_response.text)
                        else:
                            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error retrieving Javascript: {js_response.status_code}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error retrieving Javascript: {str(e)}{Style.RESET_ALL}")

            if all_js:
                script_tag = soup.new_tag('script')
                script_tag.string = "\n".join(all_js)
                if soup.body:
                    soup.body.append(script_tag)
                for script in script_links:
                    script.decompose()

            # Modifica i form per reindirizzare a una pagina di phishing
            for form in soup.find_all('form'):
                if 'action' in form.attrs:
                    form['action'] = 'phishing_success.html'
                else:
                    form['action'] = 'phishing_success.html'
                form['method'] = 'post'

            return soup.prettify()

        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] HTML recovery...{Style.RESET_ALL}")
        session = requests.Session()
        try:
            response = session.get(website_url, headers=headers, timeout=10)
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                file_name = re.sub(r'[\\/:*?"<>|]', '-', soup.title.string if soup.title else 'Phishing')

                file_html = os.path.join(output_dir, f"{file_name}.html")
                file_html_relative = f'output\\phishing\\{file_name}.html'

                final_html = css_and_js(html_content, website_url)

                # Crea anche una pagina di successo
                success_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Login Successful</title>
                    <meta http-equiv="refresh" content="3;url={website_url}">
                    <style>
                        body {{ font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }}
                        h1 {{ color: green; }}
                    </style>
                </head>
                <body>
                    <h1>Login Successful!</h1>
                    <p>You will be redirected to the original site in a few seconds...</p>
                </body>
                </html>
                """
                
                success_file = os.path.join(output_dir, "phishing_success.html")

                with open(file_html, 'w', encoding='utf-8') as file:
                    file.write(final_html)
                    
                with open(success_file, 'w', encoding='utf-8') as file:
                    file.write(success_html)
                    
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Phishing attack successful. The file is located in the folder: {Fore.WHITE}{file_html_relative}{Style.RESET_ALL}")
                
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
            else:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: Unable to access the website. Status code: {response.status_code}{Style.RESET_ALL}")
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
        except Exception as e:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error accessing the website: {str(e)}{Style.RESET_ALL}")
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