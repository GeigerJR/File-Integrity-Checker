import os
import sys
import hashlib
import json
import argparse

HASH_STORE = "hashes.json"


def compute_hash(file_path):
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError) as e:
        print(f"⚠️ Skipping {file_path}: {e}")
        return None


def store_hashes(hashes):
    """Save hashes to JSON file."""
    with open(HASH_STORE, "w") as f:
        json.dump(hashes, f, indent=4)


def load_hashes():
    """Load stored hashes from JSON file."""
    if not os.path.exists(HASH_STORE):
        return {}
    with open(HASH_STORE, "r") as f:
        return json.load(f)


def init(path):
    """Initialize and store file hashes."""
    hashes = {}
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = compute_hash(file_path)
                if file_hash:
                    hashes[file_path] = file_hash
    else:
        file_hash = compute_hash(path)
        if file_hash:
            hashes[path] = file_hash

    store_hashes(hashes)
    print("✅ Hashes stored successfully.")


def compare_file_hash(file_path, hashes):
    """Compare a file’s current hash with stored hash."""
    if not os.path.isfile(file_path):
        print(f"⚠️ Skipping non-file: {file_path}")
        return

    current_hash = compute_hash(file_path)
    if not current_hash:
        return

    stored_hash = hashes.get(file_path)

    if stored_hash is None:
        print(f"❓ No stored hash for {file_path}")
    elif current_hash != stored_hash:
        print(f"🚨 Modified: {file_path} (hash mismatch)")
    else:
        print(f"✅ Unmodified: {file_path}")


def check(path):
    """Check integrity of file or directory."""
    hashes = load_hashes()
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                compare_file_hash(os.path.join(root, file), hashes)
    else:
        compare_file_hash(path, hashes)


def update(path):
    """Update stored hash for file or directory."""
    hashes = load_hashes()
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = compute_hash(file_path)
                if file_hash:
                    hashes[file_path] = file_hash
    else:
        file_hash = compute_hash(path)
        if file_hash:
            hashes[path] = file_hash

    store_hashes(hashes)
    print("🔄 Hash updated successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("command", choices=["init", "check", "update"], help="Action to perform")
    parser.add_argument("path", help="Path to file or directory")
    args = parser.parse_args()

    if args.command == "init":
        init(args.path)
    elif args.command == "check":
        check(args.path)
    elif args.command == "update":
        update(args.path)
