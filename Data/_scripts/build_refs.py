import re

with open("/home/s/Documents/MicroGrid-IoT/Topic Analysis.md") as f:
    text = f.read()

start = text.index("### 4.3 Included References")
end = text.index("### 4.4 Source Verification")
block = text[start:end]

# Parse numbered lines like: "65. Ahmad et al. (2024). Title. *Journal*. DOI:10.xxx"
pattern = re.compile(r'^(\d+)\.\s+(.*)$', re.MULTILINE)
entries = {}
for m in pattern.finditer(block):
    num = int(m.group(1))
    txt = m.group(2).strip()
    entries[num] = txt

print(f"Parsed {len(entries)} entries, range {min(entries)}-{max(entries)}")

DROPPED = {80, 85, 106}
EXCLUDED_UNVERIFIED = {65}  # Ahmad et al., Hindawi/Wiley, blocked from re-verification this session

final = {}
for num, txt in entries.items():
    if num in DROPPED or num in EXCLUDED_UNVERIFIED:
        continue
    # strip markdown emphasis/strikethrough and the "dropped"/"caution" trailing notes
    clean = re.sub(r'\*\*', '', txt)
    clean = re.sub(r'~~', '', clean)
    clean = re.sub(r'\s*—\s*\*\*dropped.*?\*\*', '', clean)
    clean = re.sub(r'\s*⚠️.*$', '', clean)
    final[num] = clean.strip()

print(f"Final citable set: {len(final)} entries (excluded: {sorted(DROPPED | EXCLUDED_UNVERIFIED)})")

# Renumber sequentially 1..N in original order, write out MDPI-ish numbered format
with open("/home/s/Documents/MicroGrid-IoT/Data/_scripts/verified_refs.txt", "w") as out:
    for i, (orig_num, txt) in enumerate(sorted(final.items()), start=1):
        out.write(f"[{i}] (orig#{orig_num}) {txt}\n")

print("Wrote verified_refs.txt")
