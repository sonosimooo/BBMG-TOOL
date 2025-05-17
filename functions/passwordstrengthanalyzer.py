from colorama import Fore, Style
import os
import sys
import time
import re
import math
import string
from utils.utils import clear, get_current_time, username, color
from utils.titles import title_passwordstrenghtanalyzer

def passwordstrengthanalyzer():
    clear()
    print(getattr(Fore, color) + title_passwordstrenghtanalyzer + Style.RESET_ALL)
    
    def calculate_entropy(password):
        """
        Calculate password entropy (bits of entropy)
        Higher entropy means more secure password
        """
        # Count character sets used
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_numbers = bool(re.search(r'[0-9]', password))
        has_symbols = bool(re.search(r'[^a-zA-Z0-9]', password))
        
        # Calculate pool size based on character sets used
        pool_size = 0
        if has_lowercase:
            pool_size += 26
        if has_uppercase:
            pool_size += 26
        if has_numbers:
            pool_size += 10
        if has_symbols:
            pool_size += 33  # Approximate number of special characters
        
        # If no characters were found (empty password), set pool_size to 1
        if pool_size == 0:
            pool_size = 1
            
        # Calculate entropy
        entropy = math.log2(pool_size) * len(password) if len(password) > 0 else 0
        return entropy
    
    def check_common_patterns(password):
        """
        Check for common patterns that weaken passwords
        Returns a list of found weaknesses
        """
        weaknesses = []
        
        # Check for sequential characters
        sequential_chars = ['abcdefghijklmnopqrstuvwxyz', '0123456789', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        for seq in sequential_chars:
            for i in range(len(seq) - 2):
                if seq[i:i+3].lower() in password.lower():
                    weaknesses.append(f"Contains sequential characters: '{seq[i:i+3]}'")
                    break
        
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            weaknesses.append("Contains repeated characters (3+ times)")
        
        # Check for keyboard patterns (horizontal)
        keyboard_patterns = ['qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop',
                            'asd', 'sdf', 'dfg', 'fgh', 'ghj', 'hjk', 'jkl',
                            'zxc', 'xcv', 'cvb', 'vbn', 'bnm']
        for pattern in keyboard_patterns:
            if pattern in password.lower():
                weaknesses.append(f"Contains keyboard pattern: '{pattern}'")
                break
        
        # Check for years (common in passwords)
        if re.search(r'19\d\d|20\d\d', password):
            weaknesses.append("Contains a year (19XX or 20XX)")
        
        # Check for common words
        common_words = ['password', 'admin', 'welcome', 'login', 'user', 'guest', 'qwerty', '123456', 'abc123']
        for word in common_words:
            if word in password.lower():
                weaknesses.append(f"Contains common password: '{word}'")
                break
        
        return weaknesses
    
    def analyze_password_strength(password):
        """
        Analyze password strength and return detailed results
        """
        results = {}
        
        # Basic metrics
        results['length'] = len(password)
        results['has_lowercase'] = bool(re.search(r'[a-z]', password))
        results['has_uppercase'] = bool(re.search(r'[A-Z]', password))
        results['has_numbers'] = bool(re.search(r'[0-9]', password))
        results['has_symbols'] = bool(re.search(r'[^a-zA-Z0-9]', password))
        
        # Character distribution
        char_counts = {}
        for char_type, pattern in [
            ('lowercase', r'[a-z]'), 
            ('uppercase', r'[A-Z]'), 
            ('numbers', r'[0-9]'), 
            ('symbols', r'[^a-zA-Z0-9]')
        ]:
            chars = re.findall(pattern, password)
            char_counts[char_type] = len(chars)
        
        results['char_counts'] = char_counts
        
        # Calculate entropy
        results['entropy'] = calculate_entropy(password)
        
        # Check for common patterns
        results['weaknesses'] = check_common_patterns(password)
        
        # Determine strength rating
        if results['entropy'] < 28:
            results['strength'] = 'Very Weak'
            results['color'] = 'RED'
        elif results['entropy'] < 36:
            results['strength'] = 'Weak'
            results['color'] = 'YELLOW'
        elif results['entropy'] < 60:
            results['strength'] = 'Moderate'
            results['color'] = 'BLUE'
        elif results['entropy'] < 80:
            results['strength'] = 'Strong'
            results['color'] = 'GREEN'
        else:
            results['strength'] = 'Very Strong'
            results['color'] = 'LIGHTGREEN_EX'
        
        # Estimate crack time (very rough approximation)
        # Assuming 10 billion guesses per second (high-end attacker)
        if results['entropy'] > 0:
            combinations = 2 ** results['entropy']
            seconds = combinations / (10 * 10**9)
            
            # Convert to human-readable time
            if seconds < 60:
                results['crack_time'] = f"{seconds:.2f} seconds"
            elif seconds < 3600:
                results['crack_time'] = f"{seconds/60:.2f} minutes"
            elif seconds < 86400:
                results['crack_time'] = f"{seconds/3600:.2f} hours"
            elif seconds < 31536000:
                results['crack_time'] = f"{seconds/86400:.2f} days"
            elif seconds < 31536000 * 100:
                results['crack_time'] = f"{seconds/31536000:.2f} years"
            else:
                results['crack_time'] = "centuries"
        else:
            results['crack_time'] = "instant"
        
        return results
    
    def generate_password_suggestions(analysis):
        """
        Generate suggestions to improve password strength
        """
        suggestions = []
        
        # Suggest longer password if too short
        if analysis['length'] < 12:
            suggestions.append("Increase password length to at least 12 characters")
        
        # Suggest adding missing character types
        if not analysis['has_lowercase']:
            suggestions.append("Add lowercase letters (a-z)")
        if not analysis['has_uppercase']:
            suggestions.append("Add uppercase letters (A-Z)")
        if not analysis['has_numbers']:
            suggestions.append("Add numbers (0-9)")
        if not analysis['has_symbols']:
            suggestions.append("Add special characters (!@#$%^&*)")
        
        # Suggest better character distribution
        total_chars = sum(analysis['char_counts'].values())
        if total_chars > 0:
            for char_type, count in analysis['char_counts'].items():
                percentage = (count / total_chars) * 100
                if percentage > 70:
                    suggestions.append(f"Reduce reliance on {char_type} (currently {percentage:.1f}% of password)")
        
        # Suggest fixing weaknesses
        if analysis['weaknesses']:
            suggestions.append("Avoid common patterns found in your password:")
            for weakness in analysis['weaknesses']:
                suggestions.append(f"  - {weakness}")
        
        # General suggestions for stronger passwords
        if analysis['strength'] in ['Very Weak', 'Weak', 'Moderate']:
            suggestions.append("Consider using a passphrase (multiple random words)")
            suggestions.append("Use a password manager to generate and store complex passwords")
        
        return suggestions
    
    try:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Enter a password to analyze its strength{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Note: The password is not stored or transmitted{Style.RESET_ALL}")
        password = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Password > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if password.upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Analyzing password strength...{Style.RESET_ALL}")
        
        # Analyze password
        analysis = analyze_password_strength(password)
        
        # Display results
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [+] Password Length: {Fore.WHITE}{analysis['length']} characters{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Character composition
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Character Composition:{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}    - Lowercase Letters: {Fore.WHITE}{analysis['char_counts']['lowercase']}{getattr(Fore, color)}{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}    - Uppercase Letters: {Fore.WHITE}{analysis['char_counts']['uppercase']}{getattr(Fore, color)}{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}    - Numbers: {Fore.WHITE}{analysis['char_counts']['numbers']}{getattr(Fore, color)}{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}    - Special Characters: {Fore.WHITE}{analysis['char_counts']['symbols']}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Entropy
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Entropy: {Fore.WHITE}{analysis['entropy']:.2f} bits{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Strength rating
        strength_color = getattr(Fore, analysis['color'])
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Strength Rating: {strength_color}{analysis['strength']}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Estimated crack time
        print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Estimated Time to Crack: {Fore.WHITE}{analysis['crack_time']}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Weaknesses
        if analysis['weaknesses']:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Weaknesses Detected:{Style.RESET_ALL}")
            for weakness in analysis['weaknesses']:
                print(f"{getattr(Fore, color)}    - {Fore.YELLOW}{weakness}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Suggestions
        suggestions = generate_password_suggestions(analysis)
        if suggestions:
            print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Suggestions to Improve:{Style.RESET_ALL}")
            for suggestion in suggestions:
                print(f"{getattr(Fore, color)}    - {Fore.CYAN}{suggestion}{getattr(Fore, color)}{Style.RESET_ALL}")
        
        # Visual strength meter
        print(f"\n{getattr(Fore, color)}[{get_current_time()}] [+] Strength Meter:{Style.RESET_ALL}")
        meter_length = 30
        filled_length = int(min(analysis['entropy'], 100) / 100 * meter_length)
        
        if analysis['strength'] == 'Very Weak':
            meter_color = Fore.RED
        elif analysis['strength'] == 'Weak':
            meter_color = Fore.YELLOW
        elif analysis['strength'] == 'Moderate':
            meter_color = Fore.BLUE
        elif analysis['strength'] == 'Strong':
            meter_color = Fore.GREEN
        else:
            meter_color = Fore.LIGHTGREEN_EX
        
        meter = f"{meter_color}{'█' * filled_length}{Fore.WHITE}{'░' * (meter_length - filled_length)}{getattr(Fore, color)}"
        print(f"{getattr(Fore, color)}    {meter}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{getattr(Fore, color)}{Style.RESET_ALL}")
    
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