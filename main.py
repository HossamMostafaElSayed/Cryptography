"""
Cryptography Lib Lab Project - Main GUI Application
====================================================
This module provides a production-grade Tkinter GUI for:
- File selection and encryption
- Hybrid encryption (AES + RSA)
- Algorithm comparison (AES vs DES)
- Real-time execution logs and performance metrics

Author: Cybersecurity Engineer
Date: May 2026
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path

# Import the cryptography utilities
from crypto_utils import CryptoUtils
from generate_data import generate_student_data


class CryptoLabGUI:
    """
    Main GUI application for the Cryptography Lab Project.
    Provides user-friendly interface for encryption operations.
    """

    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Cryptography Lab - Production Security Toolkit")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Initialize crypto utilities
        self.crypto = CryptoUtils()
        self.selected_file = None
        self.encryption_results = None
        self.selected_encrypted_file = None
        self.selected_private_key = None
        self.selected_metadata_file = None

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        """Create all GUI components."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # ===== TITLE =====
        title_label = ttk.Label(
            main_frame,
            text="🔐 Cryptography Lab Project - Security Toolkit",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # ===== FILE SELECTION FRAME =====
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        file_frame.columnconfigure(1, weight=1)

        # File path display
        ttk.Label(file_frame, text="Selected File:").grid(row=0, column=0, sticky=tk.W)
        self.file_label = ttk.Label(
            file_frame,
            text="No file selected",
            foreground="gray"
        )
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        # Browse button
        browse_btn = ttk.Button(
            file_frame,
            text="Browse File",
            command=self.browse_file
        )
        browse_btn.grid(row=0, column=2, padx=5)

        # File info label
        self.file_info_label = ttk.Label(file_frame, text="", foreground="blue")
        self.file_info_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)

        # ===== ENCRYPTION OPTIONS FRAME =====
        options_frame = ttk.LabelFrame(main_frame, text="Encryption Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        options_frame.columnconfigure(0, weight=1)
        options_frame.rowconfigure(1, weight=1)

        # Button frame
        button_frame = ttk.Frame(options_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        hybrid_btn = ttk.Button(
            button_frame,
            text="🔐 Hybrid Encryption (AES + RSA)",
            command=self.perform_hybrid_encryption,
            width=30
        )
        hybrid_btn.pack(side=tk.LEFT, padx=5)

        compare_btn = ttk.Button(
            button_frame,
            text="⚖️ Compare AES vs DES",
            command=self.perform_comparison,
            width=30
        )
        compare_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = ttk.Button(
            button_frame,
            text="Clear Logs",
            command=self.clear_logs,
            width=15
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        generate_data_btn = ttk.Button(
            button_frame,
            text="📊 Generate Random Data",
            command=self.generate_random_data,
            width=25
        )
        generate_data_btn.pack(side=tk.LEFT, padx=5)

        decrypt_btn = ttk.Button(
            button_frame,
            text="🔓 Decrypt Hybrid File",
            command=self.show_decrypt_dialog,
            width=25
        )
        decrypt_btn.pack(side=tk.LEFT, padx=5)

        # Output log
        log_label = ttk.Label(options_frame, text="Execution Logs:")
        log_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

        self.log_text = scrolledtext.ScrolledText(
            options_frame,
            height=20,
            width=100,
            font=("Courier New", 9),
            bg="#f0f0f0",
            fg="#000000"
        )
        self.log_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Configure text tags for colors
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("info", foreground="blue")
        self.log_text.tag_config("warning", foreground="orange")

        # ===== STATUS BAR =====
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        self.status_label = ttk.Label(
            status_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X)

    def browse_file(self):
        """Open file browser dialog and select a file."""
        file_path = filedialog.askopenfilename(
            title="Select a file to encrypt",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            self.file_label.config(text=file_path, foreground="black")

            # Get file info
            file_size = os.path.getsize(file_path)
            self.file_info_label.config(
                text=f"File: {file_name} | Size: {file_size:,} bytes"
            )

            self.update_status(f"File selected: {file_name}")

    def perform_hybrid_encryption(self):
        """Perform hybrid encryption (AES + RSA)."""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return

        try:
            self.update_status("Encrypting with Hybrid (AES + RSA)...")
            self.crypto.clear_logs()

            # Perform hybrid encryption
            results = self.crypto.hybrid_encrypt_file(
                self.selected_file,
                output_dir="output"
            )

            self.encryption_results = results

            # Verify encryption
            self.crypto.log_message("\n[*] Performing Verification:")
            original_hash = self.crypto.calculate_file_hash(self.selected_file)
            self.crypto.log_message(f"[+] Original file SHA-256: {original_hash}")

            # Show results
            self.display_logs()
            self.update_status("✓ Hybrid encryption completed successfully!")

            messagebox.showinfo(
                "Success",
                f"Hybrid Encryption Completed!\n\n"
                f"Encrypted file: output/encrypted_hybrid.bin\n"
                f"Keys saved to: output/\n\n"
                f"Original size: {results['metadata']['original_size']:,} bytes\n"
                f"Encrypted size: {results['metadata']['ciphertext_size']:,} bytes"
            )

        except Exception as e:
            self.update_status(f"✗ Error: {str(e)}")
            messagebox.showerror("Encryption Error", f"Error during encryption:\n{str(e)}")
            self.crypto.log_message(f"[!] ERROR: {str(e)}")
            self.display_logs()

    def perform_comparison(self):
        """Perform AES vs DES comparison."""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return

        try:
            self.update_status("Comparing AES vs DES...")
            self.crypto.clear_logs()

            # Perform comparison
            results = self.crypto.compare_aes_vs_des(
                self.selected_file,
                output_dir="output"
            )

            # Generate comparison summary
            self.crypto.log_message("\n" + "=" * 60)
            self.crypto.log_message("DETAILED PERFORMANCE COMPARISON")
            self.crypto.log_message("=" * 60)

            aes_total = results['aes']['encrypt_time'] + results['aes']['decrypt_time']
            des_total = results['des']['encrypt_time'] + results['des']['decrypt_time']

            self.crypto.log_message(f"\nAES-256:")
            self.crypto.log_message(f"  Encrypt Time: {results['aes']['encrypt_time']*1000:.2f}ms")
            self.crypto.log_message(f"  Decrypt Time: {results['aes']['decrypt_time']*1000:.2f}ms")
            self.crypto.log_message(f"  Total Time: {aes_total*1000:.2f}ms")
            self.crypto.log_message(f"  Ciphertext Size: {results['aes']['ciphertext_size']:,} bytes")

            self.crypto.log_message(f"\nDES (56-bit):")
            self.crypto.log_message(f"  Encrypt Time: {results['des']['encrypt_time']*1000:.2f}ms")
            self.crypto.log_message(f"  Decrypt Time: {results['des']['decrypt_time']*1000:.2f}ms")
            self.crypto.log_message(f"  Total Time: {des_total*1000:.2f}ms")
            self.crypto.log_message(f"  Ciphertext Size: {results['des']['ciphertext_size']:,} bytes")

            efficiency = (des_total / aes_total) if aes_total > 0 else 0
            self.crypto.log_message(f"\nAES is {efficiency:.2f}x {'faster' if efficiency > 1 else 'slower'} than DES")
            self.crypto.log_message("=" * 60)

            self.display_logs()
            self.update_status("✓ AES vs DES comparison completed!")

            messagebox.showinfo(
                "Comparison Complete",
                f"Algorithm Comparison Results:\n\n"
                f"AES Total Time: {aes_total*1000:.2f}ms\n"
                f"DES Total Time: {des_total*1000:.2f}ms\n\n"
                f"AES Ciphertext: {results['aes']['ciphertext_size']:,} bytes\n"
                f"DES Ciphertext: {results['des']['ciphertext_size']:,} bytes\n\n"
                f"Encrypted files saved to: output/"
            )

        except Exception as e:
            self.update_status(f"✗ Error: {str(e)}")
            messagebox.showerror("Comparison Error", f"Error during comparison:\n{str(e)}")
            self.crypto.log_message(f"[!] ERROR: {str(e)}")
            self.display_logs()

    def display_logs(self):
        """Display crypto utility logs in the text widget."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)

        logs = self.crypto.get_logs()
        self.log_text.insert(tk.END, logs)

        # Color coding
        self._apply_log_colors()

        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)  # Auto-scroll to end

    def _apply_log_colors(self):
        """Apply color coding to log messages."""
        log_text = self.log_text
        content = log_text.get(1.0, tk.END)

        # Success messages (green)
        log_text.tag_remove("success", 1.0, tk.END)
        for pattern in ["[+]", "✓"]:
            start_idx = "1.0"
            while True:
                idx = log_text.search(pattern, start_idx, tk.END)
                if not idx:
                    break
                end_idx = f"{idx}+{len(pattern)}c"
                log_text.tag_add("success", idx, end_idx)
                start_idx = end_idx

        # Error messages (red)
        log_text.tag_remove("error", 1.0, tk.END)
        for pattern in ["[!]", "ERROR", "✗"]:
            start_idx = "1.0"
            while True:
                idx = log_text.search(pattern, start_idx, tk.END)
                if not idx:
                    break
                end_idx = f"{idx}+{len(pattern)}c"
                log_text.tag_add("error", idx, end_idx)
                start_idx = end_idx

    def clear_logs(self):
        """Clear the log display and crypto logs."""
        self.crypto.clear_logs()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.update_status("Logs cleared")

    def update_status(self, message: str):
        """
        Update status bar message.
        
        Args:
            message: Status message to display
        """
        self.status_label.config(text=message)
        self.root.update()

    def generate_random_data(self):
        """Generate random student data for testing."""
        try:
            self.update_status("Generating random student data...")

            # Call the generate_student_data function with silent=True for GUI use
            data_file = generate_student_data(
                output_file="data/original_data.csv",
                num_records=10,
                silent=True  # Suppress console output to avoid GUI conflicts
            )

            self.update_status("✓ Random data generated successfully!")

            # Update selected file to the generated data
            self.selected_file = data_file
            self.file_label.config(text=data_file, foreground="black")
            file_size = os.path.getsize(data_file)
            self.file_info_label.config(
                text=f"File: original_data.csv | Size: {file_size:,} bytes"
            )

            messagebox.showinfo(
                "Success",
                f"Random student data generated!\n\n"
                f"File: {data_file}\n"
                f"Records: 10\n"
                f"Size: {file_size:,} bytes\n\n"
                f"File is ready for encryption!"
            )

        except Exception as e:
            self.update_status(f"✗ Error: {str(e)}")
            messagebox.showerror("Generation Error", f"Error generating data:\n{str(e)}")

    def show_decrypt_dialog(self):
        """Show dialog for decryption file selection."""
        # Create a new top-level window
        decrypt_window = tk.Toplevel(self.root)
        decrypt_window.title("Decrypt Hybrid Encryption")
        decrypt_window.geometry("700x450")
        decrypt_window.resizable(True, True)

        # Make dialog modal
        decrypt_window.transient(self.root)
        decrypt_window.grab_set()

        # Main frame
        main_frame = ttk.Frame(decrypt_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="Select files for decryption:\n1. Encrypted file (encrypted_hybrid.bin)\n2. Private key file (private_key.pem)\n3. Metadata file (encryption_metadata.json)",
            font=("Arial", 10)
        )
        instructions.pack(anchor=tk.W, pady=10)

        # Encrypted file selection
        file_frame = ttk.LabelFrame(main_frame, text="Encrypted File", padding="10")
        file_frame.pack(fill=tk.X, pady=5)

        ttk.Label(file_frame, text="File:", foreground="gray").pack(side=tk.LEFT)
        self.encrypted_file_label = ttk.Label(
            file_frame,
            text="No file selected",
            foreground="gray"
        )
        self.encrypted_file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Button(
            file_frame,
            text="Browse",
            command=lambda: self._select_encrypted_file(self.encrypted_file_label)
        ).pack(side=tk.LEFT)

        # Private key selection
        key_frame = ttk.LabelFrame(main_frame, text="Private Key File", padding="10")
        key_frame.pack(fill=tk.X, pady=5)

        ttk.Label(key_frame, text="File:", foreground="gray").pack(side=tk.LEFT)
        self.private_key_label = ttk.Label(
            key_frame,
            text="No file selected",
            foreground="gray"
        )
        self.private_key_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Button(
            key_frame,
            text="Browse",
            command=lambda: self._select_private_key(self.private_key_label)
        ).pack(side=tk.LEFT)

        # Metadata selection
        metadata_frame = ttk.LabelFrame(main_frame, text="Metadata File", padding="10")
        metadata_frame.pack(fill=tk.X, pady=5)

        ttk.Label(metadata_frame, text="File:", foreground="gray").pack(side=tk.LEFT)
        self.metadata_file_label = ttk.Label(
            metadata_frame,
            text="No file selected",
            foreground="gray"
        )
        self.metadata_file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Button(
            metadata_frame,
            text="Browse",
            command=lambda: self._select_metadata_file(self.metadata_file_label)
        ).pack(side=tk.LEFT)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)

        ttk.Button(
            button_frame,
            text="Decrypt",
            command=lambda: self._perform_decryption_from_dialog(decrypt_window)
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=decrypt_window.destroy
        ).pack(side=tk.LEFT, padx=5)

    def _select_encrypted_file(self, label):
        """Browse and select encrypted file."""
        file_path = filedialog.askopenfilename(
            title="Select encrypted file",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if file_path:
            self.selected_encrypted_file = file_path
            label.config(text=file_path, foreground="black")

    def _select_private_key(self, label):
        """Browse and select private key file."""
        file_path = filedialog.askopenfilename(
            title="Select private key file",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
        )
        if file_path:
            self.selected_private_key = file_path
            label.config(text=file_path, foreground="black")

    def _select_metadata_file(self, label):
        """Browse and select metadata file."""
        file_path = filedialog.askopenfilename(
            title="Select metadata file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.selected_metadata_file = file_path
            label.config(text=file_path, foreground="black")

    def _perform_decryption_from_dialog(self, dialog_window):
        """Perform decryption with selected files."""
        if not self.selected_encrypted_file or not self.selected_private_key or not self.selected_metadata_file:
            messagebox.showerror("Error", "Please select all required files!")
            return

        try:
            self.update_status("Decrypting hybrid file...")
            self.crypto.clear_logs()

            # Load metadata
            metadata = self.crypto.load_metadata(self.selected_metadata_file)

            # Read private key
            with open(self.selected_private_key, 'rb') as f:
                private_key = f.read()

            # Decode metadata from Base64
            aes_iv = self.crypto.decode_base64(metadata['aes_iv'])
            encrypted_aes_key = self.crypto.decode_base64(metadata['encrypted_aes_key'])

            # Perform decryption
            decrypted_file = self.crypto.hybrid_decrypt_file(
                encrypted_file=self.selected_encrypted_file,
                private_key=private_key,
                encrypted_aes_key=encrypted_aes_key,
                aes_iv=aes_iv,
                output_dir="output"
            )

            # Get file sizes and hashes from metadata
            original_size = metadata.get('original_size', 0)
            encrypted_size = metadata.get('ciphertext_size', 0)
            original_file_hash = metadata.get('original_file_hash', None)

            self.crypto.log_message("\n[*] Decryption Summary:")
            self.crypto.log_message(f"[+] Original size: {original_size:,} bytes")
            self.crypto.log_message(f"[+] Encrypted size: {encrypted_size:,} bytes")
            self.crypto.log_message(f"[+] Decrypted file: {decrypted_file}")

            # Perform integrity verification using SHA-256
            self.crypto.log_message("\n[*] File Integrity Verification:")
            decrypted_file_hash = self.crypto.calculate_file_hash(decrypted_file)
            self.crypto.log_message(f"[+] Original file SHA-256:  {original_file_hash}")
            self.crypto.log_message(f"[+] Decrypted file SHA-256: {decrypted_file_hash}")

            if original_file_hash and original_file_hash == decrypted_file_hash:
                self.crypto.log_message(f"\n[+] ✓ INTEGRITY VERIFIED: Decrypted file matches original!")
                verification_result = "✓ INTEGRITY VERIFIED"
                verification_success = True
            else:
                if not original_file_hash:
                    self.crypto.log_message(f"\n[!] WARNING: Original file hash not available in metadata")
                    verification_result = "⚠ Hash comparison unavailable"
                    verification_success = None
                else:
                    self.crypto.log_message(f"\n[!] ✗ INTEGRITY FAILED: Decrypted file does NOT match original!")
                    verification_result = "✗ INTEGRITY FAILED"
                    verification_success = False

            self.display_logs()
            self.update_status("✓ Decryption completed successfully!")
            dialog_window.destroy()

            # Show detailed message based on verification result
            if verification_success is True:
                messagebox.showinfo(
                    "Decryption & Verification Successful",
                    f"✓ Decryption Completed Successfully!\n\n"
                    f"Decrypted file: {decrypted_file}\n\n"
                    f"Original size: {original_size:,} bytes\n"
                    f"Encrypted size: {encrypted_size:,} bytes\n\n"
                    f"✓ File Integrity Verified:\n"
                    f"SHA-256 Match: YES\n\n"
                    f"The decrypted file is identical to the original!"
                )
            elif verification_success is False:
                messagebox.showwarning(
                    "Decryption Completed - Integrity Warning",
                    f"Decryption Completed!\n\n"
                    f"Decrypted file: {decrypted_file}\n\n"
                    f"Original size: {original_size:,} bytes\n"
                    f"Encrypted size: {encrypted_size:,} bytes\n\n"
                    f"⚠ INTEGRITY CHECK FAILED:\n"
                    f"SHA-256 Mismatch: The decrypted file does NOT match the original!\n\n"
                    f"This may indicate corruption or tampering."
                )
            else:
                messagebox.showinfo(
                    "Decryption Completed",
                    f"Decryption Completed!\n\n"
                    f"Decrypted file: {decrypted_file}\n\n"
                    f"Original size: {original_size:,} bytes\n"
                    f"Encrypted size: {encrypted_size:,} bytes\n\n"
                    f"Note: Original file hash not available in metadata.\n"
                    f"Decrypted file SHA-256: {decrypted_file_hash}"
                )

        except Exception as e:
            self.update_status(f"✗ Error: {str(e)}")
            self.crypto.log_message(f"[!] ERROR: {str(e)}")
            self.display_logs()
            messagebox.showerror("Decryption Error", f"Error during decryption:\n{str(e)}")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = CryptoLabGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
