import glob

files = sorted(glob.glob('invoices/*'))
print("Files:", files)
for f in files:
    print("---", f)
    print(open(f).read())
