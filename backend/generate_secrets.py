"""
Script untuk generate SECRET_KEY dan JWT_SECRET_KEY
Jalankan script ini untuk generate key yang aman
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate random secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

if __name__ == '__main__':
    import sys
    import io
    
    # Fix encoding untuk Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("Generating Secret Keys...\n")
    
    secret_key = generate_secret_key(50)
    jwt_secret = generate_secret_key(50)
    
    print("Copy ini ke file .env:\n")
    print("=" * 60)
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print("=" * 60)
    print("\nKeys generated! Copy ke file .env di folder backend/")

