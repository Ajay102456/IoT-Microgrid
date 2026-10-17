import re

with open("/home/s/Documents/MicroGrid-IoT/Data/_scripts/verified_refs.txt") as f:
    lines = [l.rstrip("\n") for l in f if l.strip()]

def latex_escape(s):
    return s.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")

out = []
out.append(r"\begin{thebibliography}{146}")
for line in lines:
    m = re.match(r'\[(\d+)\]\s+\(orig#\d+\)\s+(.*)', line)
    num = m.group(1)
    body = m.group(2)
    # extract DOI if present
    doi_m = re.search(r'DOI:(\S+)\s*$', body)
    doi = doi_m.group(1) if doi_m else None
    body_wo_doi = re.sub(r'\.\s*DOI:\S+\s*$', '.', body).strip()
    # convert *italic* markdown to \textit{}
    body_latex = re.sub(r'\*([^*]+)\*', r'\\textit{\1}', body_wo_doi)
    body_latex = latex_escape_doi = body_latex  # authors/titles already plain
    entry = f"\\bibitem{{ref{num}}}\n{body_latex}"
    if doi:
        entry += f" https://doi.org/{doi}."
    out.append(entry)
out.append(r"\end{thebibliography}")

with open("/home/s/Documents/MicroGrid-IoT/Data/_scripts/bibliography_block.tex", "w") as f:
    f.write("\n".join(out))

print(f"Wrote {len(lines)} bibitems to bibliography_block.tex")
