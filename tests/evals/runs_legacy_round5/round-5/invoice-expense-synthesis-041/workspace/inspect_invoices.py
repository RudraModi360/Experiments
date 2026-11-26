import glob
import os

# Let's inspect all files in invoices/
for path in sorted(glob.glob('invoices/*')):
    print(f"=== {path} ===")
    with open(path) as f:
        print(f.read())
