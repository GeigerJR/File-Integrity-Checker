
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

```
#!/usr/bin/env python3
import os
import sys
import hashlib
import json

HASH_DB = ".hashes"

def compute_hash(file_path):
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def load_hashes():
    """Load stored hashes from HASH_DB file."""
    if not os.path.exists(HASH_DB):
        return {}
    with open(HASH_DB, "r") as f:
        return json.load(f)

def save_hashes(hashes):
    """Save hashes to HASH_DB file."""
    with open(HASH_DB, "w") as f:
        json.dump(hashes, f, indent=2)

def init(path):
    """Initialize hashes for all files in a directory or single file."""
    hashes = {}
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    hashes[full_path] = compute_hash(full_path)
                    print(f"Hashed: {full_path}")
                except Exception as e:
                    print(f"Error hashing {full_path}: {e}")
    elif os.path.isfile(path):
        hashes[path] = compute_hash(path)
        print(f"Hashed: {path}")
    else:
        print(f"Path not found: {path}")
        sys.exit(1)
    save_hashes(hashes)
    print("✅ Hashes stored successfully.")

def check(path):
    """Check current hashes against stored hashes."""
    stored_hashes = load_hashes()
    if not stored_hashes:
        print("No stored hashes found. Please run init first.")
        sys.exit(1)
    
    paths_to_check = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                paths_to_check.append(os.path.join(root, file))
    elif os.path.isfile(path):
        paths_to_check.append(path)
    else:
        print(f"Path not found: {path}")
        sys.exit(1)

    for file_path in paths_to_check:
        try:
            current_hash = compute_hash(file_path)
            stored_hash = stored_hashes.get(file_path)
            if stored_hash is None:
                print(f"⚠️ New file detected (no stored hash): {file_path}")
            elif current_hash == stored_hash:
                print(f"✅ Unmodified: {file_path}")
            else:
                print(f"❌ Modified: {file_path}")
        except Exception as e:
            print(f"⚠️ Skipping {file_path}: {e}")

def update(path):
    """Update stored hash for a file."""
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        sys.exit(1)

    stored_hashes = load_hashes()
    if not stored_hashes:
        print("No stored hashes found. Please run init first.")
        sys.exit(1)

    try:
        new_hash = compute_hash(path)
        stored_hashes[path] = new_hash
        save_hashes(stored_hashes)
        print(f"🔄 Hash updated successfully for {path}.")
    except Exception as e:
        print(f"Error updating hash for {path}: {e}")

def print_usage():
    print(f"Usage: {sys.argv[0]} <init|check|update> <path>")

def main():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    command = sys.argv[1]
    path = sys.argv[2]
    if command == "init":
        init(path)
    elif command == "check":
        check(path)
    elif command == "update":
        update(path)
    else:
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
   ```

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


