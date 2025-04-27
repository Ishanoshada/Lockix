import sys
import colorama
from colorama import Fore, Style
import argparse
from .core import encrypt_files, decrypt_files, encrypt_file, decrypt_file
from .config import verify_password, change_password, check_first_run, setup_first_run, reset_password
import shutil
import subprocess


ext_map = {
    "1": ("jpg", "ejpg"),
    "2": ("mp4", "emp4"),
    "3": ("png", "epng"),
    "4": ("pdf", "epdf"),
    "5": ("doc*", "edoc"),
    "6": ("txt", "etxt"),
    "7": ("zip", "ezip"),
    "8": ("mp3", "emp3"),
    "9": ("xls*", "exls"),
    "10": ("ppt*", "eppt"),
    "11": ("gif", "egif"),
    "12": ("rar", "erar"),
    "13": ("csv", "ecsv"),
    "14": ("wav", "ewav"),
    "15": ("psd", "epsd"),
    "16": ("svg", "esvg"),
    "17": ("json", "ejsn"),
    "18": ("xml", "exml"),
    "19": ("html", "ehtm"),
    "20": ("avi", "eavi"),
    "21": ("mkv", "emkv"),
    "22": ("iso", "eiso"),
    "23": ("exe", "eexe"),
    "24": ("bmp", "ebmp"),
    "25": ("7z", "e7z"),
    "26": ("py", "epy"),
    "27": ("env", "eenv"),
    "28": ("js", "ejs"),
    "29": ("go", "ego"),
    "30": ("cpp", "ecpp"),
    "31": ("cs", "ecs"),
    "32": ("java", "ejva"),
    "33": ("rb", "erb"),
    "34": ("php", "ephp"),
    "35": ("sql", "esql"),
    "36": ("jar", "ejar"),
    "37": ("apk", "eapk"),
    "38": ("md", "emd"),
    "39": ("ini", "eini"),
    "40": ("cfg", "ecfg"),
    "41": ("log", "elog"),
    "42": ("dat", "edat")
}


def colorize():
    """Initialize colorama"""
    colorama.init()

def print_banner():
    """Print the lockix banner."""
    
    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns
    
    banner = fr"""
    {Fore.CYAN}
                                   <-.(`-')    _       (`-')     
   <-.         .->    _          __( OO)   (_)      (OO )_.-> 
 ,--. )   (`-')----.  \-,-----. '-'. ,--.  ,-(`-')  (_| \_)--.
 |  (`-') ( OO).-.  '  |  .--./ |  .'   /  | ( OO)  \  `.'  / 
 |  |OO ) ( _) | |  | /_) (`-') |      /)  |  |  )   \    .') 
(|  '__ |  \|  |)|  | ||  |OO ) |  .   '  (|  |_/    .'    \  
 |     |'   '  '-'  '(_'  '--'\ |  |\   \  |  |'->  /  .'.  \ 
 `-----'     `-----'    `-----' `--' '--'  `--'    `--'   '--'"""
    
    info = f"""
    Version: 0.1.2
    Author: Ishan Oshada
    About: A secure file encryption and decryption tool
    {Style.RESET_ALL}"""
    
    # Center each line
    centered_banner = '\n'.join(line.center(terminal_width) for line in banner.splitlines())
    centered_info = '\n'.join(line.center(terminal_width) for line in info.splitlines())
    
    print(centered_banner)
    print(centered_info)

