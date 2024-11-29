import hashlib
import os

def hash_string(text):
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    sha512_hash = hashlib.sha512(text.encode()).hexdigest()
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    return sha256_hash, sha512_hash, md5_hash

def hash_file(file_path):
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    md5 = hashlib.md5()

    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
                sha512.update(chunk)
                md5.update(chunk)
    except FileNotFoundError:
        return None, None, None

    return sha256.hexdigest(), sha512.hexdigest(), md5.hexdigest()

def hash_directory(directory_path):
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    md5 = hashlib.md5()

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    while chunk := f.read(8192):
                        sha256.update(chunk)
                        sha512.update(chunk)
                        md5.update(chunk)
            except FileNotFoundError:
                continue

    return sha256.hexdigest(), sha512.hexdigest(), md5.hexdigest()

def main():
    choice = input(
        "Please select the input method: text (T), file path (F) or folder path (D)? (T/F/D): "
    ).strip().upper()
    if choice == 'T':
        text = input("Enter Text: ").strip()
        sha256_hash, sha512_hash, md5_hash = hash_string(text)
    elif choice == 'F':
        file_path = input("Enter path: ").strip()
        sha256_hash, sha512_hash, md5_hash = hash_file(file_path)
        if not sha256_hash:
            print("File not found.")
            return
    elif choice == 'D':
        directory_path = input("Enter folder path: ").strip()
        sha256_hash, sha512_hash, md5_hash = hash_directory(directory_path)
    else:
        print("Invalid choice.")
        return

    print(f"SHA256: {sha256_hash}")
    print(f"SHA512: {sha512_hash}")
    print(f"MD5: {md5_hash}")


if __name__ == "__main__":
    main()
