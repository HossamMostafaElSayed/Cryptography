"""
Generate Sample Student Data for Cryptography Lab
==================================================
This script creates a CSV file with 10 rows of fake student records
for testing encryption algorithms.

Author: Cybersecurity Engineer
Date: May 2026
"""

import csv
import random
from pathlib import Path


def generate_student_data(output_file: str = "data/original_data.csv", num_records: int = 10, silent: bool = False):
    """
    Generate sample student records and save to CSV file.
    
    Args:
        output_file: Path to output CSV file
        num_records: Number of student records to generate
        silent: If True, suppress console output (for GUI use)
    """
    # Sample data
    first_names = [
        "Ahmed", "Fatima", "Mohammed", "Aisha", "Hassan",
        "Mariam", "Omar", "Layla", "Ali", "Noor",
        "Sarah", "Karim", "Zainab", "Mustafa", "Hana"
    ]

    last_names = [
        "Al-Rashid", "Al-Mansouri", "Al-Maktoum", "Al-Thani", "Al-Nahyan",
        "Al-Zaabi", "Al-Rumaithy", "Al-Mansoori", "Al-Hashemi", "Al-Marri"
    ]

    # Create output directory if it doesn't exist
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    # Generate records
    records = []
    for i in range(num_records):
        student_id = 10001 + i
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        grade = round(random.uniform(60, 100), 2)

        records.append({
            'ID': student_id,
            'Name': name,
            'Grade': grade
        })

    # Write to CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ID', 'Name', 'Grade'])
            writer.writeheader()
            writer.writerows(records)

        if not silent:
            print(f"✓ Student data generated successfully!")
            print(f"  File: {output_file}")
            print(f"  Records: {num_records}")
            print(f"  File size: {Path(output_file).stat().st_size:,} bytes")
            print("\nSample data:")
            print("-" * 60)
            print(f"{'ID':<10} {'Name':<30} {'Grade':<10}")
            print("-" * 60)
            for record in records[:5]:
                print(f"{record['ID']:<10} {record['Name']:<30} {record['Grade']:<10}")
            if num_records > 5:
                print(f"... and {num_records - 5} more records")

    except IOError as e:
        if not silent:
            print(f"✗ Error writing to file: {e}")
        return False

    return True


if __name__ == "__main__":
    generate_student_data()
