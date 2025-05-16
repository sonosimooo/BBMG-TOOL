from colorama import Fore, Style
import os
import socket
import sys
import threading
import time
import requests
import concurrent.futures
import ssl
import subprocess
from requests.exceptions import RequestException
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_ipscanner

def ipscanner():
    clear()
    print(getattr(Fore, color) + title_ipscanner + Style.RESET_ALL)
    
    def ip_type(ip):
        ip_type = "Unknown"
        if ':' in ip:
            ip_type = "ipv6"
        elif '.' in ip:
            ip_type = "ipv4"
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] IP Type: {Fore.WHITE}{ip_type}{getattr(Fore, color)}{Style.RESET_ALL}")

    def ip_ping(ip):
        try:
            ping_cmd = ['ping', '-n', '1', ip] if sys.platform.startswith("win") else ['ping', '-c', '1', '-W', '1', ip]
            result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=1)
            ping = "Succeed" if result.returncode == 0 else "Fail"
        except Exception:
            ping = "Fail"
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Ping: {Fore.WHITE}{ping}{getattr(Fore, color)}{Style.RESET_ALL}")

    def ip_port(ip):
        port_protocol_map = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP",
            80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP", 194: "IRC", 389: "LDAP",
            443: "HTTPS", 161: "SNMP", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
            1521: "Oracle DB", 3389: "RDP"
        }
        
        def scan_port(ip, port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        protocol = port_protocol_map.get(port, "Unknown")
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Port: {Fore.WHITE}{port}{getattr(Fore, color)} Status: {Fore.WHITE}Open{getattr(Fore, color)} Protocol: {Fore.WHITE}{protocol}{getattr(Fore, color)}{Style.RESET_ALL}")
            except Exception:
                pass
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda port: scan_port(ip, port), port_protocol_map.keys())

    def ip_dns(ip):
        try:
            dns, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
        except Exception:
            dns = "None"
        if dns != "None":
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] DNS: {Fore.WHITE}{dns}{getattr(Fore, color)}{Style.RESET_ALL}")

    def ip_host_info(ip):
        api_url = f"https://ipinfo.io/{ip}/json"
        try:
            response = requests.get(api_url)
            api = response.json()
        except RequestException:
            api = {}

        host_country = api.get('country', 'None')
        if host_country != "None":
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Host Country: {Fore.WHITE}{host_country}{getattr(Fore, color)}{Style.RESET_ALL}")

        host_name = api.get('hostname', 'None')
        if host_name != "None":
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Host Name: {Fore.WHITE}{host_name}{getattr(Fore, color)}{Style.RESET_ALL}")

        host_isp = api.get('org', 'None')
        if host_isp != "None":
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Host ISP: {Fore.WHITE}{host_isp}{getattr(Fore, color)}{Style.RESET_ALL}")

        host_as = api.get('asn', 'None')
        if host_as != "None":
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Host AS: {Fore.WHITE}{host_as}{getattr(Fore, color)}{Style.RESET_ALL}")

    def ssl_certificate_check(ip):
        port = 443
        try:
            with socket.create_connection((ip, port), timeout=1) as sock:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=ip) as ssock:
                    cert = ssock.getpeercert()
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] SSL Certificate: {Fore.WHITE}{cert}{getattr(Fore, color)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] SSL Certificate Check Failed: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")

    try:
        ip = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] IP > {Style.RESET_ALL}")
        
        # Controlla se l'utente vuole tornare al menu principale
        if ip.upper() == 'B':
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
            
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Information Recovery...{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] IP: {Fore.WHITE}{ip}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        ip_type(ip)
        ip_ping(ip)
        ip_dns(ip)
        ip_port(ip)
        ip_host_info(ip)
        ssl_certificate_check(ip)
        
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
        user_input = input()
        
        # Controlla se l'utente vuole tornare al menu principale dopo la scansione
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
        
        # Controlla se l'utente vuole tornare al menu principale dopo un errore
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