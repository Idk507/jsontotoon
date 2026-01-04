import json
from json2toon import ToonEncoder

with open('debug_cli.json') as f:
    data = json.load(f)

print("=== Data ===")
print(json.dumps(data, indent=2))

encoder = ToonEncoder()
toon = encoder.encode(data)

print("\n=== TOON ===")
print(toon)

print("\n=== Check hobbies ===")
print(f"Hobbies in data: {data.get('hobbies')}")
print(f"Hobbies in TOON: {'hobbies' in toon}")
