"""
Test script untuk cek API products
Jalankan: python test_api_products.py
"""
import requests
import json

API_URL = 'http://localhost:5000/api'

# Login sebagai owner
login_data = {
    'username': 'owner',
    'password': 'admin123'
}

print("🔐 Logging in...")
login_res = requests.post(f'{API_URL}/auth/login', json=login_data)
if login_res.status_code != 200:
    print(f"❌ Login failed: {login_res.status_code}")
    print(login_res.text)
    exit(1)

token = login_res.json()['access_token']
print("✅ Login berhasil")

# Get products
print("\n📦 Getting products...")
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

products_res = requests.get(f'{API_URL}/products', headers=headers)
print(f"Status: {products_res.status_code}")
print(f"Content-Type: {products_res.headers.get('content-type')}")

if products_res.status_code == 200:
    data = products_res.json()
    print(f"\n📊 Response format:")
    print(f"  - Type: {type(data)}")
    print(f"  - Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
    
    if isinstance(data, dict) and 'products' in data:
        products = data['products']
        print(f"\n✅ Found {len(products)} products:")
        for i, p in enumerate(products, 1):
            print(f"  {i}. {p.get('product_name', 'N/A')} - Rp {p.get('product_price', 0):,.0f}")
    elif isinstance(data, list):
        print(f"\n✅ Found {len(data)} products (array format):")
        for i, p in enumerate(data, 1):
            print(f"  {i}. {p.get('product_name', 'N/A')} - Rp {p.get('product_price', 0):,.0f}")
    else:
        print(f"\n⚠️  Unexpected format:")
        print(json.dumps(data, indent=2)[:500])
else:
    print(f"❌ Error: {products_res.status_code}")
    print(products_res.text[:500])

