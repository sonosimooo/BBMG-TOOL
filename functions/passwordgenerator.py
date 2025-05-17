from colorama import Fore, Style
import os
import sys
import time
import random
import string
import pyperclip
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_passwordgenerator

def passwordgenerator():
    clear()
    print(getattr(Fore, color) + title_passwordgenerator + Style.RESET_ALL)
    
    try:
        # Ask for password length
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter the desired password length (8-128 characters){Style.RESET_ALL}")
        length_input = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Length > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if length_input.upper() == 'B':
            return_to_menu()
        
        try:
            length = int(length_input)
            if length < 8 or length > 128:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid length. Using default length of 16 characters.{Style.RESET_ALL}")
                length = 16
        except ValueError:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid input. Using default length of 16 characters.{Style.RESET_ALL}")
            length = 16
        
        # Ask for character types to include
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Include lowercase letters? (Y/N){Style.RESET_ALL}")
        include_lowercase = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}").upper() == 'Y'
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Include uppercase letters? (Y/N){Style.RESET_ALL}")
        include_uppercase = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}").upper() == 'Y'
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Include numbers? (Y/N){Style.RESET_ALL}")
        include_numbers = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}").upper() == 'Y'
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Include special characters? (Y/N){Style.RESET_ALL}")
        include_special = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}").upper() == 'Y'
        
        # Ensure at least one character type is selected
        if not any([include_lowercase, include_uppercase, include_numbers, include_special]):
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] At least one character type must be selected. Including lowercase letters by default.{Style.RESET_ALL}")
            include_lowercase = True
        
        # Ask for excluded characters
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter any characters to exclude (or press Enter to skip){Style.RESET_ALL}")
        excluded_chars = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Exclude > {Style.RESET_ALL}")
        
        # Ask for number of passwords to generate
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] How many passwords do you want to generate? (1-10){Style.RESET_ALL}")
        count_input = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Count > {Style.RESET_ALL}")
        
        try:
            count = int(count_input)
            if count < 1 or count > 10:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid count. Generating 1 password.{Style.RESET_ALL}")
                count = 1
        except ValueError:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid input. Generating 1 password.{Style.RESET_ALL}")
            count = 1
        
        # Generate passwords
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Generating {count} password(s) with length {length}...{Style.RESET_ALL}")
        
        passwords = []
        for i in range(count):
            password = generate_password(
                length, 
                include_lowercase, 
                include_uppercase, 
                include_numbers, 
                include_special, 
                excluded_chars
            )
            passwords.append(password)
        
        # Display generated passwords
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [+] Generated passwords:{Style.RESET_ALL}")
        for i, password in enumerate(passwords, 1):
            print(f"{getattr(Fore, color)}[{get_current_time()}] [{i}] {Fore.WHITE}{password}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Calculate password strength
        if count == 1:
            strength, score = calculate_password_strength(passwords[0])
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [+] Password strength: {get_strength_color(score)}{strength}{getattr(Fore, color)}{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Entropy score: {get_strength_color(score)}{score}/100{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Ask if user wants to copy a password to clipboard
        if count > 1:
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Enter the number of the password to copy to clipboard (or press Enter to skip){Style.RESET_ALL}")
            copy_input = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}")
            
            try:
                copy_index = int(copy_input) - 1
                if 0 <= copy_index < len(passwords):
                    pyperclip.copy(passwords[copy_index])
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Password copied to clipboard!{Style.RESET_ALL}")
                else:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid selection.{Style.RESET_ALL}")
            except ValueError:
                if copy_input:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid input.{Style.RESET_ALL}")
        else:
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Copy password to clipboard? (Y/N){Style.RESET_ALL}")
            copy_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}")
            
            if copy_choice.upper() == 'Y':
                pyperclip.copy(passwords[0])
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Password copied to clipboard!{Style.RESET_ALL}")
        
        # Ask if user wants to save passwords to a file
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Save passwords to a file? (Y/N){Style.RESET_ALL}")
        save_choice = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] > {Style.RESET_ALL}")
        
        if save_choice.upper() == 'Y':
            # Create passwords directory if it doesn't exist
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
            passwords_dir = os.path.join(output_dir, 'passwords')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if not os.path.exists(passwords_dir):
                os.makedirs(passwords_dir)
            
            # Generate filename with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"passwords_{timestamp}.txt"
            filepath = os.path.join(passwords_dir, filename)
            
            # Write passwords to file
            with open(filepath, 'w') as f:
                f.write(f"Generated passwords ({time.strftime('%Y-%m-%d %H:%M:%S')})\n")
                f.write(f"Length: {length}\n")
                f.write(f"Character types: {'lowercase ' if include_lowercase else ''}{'uppercase ' if include_uppercase else ''}{'numbers ' if include_numbers else ''}{'special ' if include_special else ''}\n\n")
                
                for i, password in enumerate(passwords, 1):
                    f.write(f"{i}. {password}\n")
                    
                    if i == 1 and count == 1:
                        strength, score = calculate_password_strength(password)
                        f.write(f"Strength: {strength}\n")
                        f.write(f"Entropy score: {score}/100\n")
            
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Passwords saved to: {Fore.WHITE}{filepath}{getattr(Fore, color)}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
    
    print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue or type 'B' to return to menu...{Style.RESET_ALL}")
    user_input = input()
    
    # Check if user wants to return to main menu
    if user_input.upper() == 'B':
        return_to_menu()
    else:
        return_to_menu()

