# 🔐 Cryptography Lib Lab Project

## Production-Grade Python Cryptography Application

A comprehensive, production-grade Python application for learning and demonstrating cryptographic algorithms, including AES encryption, DES encryption, RSA hybrid encryption, and algorithm performance comparison.

---

## 📋 Project Overview

This project implements security-first cryptographic standards with:

- ✅ **Hybrid Encryption (AES + RSA)**: Encrypts files using AES-256 and secures the AES key with RSA-2048
- ✅ **Algorithm Comparison (AES vs DES)**: Performance benchmarking with execution time and ciphertext size analysis
- ✅ **Proper Cryptographic Standards**: 
  - Cryptographically secure IV/nonce generation
  - PKCS7 padding implementation
  - SHA-256 file verification
- ✅ **Graphical User Interface**: Clean Tkinter GUI for easy file encryption
- ✅ **Comprehensive Logging**: Real-time execution logs and performance metrics
- ✅ **Professional Error Handling**: Graceful error handling and recovery

---

## 🏗️ Project Structure

```
Project-Arabawy/
├── cryptography/               # Virtual environment
├── main.py                     # Tkinter GUI application
├── crypto_utils.py             # Core cryptographic utilities
├── generate_data.py            # Sample data generator
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   └── original_data.csv       # Sample student records (generated)
└── output/                     # Encrypted files and keys (runtime)
    ├── encrypted_hybrid.bin    # AES+RSA encrypted file
    ├── encrypted_aes.bin       # AES encrypted file
    ├── encrypted_des.bin       # DES encrypted file
    ├── private_key.pem         # RSA private key
    └── public_key.pem          # RSA public key
```

---

## ⚙️ Installation & Setup

### Step 1: Activate Virtual Environment

```powershell
# Windows PowerShell
.\cryptography\Scripts\Activate.ps1

# Or use:
.\cryptography\Scripts\activate.bat
```

### Step 2: Verify Dependencies

```powershell
pip list
```

You should see:
- `pycryptodome` (3.20.0+)

### Step 3: Generate Sample Data (Optional)

```powershell
python generate_data.py
```

This creates `data/original_data.csv` with 10 student records.

---

## 🚀 Running the Application

### Launch the GUI

```powershell
python main.py
```

The Tkinter GUI will open with three main features:

#### Feature 1: 🔐 Hybrid Encryption (AES + RSA)
1. Click **"Browse File"** to select a CSV file
2. Click **"Hybrid Encryption (AES + RSA)"**
3. View execution logs showing:
   - RSA key pair generation time
   - AES encryption time
   - RSA key encryption time
   - Output file locations
   - File size comparison

**Output Files:**
- `output/encrypted_hybrid.bin` - Encrypted data
- `output/private_key.pem` - RSA private key
- `output/public_key.pem` - RSA public key

#### Feature 2: ⚖️ Compare AES vs DES
1. Click **"Browse File"** to select a CSV file
2. Click **"Compare AES vs DES"**
3. View detailed comparison showing:
   - AES encryption time
   - DES encryption time
   - AES decryption time
   - DES decryption time
   - Ciphertext sizes
   - Performance ratio
   - Verification results

**Output Files:**
- `output/encrypted_aes.bin` - AES encrypted file
- `output/encrypted_des.bin` - DES encrypted file

#### Feature 3: Clear Logs
Click **"Clear Logs"** to reset the execution log display.

---

## 📊 Technical Details

### Hybrid Encryption Workflow (AES + RSA)

```
1. RSA Key Generation
   └─> Generate 2048-bit RSA keypair
       └─> Export to PEM format

2. AES Key Generation
   └─> Generate 256-bit AES key
   └─> Generate cryptographically secure IV

3. File Encryption
   └─> Read plaintext file
   └─> Apply PKCS7 padding
   └─> Encrypt with AES-256-CBC
   └─> Save ciphertext to binary file

4. Key Encryption
   └─> Encrypt AES key with RSA public key
   └─> Save encrypted key metadata

5. Verification
   └─> Calculate SHA-256 hash of original file
   └─> Store for decryption verification
```

### Algorithm Comparison Workflow (AES vs DES)

```
For each algorithm:
  1. Generate key and IV
  2. Encrypt plaintext (measure time)
  3. Decrypt ciphertext (measure time)
  4. Record ciphertext size
  5. Verify decryption matches original

Results:
  - Execution time comparison
  - Ciphertext size comparison
  - Performance efficiency metrics
```

---

## 🔑 Cryptographic Standards Implemented

### AES-256 Encryption
- **Algorithm**: AES (Advanced Encryption Standard)
- **Key Size**: 256 bits
- **Mode**: CBC (Cipher Block Chaining)
- **IV Size**: 128 bits (16 bytes)
- **Padding**: PKCS7
- **Security Level**: 256-bit (> 2^128 security)

### DES Encryption
- **Algorithm**: DES (Data Encryption Standard)
- **Key Size**: 56 bits (8 bytes)
- **Mode**: CBC
- **IV Size**: 64 bits (8 bytes)
- **Padding**: PKCS7
- **Note**: Used for educational comparison only (weak by modern standards)

### RSA Encryption
- **Algorithm**: RSA (Rivest-Shamir-Adleman)
- **Key Size**: 2048 bits
- **Padding**: OAEP (Optimal Asymmetric Encryption Padding)
- **Hash Function**: SHA-256
- **Use**: Encrypting AES keys for hybrid encryption

### Hashing
- **Algorithm**: SHA-256 (Secure Hash Algorithm)
- **Output Size**: 256 bits (32 bytes)
- **Use**: File verification and integrity checking

---

## 📈 Performance Metrics Example

