import os
import sys
import time
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import Fore, Style
from datetime import datetime

# import from utils
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_phone_number_lookup

def phonelookup():
    clear()
    print(getattr(Fore, color) + title_phone_number_lookup + Style.RESET_ALL)
    
    try:
        phone_number = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Phone Number > {Style.RESET_ALL}")
        
        # Controlla se l'utente vuole tornare al menu principale
        if phone_number.upper() == 'B':
            clear()
            # Esegue nuovamente il file main.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Information Recovery...{Style.RESET_ALL}")
        
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed_number):
                status = "Valid"
            else:
                status = "Invalid"

            if phone_number.startswith("+"):
                country_code = "+" + phone_number[1:3] 
            else:
                country_code = "None"
                
            try: 
                operator = carrier.name_for_number(parsed_number, "en")
            except: 
                operator = "None"
        
            try: 
                type_number = "Mobile" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "Landline"
            except: 
                type_number = "None"

            try: 
                timezones = timezone.time_zones_for_number(parsed_number)
                timezone_info = timezones[0] if timezones else "None"
            except: 
                timezone_info = "None"
                
            try: 
                country = phonenumbers.region_code_for_number(parsed_number)
            except: 
                country = "None"
                
            try: 
                region = geocoder.description_for_number(parsed_number, "en")
            except: 
                region = "None"
                
            try: 
                formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            except: 
                formatted_number = "None"
                
            print(f"""
{getattr(Fore, color)}[{get_current_time()}] [+] Phone        : {Fore.WHITE}{phone_number}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Formatted    : {Fore.WHITE}{formatted_number}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Status       : {Fore.WHITE}{status}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Country Code : {Fore.WHITE}{country_code}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Country      : {Fore.WHITE}{country}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Region       : {Fore.WHITE}{region}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Timezone     : {Fore.WHITE}{timezone_info}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Operator     : {Fore.WHITE}{operator}{getattr(Fore, color)}
{getattr(Fore, color)}[{get_current_time()}] [+] Type Number  : {Fore.WHITE}{type_number}{getattr(Fore, color)}
            """)
            
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
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid Format!{Style.RESET_ALL}")
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