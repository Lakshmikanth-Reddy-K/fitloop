import requests
import os
import time
import csv

BASE = os.getenv("FITLOOP_BASE", "http://localhost:8000")
TOKEN = os.getenv("AUTH_TOKEN", "changeme123")

HEADERS = {"X-Auth-Token": TOKEN}

reviews_path = "sample_data/reviews_sample.csv"
returns_path = "sample_data/returns_sample.csv"

print("== Health Check ==")
r = requests.get(f"{BASE}/", headers=HEADERS)
print(r.status_code, r.text[:120])

print("== Uploading CSVs ==")
with open(reviews_path, 'rb') as rv, open(returns_path, 'rb') as rt:
    files = {
        'reviews_csv': ('reviews_sample.csv', rv, 'text/csv'),
        'returns_csv': ('returns_sample.csv', rt, 'text/csv')
    }
    r2 = requests.post(f"{BASE}/upload", headers=HEADERS, files=files)
    print(r2.status_code, r2.json())

print("== Processing ==")
r3 = requests.post(f"{BASE}/process", headers=HEADERS)
print(r3.status_code, r3.json())

print("== Products ==")
r4 = requests.get(f"{BASE}/products", headers=HEADERS)
print(r4.status_code, r4.json())

if r4.ok and r4.json():
    pid = r4.json()[0]['product_id']
    print(f"== Product Detail {pid} ==")
    r5 = requests.get(f"{BASE}/product/{pid}", headers=HEADERS)
    print(r5.status_code, list(r5.json().keys()))

    print("== Export ==")
    r6 = requests.get(f"{BASE}/export/{pid}", headers=HEADERS)
    print(r6.status_code, 'markdown length', len(r6.text))

print("== DONE ==")
