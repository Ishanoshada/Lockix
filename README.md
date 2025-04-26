# Lockix - Secure File Encryption Tool

[![PyPI version](https://badge.fury.io/py/lockix.svg)](https://badge.fury.io/py/lockix)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A secure file encryption and decryption tool for protecting your sensitive files using AES-256-CBC encryption.

## Features

- AES-256-CBC encryption with PBKDF2 key derivation
- Supports multiple file formats (JPG, MP4, PNG, PDF, DOC, TXT, etc.)
- Interactive and command-line interface modes
- Secure password management system
- File watermarking for authenticity
- Easy-to-use interface with colorful output

## Installation

```bash
pip install lockix
```

## Usage

### Interactive Mode

```bash
lockix --interactive
```

### Command Line Mode

Encrypt a single file:
```bash
lockix encrypt -f file.jpg -p your_password
```

Decrypt a single file:
```bash
lockix decrypt -f file.en -p your_password
```

Change password:
```bash
lockix passwd -n new_password
```

Reset password:
```bash
lockix --reset
```

## Supported File Types

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

## Security Features

- AES-256-CBC encryption
- PBKDF2 key derivation
- Secure password hashing
- File watermarking
- Salt-based encryption



## Usage

### Interactive Mode

```bash
lockix --interactive
```

Follow the menu prompts:
1. Enter your password
2. Select file type (1-13)
3. Choose encrypt/decrypt operation
4. Input file path when prompted

Example interactive session:
```bash
lockix

# Enter password when prompted
PASS :> mypassword

# Select file type (1-13)
>>>> 1

# Choose operation
1. Encrypt
2. Decrypt
3. Back
>>>> 1

# Enter file path
File: test.jpg Encrypted -> .\746573742e6a7067_.en
```


## Requirements

- Python 3.6+
- colorama
- cryptography

## License

MIT License - see LICENSE file for details.

## Author

Ishan Oshada
- Email: ishan.kodithuwakku.official@gmail.com
- GitHub: [ishanoshada](https://github.com/ishanoshada)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