def interactive_mode():
    global ext_map
    """Run the tool in interactive mode."""
    colorize()
    print_banner()
    
    # Check if this is the first run
    if check_first_run():
        password = setup_first_run()
    else:
        # If not first run, prompt for password
        password_input = input(f"{Fore.CYAN}\t\t PASS :> {Style.RESET_ALL}")
        password = verify_password(password_input)
        if not password:
            print(f"{Fore.RED}Invalid password! Access denied.{Style.RESET_ALL}")
            return
    # Dynamically create menu items
    items_per_page = 20
    current_page = 1
    
    def create_menu(page):
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        menu_items = []
        
        for k, (ext, _) in list(ext_map.items())[start_idx:end_idx]:
            menu_items.append(f"{k}. {ext.upper().replace('*', '/X')} Files\n")
        
        last_num = max(int(k) for k in ext_map.keys())
        
        if page * items_per_page < len(ext_map):
            menu_items.append(f"N. Next Page\n")
        if page > 1:
            menu_items.append(f"P. Previous Page\n")
            
        menu_items.extend([
            f"{last_num + 1}. Change Password\n",
            f"{last_num + 2}. Reset Password\n",
            f"{last_num + 3}/0. Exit"
        ])
        
        return f"""
    {Fore.CYAN}
        {"        ".join(menu_items)}
    {Style.RESET_ALL}"""
    
    action_menu = f"""
    {Fore.CYAN}
        1. Encrypt
        2. Decrypt
        3. Back
    {Style.RESET_ALL}"""
    
    while True:
        ext_menu = create_menu(current_page)
        print(ext_menu)
        choice = input(f"{Fore.CYAN} \n\t>>>> {Style.RESET_ALL}").upper()
        
        if choice == 'N' and current_page * items_per_page < len(ext_map):
            current_page += 1
            continue
        elif choice == 'P' and current_page > 1:
            current_page -= 1
            continue
        
        if choice in ext_map:
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
        
        elif choice == str(max(int(k) for k in ext_map.keys()) + 1):
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
        
        elif choice == str(max(int(k) for k in ext_map.keys()) + 2):
            confirm = input(f"{Fore.YELLOW}Are you sure you want to reset your password? (y/n): {Style.RESET_ALL}")
            if confirm.lower() == 'y':
                reset_password()
                print(f"{Fore.YELLOW}You will need to restart the application.{Style.RESET_ALL}")
                break
        
        elif choice == str(max(int(k) for k in ext_map.keys()) + 3) or choice.lower() == "exit" or choice == "0":
            print(f"{Fore.YELLOW}Exiting interactive mode...{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break
        
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")


def update_package():
    """Update the package using pip."""
    try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "lockix"])
                    print(f"{Fore.GREEN}Successfully updated lockix to the latest version{Style.RESET_ALL}")
    except subprocess.CalledProcessError:
                    print(f"{Fore.RED}Failed to update lockix{Style.RESET_ALL}")


def main():
    global ext_map
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Lockix - Secure File Encryption/Decryption Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive Mode:
    lockix --interactive
    
  Encrypt a file:
    lockix encrypt -f document.pdf -p mypassword
    
  Decrypt a file:
    lockix decrypt -f document.epdf -p mypassword
    
  Change password:
    lockix passwd -n newpass -p currentpass
    
  Reset password:
    lockix --reset

  Update package:
    lockix --update
        """
    )
    
    # Add version flag
    parser.add_argument('--version', action='version', version='Lockix v0.1.2')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive GUI mode')
    parser.add_argument('--reset', action='store_true', help='Reset password and start fresh')
    parser.add_argument('--update', action='store_true', help='Update the package to the latest version')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt files')
    encrypt_parser.add_argument('-f', '--file', help='Single file to encrypt')
    encrypt_parser.add_argument('-e', '--extension', help='File extension to encrypt (e.g., jpg, pdf, doc)')
    encrypt_parser.add_argument('-t', '--target', help='Target extension for encrypted files')
    encrypt_parser.add_argument('-p', '--password', required=True, help='Password for encryption')
    
    # Decrypt command  
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt files')
    decrypt_parser.add_argument('-f', '--file', help='Single file to decrypt')
    decrypt_parser.add_argument('-e', '--extension', help='File extension to decrypt (e.g., ejpg, epdf)')
    decrypt_parser.add_argument('-p', '--password', required=True, help='Password for decryption')

    # Password management
    passwd_parser = subparsers.add_parser('passwd', help='Change encryption password')
    passwd_parser.add_argument('-n', '--new', required=True, help='New password to set')
    passwd_parser.add_argument('-p', '--password', required=True, help='Current password')

    args = parser.parse_args()
    
    # Reset password if requested
    if args.reset:
        reset_password()
        return
    
    if args.update:
        update_package()
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