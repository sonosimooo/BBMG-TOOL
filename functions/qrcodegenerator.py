from colorama import Fore, Style
import os
import sys
import time
import qrcode
from PIL import Image
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_qrcodegenerator

def qrcodegenerator():
    clear()
    print(getattr(Fore, color) + title_qrcodegenerator + Style.RESET_ALL)
    
    try:
        # Create QR codes directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        qrcodes_dir = os.path.join(output_dir, 'qrcodes')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if not os.path.exists(qrcodes_dir):
            os.makedirs(qrcodes_dir)
        
        # Ask for QR code type
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Select QR code type:{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [1] URL{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [2] Text{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [3] Email{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [4] Phone number{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [5] WiFi credentials{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [6] vCard (Contact information){Style.RESET_ALL}")
        
        qr_type = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Type > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if qr_type.upper() == 'B':
            return_to_menu()
        
        # Get content based on QR code type
        content = ""
        filename_prefix = ""
        
        if qr_type == '1':  # URL
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter the URL (e.g., https://example.com):{Style.RESET_ALL}")
            url = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] URL > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if url.upper() == 'B':
                return_to_menu()
            
            # Add https:// if not present and not another protocol
            if not (url.startswith('http://') or url.startswith('https://') or url.startswith('ftp://')):
                url = 'https://' + url
            
            content = url
            filename_prefix = "url"
        
        elif qr_type == '2':  # Text
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter the text:{Style.RESET_ALL}")
            text = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Text > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if text.upper() == 'B':
                return_to_menu()
            
            content = text
            filename_prefix = "text"
        
        elif qr_type == '3':  # Email
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter email address:{Style.RESET_ALL}")
            email = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Email > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if email.upper() == 'B':
                return_to_menu()
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter subject (optional):{Style.RESET_ALL}")
            subject = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Subject > {Style.RESET_ALL}")
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter body (optional):{Style.RESET_ALL}")
            body = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Body > {Style.RESET_ALL}")
            
            # Format as mailto link
            content = f"mailto:{email}"
            if subject or body:
                content += "?"
                if subject:
                    content += f"subject={subject}"
                    if body:
                        content += "&"
                if body:
                    content += f"body={body}"
            
            filename_prefix = "email"
        
        elif qr_type == '4':  # Phone number
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter phone number (with country code, e.g., +1234567890):{Style.RESET_ALL}")
            phone = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Phone > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if phone.upper() == 'B':
                return_to_menu()
            
            # Format as tel link
            content = f"tel:{phone}"
            filename_prefix = "phone"
        
        elif qr_type == '5':  # WiFi credentials
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter WiFi network name (SSID):{Style.RESET_ALL}")
            ssid = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] SSID > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if ssid.upper() == 'B':
                return_to_menu()
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter WiFi password:{Style.RESET_ALL}")
            password = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Password > {Style.RESET_ALL}")
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Select encryption type:{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [1] WPA/WPA2{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [2] WEP{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [3] None (Open){Style.RESET_ALL}")
            
            encryption_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Encryption > {Style.RESET_ALL}")
            
            if encryption_choice == '1':
                encryption = "WPA"
            elif encryption_choice == '2':
                encryption = "WEP"
            else:
                encryption = "nopass"
            
            # Format WiFi string
            if encryption == "nopass":
                content = f"WIFI:S:{ssid};T:{encryption};;"
            else:
                content = f"WIFI:S:{ssid};T:{encryption};P:{password};;"
            
            filename_prefix = "wifi"
        
        elif qr_type == '6':  # vCard
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter full name:{Style.RESET_ALL}")
            name = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Name > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if name.upper() == 'B':
                return_to_menu()
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter phone number (optional):{Style.RESET_ALL}")
            phone = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Phone > {Style.RESET_ALL}")
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter email (optional):{Style.RESET_ALL}")
            email = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Email > {Style.RESET_ALL}")
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter organization (optional):{Style.RESET_ALL}")
            org = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Organization > {Style.RESET_ALL}")
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter address (optional):{Style.RESET_ALL}")
            address = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Address > {Style.RESET_ALL}")
            
            # Format vCard
            vcard = ["BEGIN:VCARD", "VERSION:3.0"]
            vcard.append(f"FN:{name}")
            
            # Split name into parts (assuming format: First Last)
            name_parts = name.split()
            if len(name_parts) > 1:
                vcard.append(f"N:{name_parts[-1]};{' '.join(name_parts[:-1])}")
            else:
                vcard.append(f"N:{name}")
            
            if phone:
                vcard.append(f"TEL:{phone}")
            if email:
                vcard.append(f"EMAIL:{email}")
            if org:
                vcard.append(f"ORG:{org}")
            if address:
                vcard.append(f"ADR:{address}")
            
            vcard.append("END:VCARD")
            content = "\n".join(vcard)
            filename_prefix = "contact"
        
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid option. Using text QR code.{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter the text:{Style.RESET_ALL}")
            text = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Text > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if text.upper() == 'B':
                return_to_menu()
            
            content = text
            filename_prefix = "text"
        
        # Ask for QR code customization
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Customize QR code? (Y/N){Style.RESET_ALL}")
        customize = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}").upper() == 'Y'
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        
        qr.add_data(content)
        qr.make(fit=True)
        
        if customize:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Select fill color:{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [1] Black (default){Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [2] Blue{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [3] Red{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [4] Green{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [5] Purple{Style.RESET_ALL}")
            
            fill_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Fill color > {Style.RESET_ALL}")
            
            if fill_choice == '2':
                fill_color = 'blue'
            elif fill_choice == '3':
                fill_color = 'red'
            elif fill_choice == '4':
                fill_color = 'green'
            elif fill_choice == '5':
                fill_color = 'purple'
            else:
                fill_color = 'black'
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Select background color:{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [1] White (default){Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [2] Light Blue{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [3] Light Yellow{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [4] Light Green{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [5] Light Pink{Style.RESET_ALL}")
            
            bg_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Background color > {Style.RESET_ALL}")
            
            if bg_choice == '2':
                back_color = 'lightblue'
            elif bg_choice == '3':
                back_color = 'lightyellow'
            elif bg_choice == '4':
                back_color = 'lightgreen'
            elif bg_choice == '5':
                back_color = 'lightpink'
            else:
                back_color = 'white'
            
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
        else:
            img = qr.make_image(fill_color="black", back_color="white")
        
        # Generate filename with timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.png"
        filepath = os.path.join(qrcodes_dir, filename)
        
        # Save QR code
        img.save(filepath)
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] QR code generated successfully!{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Saved to: {Fore.WHITE}{filepath}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Ask if user wants to open the QR code
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Open QR code now? (Y/N){Style.RESET_ALL}")
        open_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}")
        
        if open_choice.upper() == 'Y':
            try:
                os.startfile(filepath)
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] QR code opened in default image viewer.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Could not open QR code: {str(e)}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
    
    print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
    user_input = input()
    
    # Check if user wants to return to main menu
    if user_input.upper() == 'B':
        return_to_menu()
    else:
        return_to_menu()

def return_to_menu():
    clear()
    # Return to main menu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
    os.system(f'python "{main_path}"')
    sys.exit()