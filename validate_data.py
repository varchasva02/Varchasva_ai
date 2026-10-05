import json
from pathlib import Path

DATA_DIR = Path("data")

files = list(DATA_DIR.rglob("*.json"))

print(f"\nFound {len(files)} JSON files.\n")

failed = False

for file in files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            json.load(f)

        print(f"✓ {file}")

    except json.JSONDecodeError as e:
        print(f"✗ {file}")
        print(f"  Error: {e}")
        failed = True

print()

if failed:
    print("❌ Data validation failed.")
else:
    print("✅ All JSON files are valid.")
