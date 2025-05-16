from colorama import Fore, Style
import os
import sys
import time
from utils.utils import clear, get_current_time, username, color, get_token_from_file
from utils.titles import title_discordtokenlogin

def discordtokenlogin():
    clear()
    print(getattr(Fore, color) + title_discordtokenlogin + Style.RESET_ALL)
    
    try:
        # Check if selenium is installed
        try:
            from selenium import webdriver
        except ImportError:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Selenium module not found!{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Installing selenium...{Style.RESET_ALL}")
            os.system("pip install selenium")
            try:
                from selenium import webdriver
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Selenium installed successfully!{Style.RESET_ALL}")
            except ImportError:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Failed to install selenium. Please install it manually with 'pip install selenium'{Style.RESET_ALL}")
                time.sleep(3)
                clear()
                # Return to main menu
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
        
        # Get Discord token from file or input
        file_token = get_token_from_file()
        if file_token:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Token loaded from file{Style.RESET_ALL}")
            token = file_token
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Token not found in file. Enter your Discord token{Style.RESET_ALL}")
            token = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Token > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if token.upper() == 'B':
                clear()
                # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Browser selection menu
        print(f"""
{getattr(Fore, color)}[{get_current_time()}] [*] Select a browser:
{getattr(Fore, color)}[{get_current_time()}] [1] Chrome (Windows / Linux)
{getattr(Fore, color)}[{get_current_time()}] [2] Edge (Windows)
{getattr(Fore, color)}[{get_current_time()}] [3] Firefox (Windows){Style.RESET_ALL}
        """)
        
        browser = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Browser > {Style.RESET_ALL}")
        
        # Check if user wants to return to main menu
        if browser.upper() == 'B':
            clear()
            # Return to main menu
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
            os.system(f'python "{main_path}"')
            sys.exit()
        
        # Initialize webdriver based on browser selection
        if browser in ['1', '01']:
            try:
                navigator = "Chrome"
                print(f"{getattr(Fore, color)}[{get_current_time()}] [*] {navigator} Starting...{Style.RESET_ALL}")
                
                # Import Chrome-specific modules
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager
                
                # Setup Chrome options
                from selenium.webdriver.chrome.options import Options
                chrome_options = Options()
                chrome_options.add_experimental_option("detach", True)  # Keep browser open
                
                # Initialize Chrome driver
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                print(f"{getattr(Fore, color)}[{get_current_time()}] [+] {navigator} Ready!{Style.RESET_ALL}")
            except Exception as e:
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] {navigator} not installed or driver not up to date.{Style.RESET_ALL}")
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {str(e)}{Style.RESET_ALL}")
                time.sleep(3)
                discordtokenlogin()  # Restart the function
                return
        
        elif browser in ['2', '02']:
            if sys.platform.startswith("linux"):
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Edge is only available on Windows.{Style.RESET_ALL}")
                time.sleep(3)
                discordtokenlogin()  # Restart the function
                return
            else:
                try:
                    navigator = "Edge"
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] {navigator} Starting...{Style.RESET_ALL}")
                    
                    # Import Edge-specific modules
                    from selenium.webdriver.edge.service import Service
                    from webdriver_manager.microsoft import EdgeChromiumDriverManager
                    
                    # Setup Edge options
                    from selenium.webdriver.edge.options import Options
                    edge_options = Options()
                    edge_options.add_experimental_option("detach", True)  # Keep browser open
                    
                    # Initialize Edge driver
                    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] {navigator} Ready!{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] {navigator} not installed or driver not up to date.{Style.RESET_ALL}")
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {str(e)}{Style.RESET_ALL}")
                    time.sleep(3)
                    discordtokenlogin()  # Restart the function
                    return
        
        elif browser in ['3', '03']:
            if sys.platform.startswith("linux"):
                print(f"{getattr(Fore, color)}[{get_current_time()}] [!] This Firefox setup is only available on Windows.{Style.RESET_ALL}")
                time.sleep(3)
                discordtokenlogin()  # Restart the function
                return
            else:
                try:
                    navigator = "Firefox"
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [*] {navigator} Starting...{Style.RESET_ALL}")
                    
                    # Import Firefox-specific modules
                    from selenium.webdriver.firefox.service import Service
                    from webdriver_manager.firefox import GeckoDriverManager
                    
                    # Initialize Firefox driver
                    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [+] {navigator} Ready!{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] {navigator} not installed or driver not up to date.{Style.RESET_ALL}")
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {str(e)}{Style.RESET_ALL}")
                    time.sleep(3)
                    discordtokenlogin()  # Restart the function
                    return
        
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid choice!{Style.RESET_ALL}")
            time.sleep(3)
            discordtokenlogin()  # Restart the function
            return
        
        # Login script for Discord
        try:
            script = """
            function login(token) {
                setInterval(() => {
                    document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                }, 50);
                setTimeout(() => {
                    location.reload();
                }, 2500);
            }
            """
            
            # Navigate to Discord login page
            driver.get("https://discord.com/login")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Token Connection...{Style.RESET_ALL}")
            
            # Execute login script with token
            driver.execute_script(script + f'\nlogin("{token}")')
            time.sleep(4)
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Connected with Token!{Style.RESET_ALL}")
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] If you leave the tool, the browser will remain open.{Style.RESET_ALL}")
            
            # Wait for user input before returning to menu
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
        
        except Exception as e:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error during login: {str(e)}{Style.RESET_ALL}")
            time.sleep(3)
    
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