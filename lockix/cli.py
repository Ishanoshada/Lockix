import sys
import colorama
from colorama import Fore, Style
import argparse
from .core import encrypt_files, decrypt_files, encrypt_file, decrypt_file
from .config import verify_password, change_password, check_first_run, setup_first_run, reset_password

def colorize():
    """Initialize colorama"""
    colorama.init()

def print_banner():
    """Print the lockix banner."""
    banner = fr"""
    {Fore.CYAN}
                                   <-.(`-')    _       (`-')     
   <-.         .->    _          __( OO)   (_)      (OO )_.-> 
 ,--. )   (`-')----.  \-,-----. '-'. ,--.  ,-(`-')  (_| \_)--.
 |  (`-') ( OO).-.  '  |  .--./ |  .'   /  | ( OO)  \  `.'  / 
 |  |OO ) ( _) | |  | /_) (`-') |      /)  |  |  )   \    .') 
(|  '__ |  \|  |)|  | ||  |OO ) |  .   '  (|  |_/    .'    \  
 |     |'   '  '-'  '(_'  '--'\ |  |\   \  |  |'->  /  .'.  \ 
 `-----'     `-----'    `-----' `--' '--'  `--'    `--'   '--'

    Version: 0.1.1
    Author: Ishan Oshada
    About: A secure file encryption and decryption tool
    {Style.RESET_ALL}"""
    print(banner)

