from json2toon import ToonEncoder, ToonDecoder
import json

# Test data
data = {
    "name": "Alice",
    "address": {"zip": "10001"},
    "hobbies": ["reading", "coding"]
}

print("=== Original Data ===")
print(json.dumps(data, indent=2))

encoder = ToonEncoder()
toon = encoder.encode(data)

print("\n=== TOON Format ===")
print(toon)
print("\n=== TOON repr ===")
print(repr(toon))

decoder = ToonDecoder()
result = decoder.decode(toon)

print("\n=== Decoded Data ===")
print(json.dumps(result, indent=2))

print("\n=== Match? ===")
print(f"Match: {data == result}")
if data != result:
    print(f"Original zip type: {type(data['address']['zip'])}")
    print(f"Result zip type: {type(result['address']['zip'])}")
    print(f"Original hobbies: {data['hobbies']}")
    print(f"Result hobbies: {result['hobbies']}")
