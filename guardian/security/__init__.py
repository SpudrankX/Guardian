import hashlib, os

def hash_file(path):
    """Generate SHA256 hash of a file."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def verify_integrity(path, expected_hash):
    file_hash = hash_file(path)
    if file_hash == expected_hash:
        print(f"✅ Integrity OK for {path}")
        return True
    else:
        print(f"⚠️ Integrity mismatch for {path}")
        return False