def interactive_mode():
    """Run the tool in interactive mode."""
    colorize()
    print_banner()
    
    # Check if this is the first run
    if check_first_run():
        password = setup_first_run()
    else:
        # If not first run, prompt for password
        password_input = input(f"{Fore.CYAN} PASS :> {Style.RESET_ALL}")
        password = verify_password(password_input)
        if not password:
            print(f"{Fore.RED}Invalid password! Access denied.{Style.RESET_ALL}")
            return
    
    ext_menu = f"""
    {Fore.CYAN}
        1. JPG Files
        2. MP4 Files
        3. PNG Files
        4. PDF Files
        5. DOC/DOCX Files
        6. TXT Files
        7. ZIP Files
        8. MP3 Files
        9. XLS/XLSX Files
        10. PPT/PPTX Files
        11. GIF Files
        12. RAR Files
        13. CSV Files
        14. Change Password
        15. Reset Password
        16. Exit
    {Style.RESET_ALL}"""
    
    action_menu = f"""
    {Fore.CYAN}
        1. Encrypt
        2. Decrypt
        3. Back
    {Style.RESET_ALL}"""
    
    while True:
        print(ext_menu)
        choice = input(f"{Fore.CYAN} \n\t>>>> {Style.RESET_ALL}")
        
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
            ext_map = {
                "1": ("jpg", "en"),
                "2": ("mp4", "en4"),
                "3": ("png", "enp"),
                "4": ("pdf", "epdf"),
                "5": ("doc*", "edoc"),
                "6": ("txt", "etxt"),
                "7": ("zip", "ezip"),
                "8": ("mp3", "em3"),
                "9": ("xls*", "exls"),
                "10": ("ppt*", "eppt"),
                "11": ("gif", "egif"),
                "12": ("rar", "erar"),
                "13": ("csv", "ecsv")
            }
            ext, target_ext = ext_map[choice]
            
            while True:
                print(action_menu)
                action = input(f"{Fore.CYAN} \n\t>>>> {Style.RESET_ALL}")
                
                if action == "1":
                    results = encrypt_files(ext, target_ext, password)
                    for file_path, result in results:
                        print(f"\n\tFile: {file_path} Encrypted -> {result}")
                    break
                    
                elif action == "2":
                    results = decrypt_files(target_ext, password)
                    for file_path, result in results:
                        print(f"\n\tFile: {file_path} Decrypted -> {result}")
                    break
                    
                elif action == "3":
                    break
                    
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        
        elif choice == "14":
            new_pass = input(f"{Fore.CYAN}Enter new password: {Style.RESET_ALL}")
            if not new_pass:
                print(f"{Fore.RED}Password cannot be empty. Try again.{Style.RESET_ALL}")
                continue
            
            confirm = input(f"{Fore.CYAN}Confirm new password: {Style.RESET_ALL}")
            if new_pass != confirm:
                print(f"{Fore.RED}Passwords do not match. Try again.{Style.RESET_ALL}")
                continue
                
            change_password(new_pass)
            password = new_pass  # Update the current session password
        
        elif choice == "15":
            confirm = input(f"{Fore.YELLOW}Are you sure you want to reset your password? (y/n): {Style.RESET_ALL}")
            if confirm.lower() == 'y':
                reset_password()
                print(f"{Fore.YELLOW}You will need to restart the application.{Style.RESET_ALL}")
                break
        
        elif choice == "16" or choice.lower() == "exit":
            print(f"{Fore.YELLOW}Exiting interactive mode...{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break
        
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")





def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='Lockix File Encryption/Decryption Tool')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--reset', action='store_true', help='Reset password')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Encrypt command
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt files')
    encrypt_parser.add_argument('-f', '--file', help='Single file to encrypt')
    encrypt_parser.add_argument('-e', '--extension', help='File extension to encrypt (e.g., jpg, mp4)')
    encrypt_parser.add_argument('-t', '--target', help='Target extension for encrypted files')
    encrypt_parser.add_argument('-p', '--password', required=True, help='Password for authentication')
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt files')
    decrypt_parser.add_argument('-f', '--file', help='Single file to decrypt')
    decrypt_parser.add_argument('-e', '--extension', help='File extension to decrypt (e.g., en, en4)')
    decrypt_parser.add_argument('-p', '--password', required=True, help='Password for authentication')
    
    # Change password command
    passwd_parser = subparsers.add_parser('passwd', help='Change password')
    passwd_parser.add_argument('-n', '--new', required=True, help='New password')
    passwd_parser.add_argument('-p', '--password', required=True, help='Current password')
    
    args = parser.parse_args()
    
    # Reset password if requested
    if args.reset:
        reset_password()
        return
    
    # Default to interactive mode if no arguments provided or explicitly requested
    if len(sys.argv) == 1 or args.interactive:
        interactive_mode()
        return
    
    # Check if this is the first run
    if check_first_run():
        print("First time running lockix. Please run in interactive mode to set up.")
        print("Run: lockix --interactive")
        return
    
    # Authentication check for non-interactive mode
    if not args.password:
        print("Password required. Use -p or --password option.")
        return
    
    password = verify_password(args.password)
    if not password:
        print("Invalid password!")
        return
    
    # Extension mapping
    ext_map = {
        "1": ("jpg", "en"),
        "2": ("mp4", "en4"),
        "3": ("png", "enp"),
        "4": ("pdf", "epdf"),
        "5": ("doc*", "edoc"),
        "6": ("txt", "etxt"),
        "7": ("zip", "ezip"),
        "8": ("mp3", "em3"),
        "9": ("xls*", "exls"),
        "10": ("ppt*", "eppt"),
        "11": ("gif", "egif"),
        "12": ("rar", "erar"),
        "13": ("csv", "ecsv")
    }

    # Process commands
    if args.command == 'encrypt':
        if args.file:
            # Single file encryption
            ext = args.target or 'en'
            result = encrypt_file(args.file, ext, password)
            print(f"File: {args.file} Encrypted -> {result}")
        elif args.extension:
            # Batch encryption
            target = args.target
            if not target:
                # Use mapping to determine target extension
                for _, (ext, target_ext) in ext_map.items():
                    if ext.rstrip('*') == args.extension:
                        target = target_ext
                        break
                target = target or 'en'  # Default to 'en' if no mapping found
            results = encrypt_files(args.extension, target, password)
            for file_path, result in results:
                print(f"File: {file_path} Encrypted -> {result}")
        else:
            print("Error: No file or extension specified for encryption")
    
    elif args.command == 'decrypt':
        if args.file:
            # Single file decryption
            result = decrypt_file(args.file, password)
            print(f"File: {args.file} Decrypted -> {result}")
        elif args.extension:
            # Batch decryption
            results = decrypt_files(args.extension, password)
            for file_path, result in results:
                print(f"File: {file_path} Decrypted -> {result}")
        else:
            print("Error: No file or extension specified for decryption")


    elif args.command == 'passwd':
        if not args.new:
            print("New password required.")
            return
        
        change_password(args.new)


if __name__ == "__main__":
    main()