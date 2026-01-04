import sys
sys.path.insert(0, 'src')

from json2toon import ToonConfig, ToonEncoder

# Simple test
data = {"name": "Alice", "age": 30}

print("Test 1: Default separator")
config_default = ToonConfig()
print(f"Separator: '{config_default.separator}'")
encoder = ToonEncoder(config_default)
print(encoder.encode(data))

print("\nTest 2: Custom separator")
config_sep = ToonConfig(separator=" = ")
print(f"Separator: '{config_sep.separator}'")
encoder_sep = ToonEncoder(config_sep)
print(encoder_sep.encode(data))

print("\n✓ Success - no errors!")
