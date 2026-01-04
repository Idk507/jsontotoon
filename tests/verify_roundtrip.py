import json

with open('test_input.json') as f:
    original = json.load(f)

with open('test_roundtrip.json') as f:
    result = json.load(f)

print('Round-trip match:', original == result)
if original != result:
    print('Original:', original)
    print('Result:', result)
