"""
Cryptography Lib Lab Project - Cryptographic Utilities Module
==============================================================
This module implements production-grade cryptographic functions including:
- AES Encryption/Decryption with proper IV and PKCS7 padding
- DES Encryption/Decryption with proper IV and PKCS7 padding
- RSA Hybrid Encryption (RSA encrypts the AES key)
- SHA-256 hashing for file verification
- Base64 encoding/decoding
- Execution time measurement and comparison

Author: Cybersecurity Engineer
Date: May 2026
"""

import os
import time
import json
import csv
import random
import hashlib
import base64
from pathlib import Path
from typing import Tuple, Dict

from Crypto.Cipher import AES, DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class CryptoUtils:
    """
    A comprehensive cryptography utility class implementing industry-standard
    encryption algorithms with proper key management and verification.
    """

    # Constants for algorithm parameters
    AES_KEY_SIZE = 32  # 256-bit key
    DES_KEY_SIZE = 8   # 56-bit key (DES requirement)
    RSA_KEY_SIZE = 2048  # 2048-bit RSA keys
    BLOCK_SIZE = 8  # DES block size (AES uses 16, but we keep DES standard)

    def __init__(self):
        """Initialize the cryptography utilities."""
        self.execution_log = []

    def log_message(self, message: str) -> None:
        """
        Log execution messages for GUI display.
        
        Args:
            message: Message to log
        """
        self.execution_log.append(message)
        try:
            print(message)
        except Exception:
            # Suppress console output errors in GUI mode (Windows)
            pass

    def get_logs(self) -> str:
        """
        Retrieve all logged messages.
        
        Returns:
            String containing all log messages joined by newlines
        """
        return "\n".join(self.execution_log)

    def clear_logs(self) -> None:
        """Clear the execution log."""
        self.execution_log = []

    # ==================== AES ENCRYPTION ====================

    def generate_aes_key(self, key_size: int = AES_KEY_SIZE) -> bytes:
        """
        Generate a cryptographically secure AES key.
        
        Args:
            key_size: Size of the key in bytes (16, 24, or 32 for AES)
            
        Returns:
            Random bytes suitable for AES encryption
        """
        return get_random_bytes(key_size)

    def generate_iv(self, size: int = 16) -> bytes:
        """
        Generate a cryptographically secure Initialization Vector.
        
        Args:
            size: Size of IV in bytes (typically 16 for AES)
            
        Returns:
            Random bytes suitable for use as IV
        """
        return get_random_bytes(size)

    def encrypt_aes(self, plaintext: bytes, key: bytes, iv: bytes = None) -> Tuple[bytes, bytes]:
        """
        Encrypt data using AES-256 in CBC mode with PKCS7 padding.
        
        Args:
            plaintext: Data to encrypt
            key: AES encryption key (must be 16, 24, or 32 bytes)
            iv: Initialization Vector (generated if not provided)
            
        Returns:
            Tuple of (ciphertext, iv)
        """
        if iv is None:
            iv = self.generate_iv()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = pad(plaintext, AES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)

        return ciphertext, iv

    def decrypt_aes(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """
        Decrypt AES-256 encrypted data in CBC mode.
        
        Args:
            ciphertext: Encrypted data
            key: AES decryption key
            iv: Initialization Vector used during encryption
            
        Returns:
            Decrypted plaintext
            
        Raises:
            ValueError: If decryption fails or padding is invalid
        """
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)

        return plaintext

    # ==================== DES ENCRYPTION ====================

    def generate_des_key(self) -> bytes:
        """
        Generate a cryptographically secure DES key.
        DES uses 56-bit keys (8 bytes with parity bits).
        
        Returns:
            Random bytes suitable for DES encryption
        """
        return get_random_bytes(self.DES_KEY_SIZE)

    def encrypt_des(self, plaintext: bytes, key: bytes, iv: bytes = None) -> Tuple[bytes, bytes]:
        """
        Encrypt data using DES in CBC mode with PKCS7 padding.
        
        Note: DES has a small block size (8 bytes) and weak security.
        Used here for educational comparison with AES only.
        
        Args:
            plaintext: Data to encrypt
            key: DES encryption key (must be 8 bytes)
            iv: Initialization Vector (generated if not provided)
            
        Returns:
            Tuple of (ciphertext, iv)
        """
        if iv is None:
            iv = self.generate_iv(size=8)  # DES uses 8-byte IV

        cipher = DES.new(key, DES.MODE_CBC, iv)
        padded_plaintext = pad(plaintext, DES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)

        return ciphertext, iv

    def decrypt_des(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """
        Decrypt DES encrypted data in CBC mode.
        
        Args:
            ciphertext: Encrypted data
            key: DES decryption key
            iv: Initialization Vector used during encryption
            
        Returns:
            Decrypted plaintext
            
        Raises:
            ValueError: If decryption fails or padding is invalid
        """
        cipher = DES.new(key, DES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, DES.block_size)

        return plaintext

    # ==================== RSA HYBRID ENCRYPTION ====================

    def generate_rsa_keypair(self, key_size: int = RSA_KEY_SIZE) -> Tuple[bytes, bytes]:
        """
        Generate RSA public/private key pair.
        
        Args:
            key_size: Size of RSA key in bits (typically 2048 or 4096)
            
        Returns:
            Tuple of (private_key_pem, public_key_pem) as bytes
        """
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        return private_key, public_key

    def save_keys_to_file(self, private_key: bytes, public_key: bytes, 
                         output_dir: str = "output") -> Dict[str, str]:
        """
        Save RSA keys to files.
        
        Args:
            private_key: Private key in PEM format
            public_key: Public key in PEM format
            output_dir: Directory to save keys
            
        Returns:
            Dictionary with file paths
        """
        Path(output_dir).mkdir(exist_ok=True)
        
        private_key_path = os.path.join(output_dir, "private_key.pem")
        public_key_path = os.path.join(output_dir, "public_key.pem")

        with open(private_key_path, 'wb') as f:
            f.write(private_key)

        with open(public_key_path, 'wb') as f:
            f.write(public_key)

        return {
            'private_key': private_key_path,
            'public_key': public_key_path
        }

    def encrypt_aes_key_with_rsa(self, aes_key: bytes, public_key: bytes) -> bytes:
        """
        Encrypt an AES key using RSA public key.
        This implements hybrid encryption security.
        
        Args:
            aes_key: The AES key to encrypt
            public_key: RSA public key in PEM format
            
        Returns:
            Encrypted AES key
        """
        public_key_obj = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(public_key_obj)
        encrypted_aes_key = cipher.encrypt(aes_key)

        return encrypted_aes_key

    def decrypt_aes_key_with_rsa(self, encrypted_aes_key: bytes, private_key: bytes) -> bytes:
        """
        Decrypt an AES key using RSA private key.
        
        Args:
            encrypted_aes_key: Encrypted AES key
            private_key: RSA private key in PEM format
            
        Returns:
            Decrypted AES key
            
        Raises:
            ValueError: If decryption fails
        """
        private_key_obj = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(private_key_obj)
        aes_key = cipher.decrypt(encrypted_aes_key)

        return aes_key

    # ==================== HASHING & VERIFICATION ====================

    def calculate_sha256_hash(self, data: bytes) -> str:
        """
        Calculate SHA-256 hash of data.
        
        Args:
            data: Data to hash
            
        Returns:
            Hexadecimal string representation of hash
        """
        return hashlib.sha256(data).hexdigest()

    def calculate_file_hash(self, file_path: str) -> str:
        """
        Calculate SHA-256 hash of a file.
        Reads file in chunks to handle large files efficiently.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Hexadecimal string representation of hash
        """
        sha256_hash = hashlib.sha256()
        chunk_size = 65536  # 64KB chunks

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()

    def verify_file_integrity(self, original_file: str, decrypted_file: str) -> bool:
        """
        Verify that original and decrypted files are identical using SHA-256.
        
        Args:
            original_file: Path to original file
            decrypted_file: Path to decrypted file
            
        Returns:
            True if files are identical, False otherwise
        """
        original_hash = self.calculate_file_hash(original_file)
        decrypted_hash = self.calculate_file_hash(decrypted_file)

        return original_hash == decrypted_hash

    # ==================== BASE64 ENCODING ====================

    def encode_base64(self, data: bytes) -> str:
        """
        Encode bytes to Base64 string.
        
        Args:
            data: Data to encode
            
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(data).decode('utf-8')

    def decode_base64(self, data_str: str) -> bytes:
        """
        Decode Base64 string to bytes.
        
        Args:
            data_str: Base64 encoded string
            
        Returns:
            Decoded bytes
        """
        return base64.b64decode(data_str.encode('utf-8'))

    # ==================== FILE I/O ====================

    def read_file(self, file_path: str) -> bytes:
        """
        Read file contents as bytes.
        
        Args:
            file_path: Path to file
            
        Returns:
            File contents as bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except IOError as e:
            raise IOError(f"Error reading file {file_path}: {str(e)}")

    def write_file(self, file_path: str, data: bytes) -> None:
        """
        Write bytes to file.
        
        Args:
            file_path: Path to output file
            data: Data to write
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            Path(os.path.dirname(file_path) or '.').mkdir(parents=True, exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(data)
        except IOError as e:
            raise IOError(f"Error writing file {file_path}: {str(e)}")

    # ==================== METADATA MANAGEMENT ====================

    def save_metadata(self, metadata: Dict, output_dir: str = "output", filename: str = "encryption_metadata.json") -> str:
        """
        Save encryption metadata to JSON file for later decryption.
        
        Args:
            metadata: Dictionary containing encryption metadata
            output_dir: Directory to save metadata
            filename: Name of metadata file
            
        Returns:
            Path to metadata file
        """
        Path(output_dir).mkdir(exist_ok=True)
        metadata_path = os.path.join(output_dir, filename)
        
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            self.log_message(f"[+] Metadata saved to: {metadata_path}")
            return metadata_path
        except IOError as e:
            raise IOError(f"Error saving metadata: {str(e)}")

    def load_metadata(self, metadata_path: str) -> Dict:
        """
        Load encryption metadata from JSON file.
        
        Args:
            metadata_path: Path to metadata JSON file
            
        Returns:
            Dictionary containing encryption metadata
        """
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            self.log_message(f"[+] Metadata loaded from: {metadata_path}")
            return metadata
        except FileNotFoundError:
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid metadata file format: {metadata_path}")

    # ==================== HIGH-LEVEL WORKFLOWS ====================

    def hybrid_encrypt_file(self, input_file: str, output_dir: str = "output") -> Dict:
        """
        Encrypt a file using hybrid encryption (AES + RSA).
        
        Workflow:
        1. Generate RSA keypair
        2. Generate AES key and IV
        3. Encrypt file with AES
        4. Encrypt AES key with RSA public key
        5. Save encrypted file and metadata
        
        Args:
            input_file: Path to file to encrypt
            output_dir: Directory for output files
            
        Returns:
            Dictionary with encryption metadata and file paths
        """
        self.log_message("[*] Starting Hybrid Encryption (AES + RSA)...")

        # Generate keys
        start_time = time.time()
        private_key, public_key = self.generate_rsa_keypair()
        key_gen_time = time.time() - start_time
        self.log_message(f"[+] RSA Key pair generated in {key_gen_time:.4f}s")

        # Generate AES key and IV
        aes_key = self.generate_aes_key()
        aes_iv = self.generate_iv()

        # Read plaintext file
        plaintext = self.read_file(input_file)
        self.log_message(f"[+] Read input file: {len(plaintext)} bytes")

        # Encrypt with AES
        start_time = time.time()
        ciphertext, used_iv = self.encrypt_aes(plaintext, aes_key, aes_iv)
        aes_time = time.time() - start_time
        self.log_message(f"[+] AES encryption completed in {aes_time:.4f}s")

        # Encrypt AES key with RSA
        start_time = time.time()
        encrypted_aes_key = self.encrypt_aes_key_with_rsa(aes_key, public_key)
        rsa_time = time.time() - start_time
        self.log_message(f"[+] RSA key encryption completed in {rsa_time:.4f}s")

        # Save files
        Path(output_dir).mkdir(exist_ok=True)
        encrypted_file = os.path.join(output_dir, "encrypted_hybrid.bin")
        self.write_file(encrypted_file, ciphertext)

        key_paths = self.save_keys_to_file(private_key, public_key, output_dir)

        # Save metadata
        metadata = {
            'aes_iv': self.encode_base64(used_iv),
            'encrypted_aes_key': self.encode_base64(encrypted_aes_key),
            'ciphertext_size': len(ciphertext),
            'original_size': len(plaintext),
            'compression_ratio': (1 - len(ciphertext) / len(plaintext)) * 100,
            'original_file_hash': self.calculate_sha256_hash(plaintext)
        }

        # Save metadata to JSON file
        self.save_metadata(metadata, output_dir)

        self.log_message(f"[+] Ciphertext size: {len(ciphertext)} bytes")
        self.log_message(f"[+] Encryption saved to: {encrypted_file}")
        self.log_message(f"[+] Keys saved to: {output_dir}/")

        return {
            'encrypted_file': encrypted_file,
            'private_key': private_key,
            'public_key': public_key,
            'aes_iv': used_iv,
            'encrypted_aes_key': encrypted_aes_key,
            'metadata': metadata
        }

    def hybrid_decrypt_file(self, encrypted_file: str, private_key: bytes, 
                           encrypted_aes_key: bytes, aes_iv: bytes, 
                           output_dir: str = "output") -> str:
        """
        Decrypt a file encrypted with hybrid encryption.
        
        Args:
            encrypted_file: Path to encrypted file
            private_key: RSA private key bytes
            encrypted_aes_key: Encrypted AES key bytes
            aes_iv: AES IV bytes
            output_dir: Directory for output files
            
        Returns:
            Path to decrypted file
        """
        self.log_message("[*] Starting Hybrid Decryption...")

        # Decrypt AES key with RSA
        start_time = time.time()
        aes_key = self.decrypt_aes_key_with_rsa(encrypted_aes_key, private_key)
        rsa_time = time.time() - start_time
        self.log_message(f"[+] RSA key decryption completed in {rsa_time:.4f}s")

        # Read encrypted file
        ciphertext = self.read_file(encrypted_file)
        self.log_message(f"[+] Read encrypted file: {len(ciphertext)} bytes")

        # Decrypt with AES
        start_time = time.time()
        plaintext = self.decrypt_aes(ciphertext, aes_key, aes_iv)
        aes_time = time.time() - start_time
        self.log_message(f"[+] AES decryption completed in {aes_time:.4f}s")

        # Save decrypted file
        Path(output_dir).mkdir(exist_ok=True)
        decrypted_file = os.path.join(output_dir, "decrypted_hybrid.csv")
        self.write_file(decrypted_file, plaintext)

        self.log_message(f"[+] Decrypted file saved to: {decrypted_file}")

        return decrypted_file

    def compare_aes_vs_des(self, input_file: str, output_dir: str = "output") -> Dict:
        """
        Encrypt a file with both AES and DES to compare performance.
        
        Args:
            input_file: Path to file to encrypt
            output_dir: Directory for output files
            
        Returns:
            Dictionary with comparison results
        """
        self.log_message("[*] Starting AES vs DES Comparison...")
        Path(output_dir).mkdir(exist_ok=True)

        # Read plaintext
        plaintext = self.read_file(input_file)
        self.log_message(f"[+] Read input file: {len(plaintext)} bytes")

        # ===== AES ENCRYPTION =====
        self.log_message("\n[*] AES Encryption/Decryption:")
        aes_key = self.generate_aes_key()
        aes_iv = self.generate_iv()

        # Encrypt with AES
        start_time = time.time()
        aes_ciphertext, _ = self.encrypt_aes(plaintext, aes_key, aes_iv)
        aes_encrypt_time = time.time() - start_time
        self.log_message(f"  [+] Encryption time: {aes_encrypt_time:.6f}s")

        # Decrypt with AES
        start_time = time.time()
        aes_plaintext = self.decrypt_aes(aes_ciphertext, aes_key, aes_iv)
        aes_decrypt_time = time.time() - start_time
        self.log_message(f"  [+] Decryption time: {aes_decrypt_time:.6f}s")
        self.log_message(f"  [+] Ciphertext size: {len(aes_ciphertext)} bytes")

        # Save AES encrypted file
        aes_file = os.path.join(output_dir, "encrypted_aes.bin")
        self.write_file(aes_file, aes_ciphertext)

        # ===== DES ENCRYPTION =====
        self.log_message("\n[*] DES Encryption/Decryption:")
        des_key = self.generate_des_key()
        des_iv = self.generate_iv(size=8)

        # Encrypt with DES
        start_time = time.time()
        des_ciphertext, _ = self.encrypt_des(plaintext, des_key, des_iv)
        des_encrypt_time = time.time() - start_time
        self.log_message(f"  [+] Encryption time: {des_encrypt_time:.6f}s")

        # Decrypt with DES
        start_time = time.time()
        des_plaintext = self.decrypt_des(des_ciphertext, des_key, des_iv)
        des_decrypt_time = time.time() - start_time
        self.log_message(f"  [+] Decryption time: {des_decrypt_time:.6f}s")
        self.log_message(f"  [+] Ciphertext size: {len(des_ciphertext)} bytes")

        # Save DES encrypted file
        des_file = os.path.join(output_dir, "encrypted_des.bin")
        self.write_file(des_file, des_ciphertext)

        # ===== COMPARISON RESULTS =====
        self.log_message("\n[*] Algorithm Comparison:")
        speed_ratio = des_encrypt_time / aes_encrypt_time if aes_encrypt_time > 0 else 0
        self.log_message(f"  [+] AES is {speed_ratio:.2f}x {'slower' if speed_ratio > 1 else 'faster'} than DES")
        self.log_message(f"  [+] AES total time: {aes_encrypt_time + aes_decrypt_time:.6f}s")
        self.log_message(f"  [+] DES total time: {des_encrypt_time + des_decrypt_time:.6f}s")

        # ===== VERIFICATION =====
        self.log_message("\n[*] Verification:")
        aes_match = aes_plaintext == plaintext
        des_match = des_plaintext == plaintext
        self.log_message(f"  [+] AES decryption matches original: {aes_match}")
        self.log_message(f"  [+] DES decryption matches original: {des_match}")

        return {
            'aes': {
                'ciphertext': aes_ciphertext,
                'encrypt_time': aes_encrypt_time,
                'decrypt_time': aes_decrypt_time,
                'ciphertext_size': len(aes_ciphertext),
                'file': aes_file
            },
            'des': {
                'ciphertext': des_ciphertext,
                'encrypt_time': des_encrypt_time,
                'decrypt_time': des_decrypt_time,
                'ciphertext_size': len(des_ciphertext),
                'file': des_file
            }
        }
