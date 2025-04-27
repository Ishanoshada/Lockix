"""
Lockix - Secure File Encryption Tool
==================================

A secure file encryption and decryption tool for protecting sensitive files using 
AES-256-CBC encryption with PBKDF2 key derivation.

Features
--------
* Industrial-strength encryption using AES-256-CBC
* Advanced key derivation using PBKDF2 with 1M iterations
* Support for 39+ common file formats
* Interactive CLI with colored output 
* Direct command-line interface
* Secure password storage and management
* File integrity verification with HMAC
* Digital watermarking for authenticity
* Cross-platform support (Windows/Linux/Mac)

Usage
-----
Interactive Mode:
    $ lockix --interactive

Command Line Mode:
    $ lockix encrypt -f file.jpg -p password
    $ lockix decrypt -f file.en -p password
    $ lockix passwd -n new_password -p current_password
    $ lockix --reset

Requirements
-----------
* Python 3.6+
* colorama 
* cryptography

Author: Ishan Oshada
Email: ishan.kodithuwakku.official@gmail.com
Version: 0.1.2
License: MIT
Repository: https://github.com/ishanoshada/Lockix
"""
