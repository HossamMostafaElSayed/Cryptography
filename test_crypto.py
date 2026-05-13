"""
Quick Test Script for Cryptography Lab Project
================================================
Verifies that all cryptographic functions work correctly.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from crypto_utils import CryptoUtils


def test_crypto_utils():
    """Run quick tests on crypto utilities."""
    print("🧪 Testing Cryptography Lab Project")
    print("=" * 60)

    try:
        # Initialize
        crypto = CryptoUtils()

        # Test 1: Key Generation
        print("\n[Test 1] Key Generation")
        aes_key = crypto.generate_aes_key()
        print(f"  ✓ AES Key: {len(aes_key)} bytes")

        des_key = crypto.generate_des_key()
        print(f"  ✓ DES Key: {len(des_key)} bytes")

        private_key, public_key = crypto.generate_rsa_keypair()
        print(f"  ✓ RSA Private Key: {len(private_key)} bytes")
        print(f"  ✓ RSA Public Key: {len(public_key)} bytes")

        # Test 2: IV Generation
        print("\n[Test 2] IV Generation")
        aes_iv = crypto.generate_iv(16)
        print(f"  ✓ AES IV: {len(aes_iv)} bytes")

        des_iv = crypto.generate_iv(8)
        print(f"  ✓ DES IV: {len(des_iv)} bytes")

        # Test 3: AES Encryption/Decryption
        print("\n[Test 3] AES Encryption/Decryption")
        plaintext = b"Hello, Cryptography Lab! This is a test message."
        ciphertext, used_iv = crypto.encrypt_aes(plaintext, aes_key)
        decrypted = crypto.decrypt_aes(ciphertext, aes_key, used_iv)
        
        if decrypted == plaintext:
            print(f"  ✓ Plaintext: {len(plaintext)} bytes")
            print(f"  ✓ Ciphertext: {len(ciphertext)} bytes")
            print(f"  ✓ Decryption matches original: YES")
        else:
            print("  ✗ Decryption failed!")
            return False

        # Test 4: DES Encryption/Decryption
        print("\n[Test 4] DES Encryption/Decryption")
        ciphertext_des, used_iv_des = crypto.encrypt_des(plaintext, des_key)
        decrypted_des = crypto.decrypt_des(ciphertext_des, des_key, used_iv_des)

        if decrypted_des == plaintext:
            print(f"  ✓ Ciphertext: {len(ciphertext_des)} bytes")
            print(f"  ✓ Decryption matches original: YES")
        else:
            print("  ✗ DES Decryption failed!")
            return False

        # Test 5: RSA Hybrid Encryption
        print("\n[Test 5] RSA Hybrid Encryption")
        encrypted_aes_key = crypto.encrypt_aes_key_with_rsa(aes_key, public_key)
        decrypted_aes_key = crypto.decrypt_aes_key_with_rsa(encrypted_aes_key, private_key)

        if decrypted_aes_key == aes_key:
            print(f"  ✓ Original AES Key: {len(aes_key)} bytes")
            print(f"  ✓ Encrypted Key: {len(encrypted_aes_key)} bytes")
            print(f"  ✓ Decrypted Key matches original: YES")
        else:
            print("  ✗ RSA Key Decryption failed!")
            return False

        # Test 6: Hashing
        print("\n[Test 6] SHA-256 Hashing")
        hash_value = crypto.calculate_sha256_hash(plaintext)
        print(f"  ✓ SHA-256 Hash: {hash_value[:32]}...")
        print(f"  ✓ Hash Length: {len(hash_value)} characters")

        # Test 7: Base64 Encoding
        print("\n[Test 7] Base64 Encoding/Decoding")
        encoded = crypto.encode_base64(ciphertext)
        decoded = crypto.decode_base64(encoded)

        if decoded == ciphertext:
            print(f"  ✓ Encoded length: {len(encoded)} characters")
            print(f"  ✓ Decoding matches original: YES")
        else:
            print("  ✗ Base64 Decoding failed!")
            return False

        # Test 8: File Operations
        print("\n[Test 8] File Operations")
        test_file = "data/test_input.bin"
        Path("data").mkdir(exist_ok=True)
        crypto.write_file(test_file, plaintext)
        read_content = crypto.read_file(test_file)

        if read_content == plaintext:
            print(f"  ✓ File write/read successful")
            print(f"  ✓ Content matches original: YES")
        else:
            print("  ✗ File operations failed!")
            return False

        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_crypto_utils()
    sys.exit(0 if success else 1)
