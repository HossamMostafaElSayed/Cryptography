# ⚡ Quick Start Guide - Cryptography Lab Project

## 5-Minute Setup & First Run

### ✅ Prerequisites Checklist
- [x] Python 3.7+ installed
- [x] Virtual environment created (`cryptography`)
- [x] pycryptodome installed
- [x] Sample data generated (`data/original_data.csv`)

---

## 🚀 Launch the Application

### Option 1: Using PowerShell

```powershell
cd "c:\Users\Hossam Mostafa\Desktop\Project-Arabawy"
.\cryptography\Scripts\Activate.ps1
python main.py
```

### Option 2: Quick Launch Script (Create this as `run.bat`)

```batch
@echo off
cd /d "%~dp0"
call cryptography\Scripts\activate.bat
python main.py
pause
```

---

## 🔐 First Test: Hybrid Encryption

1. **Launch the app**: `python main.py`
2. **Click "Browse File"**
3. **Select**: `data/original_data.csv`
4. **Click "🔐 Hybrid Encryption (AES + RSA)"**
5. **View Results**:
   - Check execution logs
   - Output files created in `output/` directory
   - Success message shows file sizes

### Expected Output Files:
```
output/
├── encrypted_hybrid.bin      # Encrypted data
├── private_key.pem          # RSA private key
└── public_key.pem           # RSA public key
```

---

## ⚖️ Second Test: Algorithm Comparison

1. **Click "Browse File"** (keep same file selected)
2. **Click "⚖️ Compare AES vs DES"**
3. **View Comparison Results**:
   - AES vs DES encryption times
   - Ciphertext size comparison
   - Performance efficiency metrics

### Expected Output Files:
```
output/
├── encrypted_aes.bin        # AES encrypted file
└── encrypted_des.bin        # DES encrypted file
```

---

## 📊 Understanding the Logs

### Color Coding:
- 🟢 **Green [+]**: Successful operations
- 🔴 **Red [!]**: Errors and warnings
- 🔵 **Blue [*]**: Process markers
- ⚫ **Black**: General information

### Sample Log Output:
```
[*] Starting Hybrid Encryption (AES + RSA)...
[+] RSA Key pair generated in 0.4521s
[+] Read input file: 312 bytes
[+] AES encryption completed in 0.0012s
[+] RSA key encryption completed in 0.0045s
[+] Ciphertext size: 376 bytes
[+] Encryption saved to: output/encrypted_hybrid.bin
[+] Keys saved to: output/
```

---

## 🧪 Test All Features

### Test Script:
```powershell
python test_crypto.py
```

This runs comprehensive tests on all cryptographic functions:
- Key generation (AES, DES, RSA)
- Encryption/Decryption (AES, DES)
- RSA Hybrid encryption
- SHA-256 hashing
- Base64 encoding
- File I/O operations

---

## 📁 Project File Organization

```
Project-Arabawy/
├── main.py                 # 🎯 Launch this to run GUI
├── crypto_utils.py         # Cryptographic implementation
├── generate_data.py        # Generate sample CSV
├── test_crypto.py          # Run unit tests
├── requirements.txt        # Python dependencies
├── README.md              # Full documentation
├── QUICKSTART.md          # This file
│
├── cryptography/          # Virtual environment
├── data/                  # Input data
│   └── original_data.csv  # Sample student records
├── output/                # Generated encrypted files & keys
└── __pycache__/           # Python cache (ignore)
```

---

## ⚙️ Virtual Environment Commands

### Activate
```powershell
.\cryptography\Scripts\Activate.ps1
```

### Deactivate
```powershell
deactivate
```

### Update Dependencies
```powershell
pip install -r requirements.txt --upgrade
```

### List Installed Packages
```powershell
pip list
```

---

## 🎓 Learning Path

### Week 1: Understanding Basics
1. Read `README.md`
2. Review `crypto_utils.py` code comments
3. Run `test_crypto.py` to see functions in action
4. Examine generated keys in `output/`

### Week 2: Hands-On Testing
1. Run Hybrid Encryption with different files
2. Compare AES vs DES performance on larger files
3. Examine encrypted output files (binary format)
4. Verify file hashes for integrity

### Week 3: Deep Dive
1. Modify algorithm parameters (key sizes, IV sizes)
2. Add new encryption algorithms
3. Implement file decryption workflow
4. Create custom data generators

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'crypto_utils'"
```
Solution: Make sure you're in the project root directory
cd "c:\Users\Hossam Mostafa\Desktop\Project-Arabawy"
```

### Issue: "Tkinter not found"
```
Solution: Reinstall Python with Tkinter
- Windows: Run Python installer, select "tcl/tk and IDLE"
```

### Issue: "Virtual environment not activated"
```
Solution: Check if (cryptography) appears in terminal prompt
If not: .\cryptography\Scripts\Activate.ps1
```

### Issue: Slow performance on first run
```
Note: RSA key generation takes time. This is expected!
First run: ~0.5-1 second
Subsequent runs: ~0.01-0.1 seconds
```

---

## 📈 Performance Tips

### For Faster Operations:
1. Use smaller test files (< 1MB)
2. Pre-generate RSA keys and reuse them
3. Use batch mode for multiple files

### For Learning:
1. Start with small files (< 100 bytes)
2. Review logs after each operation
3. Compare binary output files

---

## 🎯 Next Steps

1. ✅ Complete: Setup & installation
2. ✅ Complete: Run first encryption
3. ⭕ Run algorithm comparison
4. ⭕ Test with your own files
5. ⭕ Modify parameters and observe results
6. ⭕ Implement additional features

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Launch GUI | `python main.py` |
| Generate data | `python generate_data.py` |
| Run tests | `python test_crypto.py` |
| Activate env | `.\cryptography\Scripts\Activate.ps1` |
| Install packages | `pip install -r requirements.txt` |
| Update packages | `pip install --upgrade -r requirements.txt` |

---

## 🎉 You're Ready!

Your Cryptography Lab Project is fully set up and tested. 

**Start with**: `python main.py`

Enjoy exploring the world of cryptography! 🔐

For detailed information, see [README.md](README.md)
