from json2toon import ToonEncoder, ToonDecoder
import json

# Comprehensive test covering all bug fixes
test_cases = [
    {
        "name": "Numeric strings",
        "data": {"zip": "10001", "phone": "555-1234", "number": "123"}
    },
    {
        "name": "Arrays", 
        "data": {"nums": [1, 2, 3], "strs": ["a", "b"], "mixed": [1, "a"]}
    },
    {
        "name": "Nested",
        "data": {"a": {"b": {"c": "deep"}}}
    },
    {
        "name": "Empty values",
        "data": {"empty_str": "", "empty_list": [], "empty_dict": {}}
    },
    {
        "name": "Special chars",
        "data": {"path": "C:\\Users\\file.txt", "text": "Line1\nLine2"}
    },
    {
        "name": "Whitespace",
        "data": {"trailing": "hello ", "leading": " world"}
    },
    {
        "name": "Deep arrays",
        "data": {"nested": [[[1, 2]]]}
    },
    {
        "name": "All types",
        "data": {
            "string": "text",
            "number": 42,
            "float": 3.14,
            "bool_true": True,
            "bool_false": False,
            "null_val": None,
            "array": [1, 2, 3],
            "object": {"key": "value"}
        }
    }
]

encoder = ToonEncoder()
decoder = ToonDecoder()

print("=" * 70)
print("FINAL COMPREHENSIVE VERIFICATION")
print("=" * 70)
print()

passed = 0
failed = 0

for test in test_cases:
    name = test["name"]
    data = test["data"]
    
    try:
        # Encode
        toon = encoder.encode(data)
        
        # Decode
        result = decoder.decode(toon)
        
        # Check match
        if result == data:
            print(f"✓ {name}")
            passed += 1
        else:
            print(f"✗ {name} - Mismatch")
            print(f"  Original: {data}")
            print(f"  Result:   {result}")
            failed += 1
    except Exception as e:
        print(f"✗ {name} - Exception: {e}")
        failed += 1

print()
print("=" * 70)
print(f"Passed: {passed}/{len(test_cases)}")

if failed == 0:
    print("🎉 ALL VERIFICATIONS PASSED!")
else:
    print(f"❌ {failed} verification(s) failed")
