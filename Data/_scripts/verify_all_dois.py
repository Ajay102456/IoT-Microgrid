import re, json, time, subprocess, difflib, sys

with open("/home/s/Documents/MicroGrid-IoT/Data/_scripts/verified_refs.txt") as f:
    lines = [l.rstrip("\n") for l in f if l.strip()]

entries = []
for line in lines:
    m = re.match(r'\[\d+\]\s+\(orig#(\d+)\)\s+(.*)', line)
    orig_num = m.group(1)
    body = m.group(2)
    doi_m = re.search(r'DOI:(\S+)\s*$', body)
    doi = doi_m.group(1) if doi_m else None
    # extract claimed title: text between the first ". " after authors/year and the next " *" (italic journal marker)
    title_m = re.match(r'.*?\(\d{4}[a-z]?\)\.\s*(.*?)\.\s*\*', body)
    title = title_m.group(1).strip() if title_m else None
    entries.append({"orig": orig_num, "doi": doi, "claimed_title": title, "raw": body})

print(f"Total entries: {len(entries)}, with DOI: {sum(1 for e in entries if e['doi'])}")

results = []
for i, e in enumerate(entries):
    if not e["doi"]:
        results.append({**e, "status": "NO_DOI"})
        continue
    try:
        out = subprocess.run(
            ["curl", "-s", "--max-time", "12",
             f"https://api.crossref.org/works/{e['doi']}",
             "-H", "User-Agent: verification-check/1.0 (mailto:verify@example.com)"],
            capture_output=True, text=True, timeout=15
        )
        data = json.loads(out.stdout)
        if "message" not in data:
            results.append({**e, "status": "NOT_FOUND", "crossref_title": None})
            continue
        msg = data["message"]
        cr_title = (msg.get("title") or [None])[0]
        cr_journal = (msg.get("container-title") or [None])[0]
        sim = difflib.SequenceMatcher(None, (e["claimed_title"] or "").lower(), (cr_title or "").lower()).ratio() if cr_title else 0.0
        status = "MATCH" if sim > 0.6 else "TITLE_MISMATCH"
        results.append({**e, "status": status, "crossref_title": cr_title, "crossref_journal": cr_journal, "similarity": round(sim, 2)})
    except Exception as ex:
        results.append({**e, "status": "ERROR", "error": str(ex)})
    if (i+1) % 20 == 0:
        print(f"  ...{i+1}/{len(entries)} checked", file=sys.stderr)
    time.sleep(0.15)

with open("/home/s/Documents/MicroGrid-IoT/Data/_scripts/doi_verification_results.json", "w") as f:
    json.dump(results, f, indent=2)

# Summary
from collections import Counter
c = Counter(r["status"] for r in results)
print()
print("=== SUMMARY ===")
for k, v in c.items():
    print(f"  {k}: {v}")

print()
print("=== FLAGGED ENTRIES (not clean MATCH) ===")
for r in results:
    if r["status"] != "MATCH":
        print(f"  orig#{r['orig']} [{r['status']}] DOI={r['doi']}")
        print(f"      claimed:  {r.get('claimed_title')}")
        print(f"      crossref: {r.get('crossref_title')}")