def generate_password(length, include_lowercase, include_uppercase, include_numbers, include_special, excluded_chars):
    # Define character sets
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    number_chars = string.digits
    special_chars = string.punctuation
    
    # Remove excluded characters from character sets
    if excluded_chars:
        lowercase_chars = ''.join(c for c in lowercase_chars if c not in excluded_chars)
        uppercase_chars = ''.join(c for c in uppercase_chars if c not in excluded_chars)
        number_chars = ''.join(c for c in number_chars if c not in excluded_chars)
        special_chars = ''.join(c for c in special_chars if c not in excluded_chars)
    
    # Create character pool based on selected options
    char_pool = ''
    if include_lowercase:
        char_pool += lowercase_chars
    if include_uppercase:
        char_pool += uppercase_chars
    if include_numbers:
        char_pool += number_chars
    if include_special:
        char_pool += special_chars
    
    # Ensure at least one character from each selected type is included
    password = []
    
    if include_lowercase and lowercase_chars:
        password.append(random.choice(lowercase_chars))
    if include_uppercase and uppercase_chars:
        password.append(random.choice(uppercase_chars))
    if include_numbers and number_chars:
        password.append(random.choice(number_chars))
    if include_special and special_chars:
        password.append(random.choice(special_chars))
    
    # Fill the rest of the password with random characters from the pool
    remaining_length = length - len(password)
    if remaining_length > 0:
        password.extend(random.choices(char_pool, k=remaining_length))
    
    # Shuffle the password to ensure randomness
    random.shuffle(password)
    
    return ''.join(password)

def calculate_password_strength(password):
    # Calculate entropy score (0-100)
    length = len(password)
    has_lowercase = any(c.islower() for c in password)
    has_uppercase = any(c.isupper() for c in password)
    has_numbers = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    char_set_size = 0
    if has_lowercase:
        char_set_size += 26
    if has_uppercase:
        char_set_size += 26
    if has_numbers:
        char_set_size += 10
    if has_special:
        char_set_size += 33  # Approximate number of special characters
    
    # Calculate entropy bits
    if char_set_size > 0:
        entropy_bits = length * (len(password) / 100) * (char_set_size / 95)
    else:
        entropy_bits = 0
    
    # Convert to score out of 100
    score = min(100, int(entropy_bits * 5))
    
    # Determine strength category
    if score < 20:
        strength = "Very Weak"
    elif score < 40:
        strength = "Weak"
    elif score < 60:
        strength = "Moderate"
    elif score < 80:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return strength, score

def get_strength_color(score):
    if score < 20:
        return Fore.RED
    elif score < 40:
        return Fore.YELLOW
    elif score < 60:
        return Fore.YELLOW
    elif score < 80:
        return Fore.GREEN
    else:
        return Fore.LIGHTGREEN_EX

def return_to_menu():
    clear()
    # Return to main menu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
    os.system(f'python "{main_path}"')
    sys.exit()