import os
import sys
import time
import random
import subprocess
import threading
import concurrent.futures
import json
import requests
import keyboard
from colorama import Fore, Style
from datetime import datetime

# import from utils
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_ipgenerator

def ipgenerator():
    clear()
    print(getattr(Fore, color) + title_ipgenerator + Style.RESET_ALL)
    
    try:
        # Chiedi all'utente se vuole utilizzare un webhook
        webhook = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Webhook? (y/n) > {Style.RESET_ALL}")
        
        # Controlla se l'utente vuole tornare al menu principale
        if webhook.upper() == 'B':
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        webhook_url = None
        if webhook.lower() in ['y', 'yes']:
            webhook_url = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Webhook URL > {Style.RESET_ALL}")
            
            # Controlla se l'utente vuole tornare al menu principale
            if webhook_url.upper() == 'B':
                clear()
                # Esegue nuovamente il file main.py
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
            
            # Verifica webhook
            try:
                test_response = requests.get(webhook_url)
                if test_response.status_code != 200:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid webhook URL{Style.RESET_ALL}")
                    time.sleep(2)
                    ipgenerator()  # Riavvia la funzione
                    return
            except:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid webhook URL{Style.RESET_ALL}")
                time.sleep(2)
                ipgenerator()  # Riavvia la funzione
                return
        
        # Chiedi il numero di thread
        try:
            threads_number = int(input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Threads Number > {Style.RESET_ALL}"))
            
            # Controlla se l'utente vuole tornare al menu principale
            if str(threads_number).upper() == 'B':
                clear()
                # Esegue nuovamente il file main.py
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
                
            if threads_number <= 0:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid number of threads{Style.RESET_ALL}")
                time.sleep(2)
                ipgenerator()  # Riavvia la funzione
                return
        except ValueError:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Please enter a valid number{Style.RESET_ALL}")
            time.sleep(2)
            ipgenerator()  # Riavvia la funzione
            return
        
        # Funzione per inviare webhook
        def send_webhook(ip, is_valid):
            if webhook_url:
                username_webhook = "IP Generator"
                avatar_webhook = "https://i.imgur.com/5BFecvA.png"
                color_webhook = 65280 if is_valid else 16711680  # Verde se valido, rosso se non valido
                
                embed_content = {
                    'title': 'IP Valid!' if is_valid else 'IP Invalid',
                    'description': f"**IP:**\n```{ip}```",
                    'color': color_webhook,
                    'footer': {
                        "text": username_webhook,
                        "icon_url": avatar_webhook,
                    }
                }
                
                payload = {
                    'embeds': [embed_content],
                    'username': username_webhook,
                    'avatar_url': avatar_webhook
                }

                headers = {'Content-Type': 'application/json'}

                try:
                    requests.post(webhook_url, data=json.dumps(payload), headers=headers)
                except requests.RequestException as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error sending webhook: {str(e)}{Style.RESET_ALL}")
        
        # Contatori per IP validi e non validi
        number_valid = 0
        number_invalid = 0
        
        # Funzione per verificare un IP
        def ip_check():
            nonlocal number_valid, number_invalid
            
            # Genera un IP casuale
            ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            
            try:
                # Ping l'IP per verificare se è raggiungibile
                if sys.platform.startswith("win"):
                    result = subprocess.run(['ping', '-n', '1', '-w', '100', ip], capture_output=True, text=True, timeout=1)
                elif sys.platform.startswith("linux"):
                    result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True, timeout=1)
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Unsupported platform{Style.RESET_ALL}")
                    return
                
                # Verifica il risultato del ping
                if result.returncode == 0:
                    number_valid += 1
                    if webhook_url:
                        send_webhook(ip, True)
                    print(f"{Fore.GREEN}[{get_current_time()}] [+] Logs: {Fore.WHITE}{number_invalid} invalid - {number_valid} valid {Fore.GREEN}Status: {Fore.WHITE}Valid {Fore.GREEN}IP: {Fore.WHITE}{ip}{Style.RESET_ALL}")
                else:
                    number_invalid += 1
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [-] Logs: {Fore.WHITE}{number_invalid} invalid - {number_valid} valid {getattr(Fore, color)}Status: {Fore.WHITE}Invalid {getattr(Fore, color)}IP: {Fore.WHITE}{ip}{Style.RESET_ALL}")
            except Exception as e:
                number_invalid += 1
                print(f"{getattr(Fore, color)}[{get_current_time()}] [-] Logs: {Fore.WHITE}{number_invalid} invalid - {number_valid} valid {getattr(Fore, color)}Status: {Fore.WHITE}Invalid {getattr(Fore, color)}IP: {Fore.WHITE}{ip}{Style.RESET_ALL}")
            
            # Aggiorna il titolo della console
            os.system(f"title IP Generator - Invalid: {number_invalid} - Valid: {number_valid}")
        
        # Funzione principale per eseguire i thread
        def run_threads():
            try:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting IP Generator with {threads_number} threads{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press Ctrl+C or 'B' key to stop and return to menu{Style.RESET_ALL}")
                
                # Variabile per controllare l'esecuzione
                running = True
                
                # Funzione per gestire la pressione del tasto 'B'
                def on_key_press(event):
                    nonlocal running
                    if event.name.upper() == 'B':
                        running = False
                
                # Registra l'handler per il tasto 'B'
                keyboard.on_press(on_key_press)
                
                # Esegui continuamente finché l'utente non interrompe
                while running:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_number) as executor:
                        futures = [executor.submit(ip_check) for _ in range(threads_number)]
                        concurrent.futures.wait(futures, timeout=0.5)  # Timeout breve per controllare running
                
                # Quando l'utente interrompe
                print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] IP Generator stopped{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Total valid IPs: {Fore.WHITE}{number_valid}{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Total invalid IPs: {Fore.WHITE}{number_invalid}{Style.RESET_ALL}")
                
                print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue...{Style.RESET_ALL}")
                input()
                
                clear()
                # Esegue nuovamente il file main.py
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
                
            except KeyboardInterrupt:
                print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] IP Generator stopped{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Total valid IPs: {Fore.WHITE}{number_valid}{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Total invalid IPs: {Fore.WHITE}{number_invalid}{Style.RESET_ALL}")
                
                print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue...{Style.RESET_ALL}")
                input()
                
                clear()
                # Esegue nuovamente il file main.py
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
        
        # Avvia i thread
        run_threads()
                
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