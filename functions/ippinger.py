import os
import sys
import time
import socket
import concurrent.futures
import threading
import msvcrt
from colorama import Fore, Style
from datetime import datetime

# import from utils
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_ippinger

def ippinger():
    
    clear()
    print(getattr(Fore, color) + title_ippinger + Style.RESET_ALL)
    
    try:
        hostname = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] IP > {Style.RESET_ALL}")
        
        # Controlla se l'utente vuole tornare al menu principale
        if hostname.upper() == 'B':
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        try:
            port_input = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Port (press Enter for default 80) > {Style.RESET_ALL}")
            port = int(port_input) if port_input else 80
            
            bytes_input = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Bytes (press Enter for default 64) > {Style.RESET_ALL}")
            bytes_size = int(bytes_input) if bytes_input else 64
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting IP Pinger...{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press 'B' to stop and return to menu{Style.RESET_ALL}")
            
            # Variabile per controllare se il ping è in esecuzione
            running = True
            
            # Funzione per eseguire il ping
            def ping_ip(hostname, port, bytes_size):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(2)
                        start_time = time.time()
                        sock.connect((hostname, port))
                        data = b'\x00' * bytes_size
                        sock.sendall(data)
                        end_time = time.time()
                        elapsed_time = (end_time - start_time) * 1000
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Hostname: {Fore.WHITE}{hostname}{getattr(Fore, color)} | Time: {Fore.WHITE}{elapsed_time:.2f}ms{getattr(Fore, color)} | Port: {Fore.WHITE}{port}{getattr(Fore, color)} | Bytes: {Fore.WHITE}{bytes_size}{getattr(Fore, color)} | Status: {Fore.GREEN}succeed{Style.RESET_ALL}")
                except:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Hostname: {Fore.WHITE}{hostname}{getattr(Fore, color)} | Time: {Fore.WHITE}0ms{getattr(Fore, color)} | Port: {Fore.WHITE}{port}{getattr(Fore, color)} | Bytes: {Fore.WHITE}{bytes_size}{getattr(Fore, color)} | Status: {Fore.RED}fail{Style.RESET_ALL}")
            
            # Funzione per controllare l'input dell'utente
            def check_for_exit():
                nonlocal running
                while running:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8').upper()
                        if key == 'B':
                            running = False
                            break
                    time.sleep(0.1)
            
            # Avvia il thread per controllare l'input dell'utente
            input_thread = threading.Thread(target=check_for_exit)
            input_thread.daemon = True
            input_thread.start()
            
            # Utilizziamo un approccio più semplice e diretto
            try:
                # Loop principale per il ping
                while running:
                    # Esegui il ping direttamente nel thread principale
                    ping_ip(hostname, port, bytes_size)
                    time.sleep(0.1)
                
                # Quando l'utente preme 'B', il loop termina e arriviamo qui
                print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Pinging stopped, returning to menu...{Style.RESET_ALL}")
                time.sleep(0.5)  # Breve pausa per mostrare il messaggio
                
                # Termina il thread di input
                if input_thread.is_alive():
                    input_thread.join(0.1)
                
                clear()
                # Esegue nuovamente il file main.py
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
                
            except KeyboardInterrupt:
                # Se l'utente usa Ctrl+C, torna comunque subito al menu principale
                running = False
                print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Pinging stopped, returning to menu...{Style.RESET_ALL}")
                time.sleep(0.5)  # Breve pausa per mostrare il messaggio
                
                # Termina il thread di input
                if input_thread.is_alive():
                    input_thread.join(0.1)
                
                clear()
                # Esegue nuovamente il file main.py
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
                        
        except ValueError:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}Please enter valid numbers for port and bytes{getattr(Fore, color)}{Style.RESET_ALL}")
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