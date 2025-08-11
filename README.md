Absolutely! Here’s the **same professional README** but now enhanced with the **exact commands** the user should run at each step. You can copy-paste this directly to your GitHub or share as a guide:

---

# File Integrity Checker

A **File Integrity Checker** is a security tool used to detect unauthorized modifications in log files or any critical files by computing and verifying cryptographic hashes (SHA-256). This project guides you through building a simple, effective tool to track file integrity and identify tampering.

---

## Project Overview

The tool will:

* Accept a file or directory path as input.
* Compute SHA-256 hashes for each file.
* Store these hashes securely for future reference.
* Compare current file hashes against stored hashes to detect changes.
* Allow manual re-initialization or update of the stored hashes.

By completing this project, you'll learn about hashing algorithms, file I/O, scripting best practices, and basic security concepts.

---

## Step-by-Step Implementation Guide

### Step 1: Setup Your Development Environment

* Ensure you have **Python 3.6+** installed on your system.
* (Optional) Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

* Create and navigate to your project directory:

```bash
mkdir file-integrity-checker
cd file-integrity-checker
```

---

### Step 2: Design the Integrity Checker Script

* Create your Python script file:

```bash
nano integrity_checker.py
```

* (Write your hashing logic, CLI commands parsing, etc.)

---

### Step 3: Implement File Hashing Functionality

* Use Python’s `hashlib` in your script to compute SHA-256 hashes.
* Ensure your script handles files and directories.

---

### Step 4: Write Command Logic in the Script

The script will support these commands: `init`, `check`, and `update`.

#!/usr/bin/env python3

import os
import sys
import hashlib

HASH_FILE = ".hashes"

def compute_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (FileNotFoundError, PermissionError) as e:
        print(f"⚠️ Skipping {file_path}: {e}")
        return None

def load_hashes():
    hashes = {}
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                path, file_hash = line.strip().split(" ", 1)
                hashes[path] = file_hash
    return hashes

def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        for path, file_hash in hashes.items():
            f.write(f"{path} {file_hash}\n")

def init(path):
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        sys.exit(1)

    hashes = {}
    if os.path.isfile(path):
        h = compute_hash(path)
        if h:
            hashes[path] = h
    else:
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                h = compute_hash(full_path)
                if h:
                    hashes[full_path] = h
    save_hashes(hashes)
    print("✅ Hashes stored successfully.")

def check(path):
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        sys.exit(1)

    stored_hashes = load_hashes()
    if not stored_hashes:
        print(f"Error: No stored hashes found. Please run 'init' first.")
        sys.exit(1)

    if os.path.isfile(path):
        paths_to_check = [path]
    else:
        paths_to_check = []
        for root, _, files in os.walk(path):
            for file in files:
                paths_to_check.append(os.path.join(root, file))

    modified_files = False
    for file_path in paths_to_check:
        current_hash = compute_hash(file_path)
        if not current_hash:
            continue  # skip unreadable files

        stored_hash = stored_hashes.get(file_path)
        if stored_hash is None:
            print(f"⚠️ {file_path} not found in stored hashes.")
            modified_files = True
        elif stored_hash == current_hash:
            print(f"✅ Unmodified: {file_path}")
        else:
            print(f"❌ Modified: {file_path}")
            modified_files = True

    if modified_files:
        print("\n⚠️ Some files have been modified or are new.")
    else:
        print("\n✅ All checked files are unmodified.")

def update(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist or is not a file.")
        sys.exit(1)

    stored_hashes = load_hashes()
    if not stored_hashes:
        print(f"Error: No stored hashes found. Please run 'init' first.")
        sys.exit(1)

    new_hash = compute_hash(file_path)
    if not new_hash:
        print(f"Error: Could not read file '{file_path}'.")
        sys.exit(1)

    stored_hashes[file_path] = new_hash
    save_hashes(stored_hashes)
    print("🔄 Hash updated successfully.")

def print_usage():
    print("Usage:")
    print("  integrity_checker.py init <path>     # Initialize hashes for file or directory")
    print("  integrity_checker.py check <path>    # Check files for modifications")
    print("  integrity_checker.py update <file>   # Update hash for a single file")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()
    path = sys.argv[2]

    if command == "init":
        init(path)
    elif command == "check":
        check(path)
    elif command == "update":
        update(path)
    else:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)

---

### Step 5: Testing Your Tool

Run these commands to test the functionality:

```bash
# Initialize hashes for all files in a directory
python3 integrity_checker.py init /path/to/logs

# Check for any file modifications
python3 integrity_checker.py check /path/to/logs

# Update the stored hash for a modified file
python3 integrity_checker.py update /path/to/logs/filename.log
```

**Example:**

```bash
python3 integrity_checker.py init /var/log
python3 integrity_checker.py check /var/log
python3 integrity_checker.py update /var/log/syslog
```

---

### Step 6: Optional Enhancements

* Add logging:

```bash
# Use Python logging module inside your script
```

* Encrypt stored hashes or secure storage location.
* Set up alerts for detected changes.
* Package as a CLI with argument parsing libraries (`argparse`).

---

## Example Project Structure

```
file-integrity-checker/
├── integrity_checker.py    # Main Python script
├── README.md               # This file
└── .hashes                 # Hash database file (generated after init)
```

---

## Summary

By following this guide and running the commands above, you will create a reliable tool to:

* Initialize and store file hashes securely,
* Detect unauthorized file changes,
* Update known good hashes when needed.

This is a practical security project to boost your scripting, cryptography, and system monitoring skills.

---

## Author

Phillip — DevOps Engineer passionate about security and automation.

---

```
https://roadmap.sh/projects/file-integrity-checker
```

