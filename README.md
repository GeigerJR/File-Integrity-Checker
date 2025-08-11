
---

````markdown
# File Integrity Checker

A command-line tool to verify the integrity of log files and detect tampering by using SHA-256 cryptographic hashing.

---

## Project Overview

This tool enhances security by monitoring log files and directories for unauthorized changes. It supports initialization of a hash database, verification of file integrity, and updating stored hashes after legitimate modifications.

---

## Features

- Initialize hash storage for single files or entire directories.
- Verify current file hashes against stored hashes.
- Detect and report any changes indicating possible tampering.
- Update stored hashes when files are intentionally changed.
- Simple command-line interface with clear status messages.

---

## Technologies Used

- Python 3.12
- SHA-256 hashing (via Python's `hashlib`)
- File system operations for directory traversal
- JSON for storing hash records securely

---

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repo-url>
   cd file-integrity-checker
````

2. **Create and activate a Python virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   *(No external dependencies required; uses Python standard libraries)*

---

## Usage

### Initialize hash storage for a directory or file

```bash
python3 integrity_checker.py init /path/to/logs
```

Output:

```
✅ Hashes stored successfully.
```

---

### Check integrity status

```bash
python3 integrity_checker.py check /path/to/log/or/directory
```

Output example for unmodified files:

```
✅ Unmodified: /path/to/log1.log
✅ Unmodified: /path/to/log2.log
```

Output example for modified files:

```
⚠️ Modified: /path/to/log1.log (Hash mismatch)
```

---

### Update hashes after intentional changes

```bash
python3 integrity_checker.py update /path/to/modified/log.log
```

Output:

```
🔄 Hash updated successfully.
```

---

## Best Practices

* Run `init` on clean logs to establish baseline hashes.
* Regularly run `check` to monitor for tampering.
* Use `update` only when authorized changes have been made.
* Store the hash database file securely to prevent tampering.

---

## Notes

* The tool handles both files and directories recursively.
* Non-regular files or inaccessible files are skipped with warnings.
* The hash database is stored as `.integrity_hashes.json` in the current working directory.

---

## Example Workflow

```bash
# Initialize hashes
python3 integrity_checker.py init ~/log-test

# Verify logs (detect tampering)
python3 integrity_checker.py check ~/log-test

# Update hash after intentional edits
python3 integrity_checker.py update ~/log-test/test1.log
```

---

## Author

Phillip — DevOps Engineer passionate about security and automation.

---

```
https://roadmap.sh/projects/file-integrity-checker
```