```
AES-256 vs DES Comparison Results:
==================================================

AES-256 (256-bit key):
  Encrypt Time: 0.85 ms
  Decrypt Time: 0.92 ms
  Total Time: 1.77 ms
  Ciphertext Size: 378 bytes

DES (56-bit key):
  Encrypt Time: 2.14 ms
  Decrypt Time: 1.98 ms
  Total Time: 4.12 ms
  Ciphertext Size: 376 bytes

Performance Analysis:
  AES is 2.33x FASTER than DES
  (Modern AES implementation is highly optimized)
```

---

## 🛡️ Security Features

### Proper Key Management
- ✅ Cryptographically secure random key generation
- ✅ No hardcoded keys or plaintexts
- ✅ Keys saved separately from encrypted data

### Padding & Encoding
- ✅ PKCS7 padding for symmetric encryption
- ✅ OAEP padding for RSA encryption
- ✅ Base64 encoding for metadata storage

### Verification
- ✅ SHA-256 hashing for file integrity
- ✅ Decryption verification against original
- ✅ Error handling for failed decryption

### File I/O
- ✅ Binary file handling for encrypted data
- ✅ Directory creation with proper permissions
- ✅ Graceful error handling for I/O operations

---

## 🧪 Testing

### Test Case 1: Hybrid Encryption
```powershell
# Generate test data
python generate_data.py

# Run application
python main.py

# In GUI:
# 1. Select data/original_data.csv
# 2. Click "Hybrid Encryption (AES + RSA)"
# 3. Verify output files created
# 4. Check execution times in logs
```

### Test Case 2: Algorithm Comparison
```powershell
# Run application
python main.py

# In GUI:
# 1. Select data/original_data.csv
# 2. Click "Compare AES vs DES"
# 3. Compare execution times
# 4. Analyze performance differences
```

### Test Case 3: Error Handling
```powershell
# In GUI:
# 1. Click buttons without selecting file
# 2. Verify error messages appear
# 3. Try encrypting non-existent files
# 4. Confirm graceful error handling
```

---

## 📚 Code Documentation

### crypto_utils.py
Core cryptographic module with classes and methods:

```python
class CryptoUtils:
    # Key generation
    generate_aes_key()
    generate_des_key()
    generate_rsa_keypair()
    generate_iv()

    # AES operations
    encrypt_aes()
    decrypt_aes()

    # DES operations
    encrypt_des()
    decrypt_des()

    # RSA operations
    encrypt_aes_key_with_rsa()
    decrypt_aes_key_with_rsa()
    save_keys_to_file()

    # Hashing
    calculate_sha256_hash()
    calculate_file_hash()
    verify_file_integrity()

    # Encoding
    encode_base64()
    decode_base64()

    # File I/O
    read_file()
    write_file()

    # High-level workflows
    hybrid_encrypt_file()
    hybrid_decrypt_file()
    compare_aes_vs_des()
```

### main.py
Tkinter GUI application with methods:

```python
class CryptoLabGUI:
    # UI Setup
    create_widgets()

    # File operations
    browse_file()

    # Encryption operations
    perform_hybrid_encryption()
    perform_comparison()

    # UI Updates
    display_logs()
    update_status()
    clear_logs()
```

---

## 🐛 Troubleshooting

### Issue: Module not found errors
```
Solution: Ensure virtual environment is activated and pycryptodome is installed
pip install pycryptodome
```

### Issue: GUI doesn't launch
```
Solution: Tkinter is included with Python. Try:
python main.py
```

### Issue: File encryption fails
```
Solution: 
- Ensure file path is correct
- Check file permissions
- Verify enough disk space in output/ directory
```

### Issue: Slow performance
```
Note: First run may be slower due to RSA key generation.
Subsequent operations will be faster. This is expected behavior.
```

---

## 📝 Requirements

### System Requirements
- Python 3.7+
- Windows/Mac/Linux
- 100MB free disk space (for keys and encrypted files)

### Python Dependencies
```
pycryptodome==3.20.0  # Cryptographic algorithms
tkinter               # GUI (included with Python)
```

### Optional
- OpenSSL (for key validation, but not required)

---

## 📜 License & Attribution

This project is created as an educational tool for learning cryptographic principles and industry best practices in information security.

### Technologies Used
- **Python 3.x**
- **pycryptodome** - Professional-grade cryptographic library
- **Tkinter** - Python's standard GUI library

---

## 📧 Project Information

**Project Name**: Cryptography Lib Lab Project  
**Version**: 1.0.0  
**Date**: May 2026  
**Author**: Cybersecurity Engineer  

**Key Features**:
- ✅ Production-grade cryptographic implementation
- ✅ Professional security standards compliance
- ✅ Comprehensive error handling
- ✅ Real-time performance metrics
- ✅ Educational value with practical examples

---

## 🎓 Learning Objectives

This project helps you learn:

1. **Cryptographic Algorithms**: AES, DES, RSA, SHA-256
2. **Key Management**: Generation, storage, encryption
3. **Symmetric vs Asymmetric Encryption**: Practical comparison
4. **Hybrid Encryption**: Combining symmetric and asymmetric crypto
5. **Performance Analysis**: Benchmarking encryption algorithms
6. **Secure Coding**: Error handling, input validation, file I/O
7. **Python GUI Development**: Tkinter for user interfaces
8. **Software Engineering**: Modular design, documentation, testing

---

## 🚀 Future Enhancements

Potential additions:
- [ ] Support for other encryption algorithms (3DES, Chacha20)
- [ ] Digital signatures implementation
- [ ] Key derivation functions (PBKDF2)
- [ ] Streaming encryption for large files
- [ ] Configuration file support
- [ ] Database storage for encryption keys
- [ ] Multi-threading for large file encryption
- [ ] Export/import encryption results

---

**Happy Secure Computing! 🔐**
