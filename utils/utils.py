import os
import sys
import time
import random
import requests
import json
from colorama import Fore, Style
from datetime import datetime, timedelta

# import from options
from utils.options import op1, op2, op3, op4, op5, op6, op7, op8, op9, op10, op11, op13, op14, op15, op16, op17, op18

versione = '1.0.0'

username = os.getlogin()

# Colore predefinito per l'applicazione
color = "LIGHTMAGENTA_EX"


# CLEAR CMD
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# GET CURRENT TIME
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# GET TOKEN FROM FILE
def get_token_from_file():
    """
    Reads Discord token from input/token.txt file.
    Returns the token if file exists and contains a token, otherwise returns None.
    """
    try:
        token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'input', 'token.txt')
        if os.path.exists(token_path):
            with open(token_path, 'r') as file:
                token = file.read().strip()
                if token:
                    return token
        return None
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error reading token file: {str(e)}{Style.RESET_ALL}")
        return None

# CHECK FOR UPDATES
def check_for_updates():
    """
    Checks for updates by comparing local version with the latest version on GitHub.
    Returns a tuple (update_available, latest_version) where update_available is a boolean
    and latest_version is the latest version string.
    """
    try:
        # GitHub repository info (replace with your actual repository)
        repo_owner = "sonosimooo"
        repo_name = "BBMG-TOOL"
        
        # URL for GitHub API to get latest release
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        
        # Make request to GitHub API
        response = requests.get(api_url, timeout=5)
        
        # If request was successful
        if response.status_code == 200:
            # Parse JSON response
            release_info = json.loads(response.text)
            
            # Get latest version (tag_name)
            latest_version = release_info.get('tag_name', '').replace('v', '')
            
            # Compare with current version
            if latest_version and latest_version != versione:
                # Convert versions to tuples of integers for proper comparison
                current_version_parts = [int(x) for x in versione.split('.')]
                latest_version_parts = [int(x) for x in latest_version.split('.')]
                
                # Check if latest version is newer
                if latest_version_parts > current_version_parts:
                    return True, latest_version
            
            return False, latest_version
        
        return False, versione
    
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error checking for updates: {str(e)}{Style.RESET_ALL}")
        return False, versione


