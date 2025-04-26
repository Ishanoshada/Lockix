import glob
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib

WATERMARK = "https://github.com/ishanoshada/Lockix"

def derive_key_iv(password, salt=None):
    """Derive encryption key and IV from password."""
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, 32)
    iv = hashlib.pbkdf2_hmac('sha256', key, salt, 100000, 16)
    return key, iv, salt

def encrypt_bytes(data, password):
    """Encrypt bytes using AES-256-CBC."""
    key, iv, salt = derive_key_iv(password)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return salt + encrypted_data  # Prepend salt (16 bytes)

def decrypt_bytes(encrypted_data, password):
    """Decrypt bytes using AES-256-CBC."""
    if len(encrypted_data) < 16:
        raise ValueError("Encrypted data too short to contain salt.")
    salt = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    if len(encrypted_data) % 16 != 0:
        raise ValueError("Encrypted data length is not a multiple of block size (16 bytes).")
    key, iv, _ = derive_key_iv(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decrypted_padded_data) + unpadder.finalize()

def encrypt_file(file_path, extension, password):
    """Encrypt first and last 10 chars of base64-encoded image file with watermark."""
    try:
        # Read image and encode to base64
        with open(file_path, 'rb') as f:
            image_data = f.read()
        base64_text = base64.b64encode(image_data).decode('utf-8')

        # Append watermark
        base64_text_with_watermark = base64_text + WATERMARK

        # Check if text is long enough
        if len(base64_text_with_watermark) < 20:
            return f"Error: Base64 text from {file_path} is too short (< 20 chars)."

        # Split into prefix, middle, suffix
        prefix = base64_text_with_watermark[:10].encode('utf-8')  # First 10 chars
        middle = base64_text_with_watermark[10:-10].encode('utf-8')  # Middle part
        suffix = base64_text_with_watermark[-10:].encode('utf-8')  # Last 10 chars

        # Encrypt prefix and suffix
        encrypted_prefix = encrypt_bytes(prefix, password)  # 16 (salt) + 16 (padded data) = 32 bytes
        encrypted_suffix = encrypt_bytes(suffix, password)  # 16 (salt) + 16 (padded data) = 32 bytes

        # Combine parts
        final_data = encrypted_prefix + middle + encrypted_suffix

        # Create encrypted filename
        encrypted_name = f"{os.path.basename(file_path).encode().hex()}_.{extension}"
        encrypted_path = os.path.join(os.path.dirname(file_path) or '.', encrypted_name)

        # Write encrypted file (binary, due to encrypted parts)
        with open(encrypted_path, 'wb') as f:
            f.write(final_data)

        # Remove original file
        os.remove(file_path)
        return encrypted_path
    except Exception as e:
        return f"Encryption failed: {str(e)}"

def decrypt_file(file_path, password):
    """Decrypt first and last 10 chars of base64-encoded encrypted file with watermark."""
    try:
        # Read encrypted file
        with open(file_path, 'rb') as f:
            data = f.read()

        # Check minimum size (32 bytes prefix + 32 bytes suffix + middle)
        if len(data) < 64:
            return f"Decryption failed: File {file_path} is too small (< 64 bytes)."

        # Split data: prefix (32 bytes), middle, suffix (32 bytes)
        encrypted_prefix = data[:32]  # 16 salt + 16 encrypted
        middle = data[32:-32]  # Middle part (base64 text)
        encrypted_suffix = data[-32:]  # 16 salt + 16 encrypted

        # Decrypt prefix and suffix
        prefix = decrypt_bytes(encrypted_prefix, password).decode('utf-8')
        suffix = decrypt_bytes(encrypted_suffix, password).decode('utf-8')

        # Combine parts
        base64_text_with_watermark = prefix + middle.decode('utf-8') + suffix

        # Remove watermark
        if not base64_text_with_watermark.endswith(WATERMARK):
            return f"Decryption failed: Watermark not found in {file_path}."
        base64_text = base64_text_with_watermark[:-len(WATERMARK)]

        # Decode from base64 to restore image
        image_data = base64.b64decode(base64_text)

        # Extract original filename
        basename = os.path.basename(file_path)
        name_part = basename.split('_.')[0]
        original_name = bytes.fromhex(name_part).decode('utf-8')
        original_path = os.path.join(os.path.dirname(file_path) or '.', original_name)

        # Write decrypted file
        with open(original_path, 'wb') as f:
            f.write(image_data)

        # Remove encrypted file
        os.remove(file_path)
        return original_path
    except ValueError as ve:
        return f"Decryption failed: {str(ve)}"
    except Exception as e:
        return f"Decryption failed: {str(e)}"

def encrypt_files(extension, target_extension, password):
    """Encrypt all files with given extension in current directory."""
    results = []
    for file_path in glob.glob(f'*.{extension}'):
        result = encrypt_file(file_path, target_extension, password)
        results.append((file_path, result))
    return results

def decrypt_files(extension, password):
    """Decrypt all encrypted files with given extension in current directory."""
    results = []
    for file_path in glob.glob(f'*.{extension}'):
        result = decrypt_file(file_path, password)
        results.append((file_path, result))
    return results