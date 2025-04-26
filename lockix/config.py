import os
import hashlib
import json
import sys
from colorama import Fore, Style, init

CONFIG_DIR = os.path.expanduser("~/.lockix")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def hash_password(password):
    """Create a SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_first_run():
    """Check if this is the first run of the application."""
    return not os.path.exists(CONFIG_FILE)

def setup_first_run():
    """Setup first run - create config directory and prompt for password."""
    init()  # Initialize colorama
    
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    print(f"{Fore.CYAN}First time running lockix. You need to set up a password.{Style.RESET_ALL}")
    
    while True:
        password = input(f"{Fore.CYAN}Enter new password: {Style.RESET_ALL}")
        
        if not password:
            print(f"{Fore.RED}Password cannot be empty. Try again.{Style.RESET_ALL}")
            continue
        
        confirm = input(f"{Fore.CYAN}Confirm password: {Style.RESET_ALL}")
        
        if password != confirm:
            print(f"{Fore.RED}Passwords do not match. Try again.{Style.RESET_ALL}")
            continue
        
        config = {
            "password_hash": hash_password(password)
        }
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        
        print(f"{Fore.GREEN}Password set successfully!{Style.RESET_ALL}")
        return password  # Return the plaintext password for encryption use
    
def verify_password(password):
    """Verify the password against the stored hash."""
    # If this is the first run, set up the password
    if check_first_run():
        return setup_first_run()
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        if hash_password(password) == config["password_hash"]:
            return password  # Return the plaintext password for encryption use
        else:
            return False
    except Exception as e:
        print(f"{Fore.RED}Error verifying password: {e}{Style.RESET_ALL}")
        return False

def change_password(new_password):
    """Change the password in the config file."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    if not new_password:
        print(f"{Fore.RED}Password cannot be empty. Password not changed.{Style.RESET_ALL}")
        return False
    
    config = {"password_hash": hash_password(new_password)}
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    
    print(f"{Fore.GREEN}Password changed successfully!{Style.RESET_ALL}")
    return True

def reset_password():
    """Reset the password by deleting the config file."""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print(f"{Fore.GREEN}Password reset. You will be prompted for a new password on next run.{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.YELLOW}No password file found. Nothing to reset.{Style.RESET_ALL}")
        return False