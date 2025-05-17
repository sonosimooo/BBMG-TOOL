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

versione = '1.0.2'

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
        # GitHub repository info
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

# UPDATE REPOSITORY USING GIT
def update_repository():
    """
    Updates the repository using Git to the latest version.
    Returns a tuple (success, message) where success is a boolean
    and message is a string with information about the update.
    """
    try:
        import subprocess
        
        # Check if git is installed
        try:
            subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (subprocess.SubprocessError, FileNotFoundError):
            return False, "Git is not installed on this system. Please install Git to enable automatic updates."
        
        # Check if the current directory is a git repository
        try:
            subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], 
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.SubprocessError:
            return False, "The current directory is not a Git repository. Cannot perform automatic update."
        
        # Fetch the latest changes
        fetch_process = subprocess.run(['git', 'fetch'], 
                                     check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check if there are changes to pull
        status_process = subprocess.run(['git', 'status', '-uno'], 
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status_output = status_process.stdout.decode('utf-8')
        
        if "Your branch is up to date" in status_output:
            return True, "Repository is already up to date."
        
        # Check for local changes
        diff_process = subprocess.run(['git', 'diff', '--name-only'], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        diff_output = diff_process.stdout.decode('utf-8').strip()
        
        # If there are local changes, try to stash them
        if diff_output:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Local changes detected. Attempting to stash them...{Style.RESET_ALL}")
            stash_process = subprocess.run(['git', 'stash'], 
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if stash_process.returncode != 0:
                stash_error = stash_process.stderr.decode('utf-8')
                return False, f"Failed to stash local changes: {stash_error}"
        
        # Pull the latest changes
        pull_process = subprocess.run(['git', 'pull'], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if pull_process.returncode != 0:
            error_message = pull_process.stderr.decode('utf-8')
            
            # If stashing was done, try to pop the stash
            if diff_output:
                subprocess.run(['git', 'stash', 'pop'], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
            return False, f"Failed to update repository: {error_message}"
        
        # If stashing was done, try to pop the stash
        if diff_output:
            pop_process = subprocess.run(['git', 'stash', 'pop'], 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if pop_process.returncode != 0:
                pop_error = pop_process.stderr.decode('utf-8')
                return True, f"Repository updated, but failed to restore local changes: {pop_error}"
        
        return True, "Repository successfully updated to the latest version."
        
    except Exception as e:
        return False, f"Error updating repository: {str(e)}"


