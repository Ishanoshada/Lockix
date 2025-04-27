import glob
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hmac
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
import hashlib

WATERMARK = "https://github.com/ishanoshada/Lockix"

def derive_key(password, salt=None):
    """Derive encryption and HMAC keys from password."""
    if salt is None:
        salt = os.urandom(16)
    # Use higher iteration count for stronger key derivation
    key_material = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000000, 64)
    encryption_key = key_material[:32]  # 32 bytes for AES-256
    hmac_key = key_material[32:]  # 32 bytes for HMAC
    return encryption_key, hmac_key, salt

def encrypt_bytes(data, password, iv=None):
    """Encrypt bytes using AES-256-CBC with HMAC."""
    if iv is None:
        iv = os.urandom(16)  # Random IV for each encryption
    encryption_key, hmac_key, salt = derive_key(password)

    # Create cipher
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Compute HMAC
    h = hmac.HMAC(hmac_key, SHA256(), backend=default_backend())
    h.update(salt + iv + encrypted_data)
    hmac_tag = h.finalize()

    # Return structured data: salt (16) + IV (16) + HMAC (32) + encrypted data
    return salt + iv + hmac_tag + encrypted_data

def decrypt_bytes(encrypted_data, password):
    """Decrypt bytes using AES-256-CBC with HMAC verification."""
    if len(encrypted_data) < 64:  # 16 (salt) + 16 (IV) + 32 (HMAC)
        raise ValueError("Encrypted data too short to contain metadata.")
    
    # Extract components
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    hmac_tag = encrypted_data[32:64]
    encrypted_data = encrypted_data[64:]

    if len(encrypted_data) % 16 != 0:
        raise ValueError("Encrypted data length is not a multiple of block size (16 bytes).")

    # Derive keys
    encryption_key, hmac_key, _ = derive_key(password, salt)

    # Verify HMAC
    h = hmac.HMAC(hmac_key, SHA256(), backend=default_backend())
    h.update(salt + iv + encrypted_data)
    h.verify(hmac_tag)  # Raises InvalidSignature if tampered

    # Decrypt
    cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decrypted_padded_data) + unpadder.finalize()

def encrypt_file(file_path, extension, password):
    """Encrypt base64-encoded image file with watermark."""
    try:
        # Read image and encode to base64
        with open(file_path, 'rb') as f:
            image_data = f.read()
        base64_text = base64.b64encode(image_data).decode('utf-8')

        # Append watermark
        base64_text_with_watermark = base64_text + WATERMARK
        data_to_encrypt = base64_text_with_watermark.encode('utf-8')

        # Encrypt entire data
        encrypted_data = encrypt_bytes(data_to_encrypt, password)

        # Split encrypted data into prefix, middle, suffix for compatibility
        # Each part is encrypted, but we mimic the original structure
        if len(encrypted_data) < 64:
            return f"Error: Encrypted data from {file_path} is too short."
        
        prefix = encrypted_data[:32]  # First 32 bytes
        middle = encrypted_data[32:-32]  # Middle part
        suffix = encrypted_data[-32:]  # Last 32 bytes
        final_data = prefix + middle + suffix  # Same as encrypted_data, but structured

        # Create encrypted filename
        encrypted_name = f"{os.path.basename(file_path).encode().hex()}_.{extension}"
        encrypted_path = os.path.join(os.path.dirname(file_path) or '.', encrypted_name)

        # Write encrypted file
        with open(encrypted_path, 'wb') as f:
            f.write(final_data)

        # Remove original file
        os.remove(file_path)
        return encrypted_path
    except Exception as e:
        return f"Encryption failed: {str(e)}"

def decrypt_file(file_path, password):
    """Decrypt base64-encoded encrypted file with watermark."""
    try:
        # Read encrypted file
        with open(file_path, 'rb') as f:
            data = f.read()

        # Check minimum size
        if len(data) < 64:
            return f"Decryption failed: File {file_path} is too small (< 64 bytes)."

        # Reconstruct encrypted data (prefix + middle + suffix)
        encrypted_data = data  # Already structured correctly

        # Decrypt entire data
        decrypted_data = decrypt_bytes(encrypted_data, password)
        base64_text_with_watermark = decrypted_data.decode('utf-8')

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