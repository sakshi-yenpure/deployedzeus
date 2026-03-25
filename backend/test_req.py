import urllib.request
import json
import urllib.error

data = json.dumps({
    'username': 'testusernew', 
    'email': 'testnew@test.com', 
    'password': 'Password123!', 
    'password_confirm': 'Password123!',
    'first_name': 'Test', 
    'last_name': 'User',
    'phone': '1234567890'
}).encode('utf-8')
req = urllib.request.Request('http://localhost:8000/api/auth/register/', data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode())
except urllib.error.HTTPError as e:
    print("Error HTTP:", e.read().decode())
except Exception as e:
    print("Other error:", str(e))
